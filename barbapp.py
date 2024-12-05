import os
import json
import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv  # For loading API key from environment variables

# Load environment variables from the .env file
load_dotenv()

application = Flask(__name__)

# Load the Google API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if Google API Key is loaded correctly
if not GOOGLE_API_KEY:
    print("Warning: Google API Key is missing. Please check your .env file.")

# Define the URL for the API to fetch the barbershop data
API_URL = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Business_Goods_and_Service_WebMercator/MapServer/36/query"
API_PARAMS = {
    'where': '1=1',          # Fetch all records
    'outFields': '*',        # Get all fields
    'outSR': 4326,           # Spatial reference (WGS84)
    'f': 'json'              # Response format
}

# Ensure the 'data' directory exists for caching
if not os.path.exists(os.path.join(application.root_path, 'data')):
    os.makedirs(os.path.join(application.root_path, 'data'))

def fetch_data_from_api():
    """
    Fetch barbershop data from the API.

    This function sends a GET request to the API defined in the API_URL 
    with the given parameters. If the request is successful, it returns 
    the list of barbershop features in JSON format. In case of failure, 
    it logs the error and returns an empty list.

    Returns:
        list: A list of barbershop data features from the API, or an empty list if the request fails.
    """
    try:
        response = requests.get(API_URL, params=API_PARAMS)
        response.raise_for_status()  # Will raise an error for 4xx/5xx HTTP responses
        return response.json().get('features', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []

def save_data(data):
    """
    Save barbershop data to a local JSON file.

    This function saves the provided barbershop data into a file located 
    in the 'data' directory under the 'bbs_data.json' filename. The data 
    is saved in a pretty-printed JSON format.

    Args:
        data (list): The list of barbershop data to be saved.
    """
    data_file_path = os.path.join(application.root_path, 'data', 'bbs_data.json')
    with open(data_file_path, 'w') as f:
        json.dump(data, f, indent=4)

def load_data():
    """
    Load barbershop data from the local JSON file.

    This function reads the barbershop data from the local 'bbs_data.json' file 
    in the 'data' directory. If the file doesn't exist, it returns an empty list.

    Returns:
        list: A list of barbershop data loaded from the local file, or an empty list if the file doesn't exist.
    """
    data_file_path = os.path.join(application.root_path, 'data', 'bbs_data.json')
    if os.path.exists(data_file_path):
        with open(data_file_path, 'r') as f:
            return json.load(f)
    return []

@application.route('/')
def index():
    """
    Render the index page with a list of barbershops.

    This route fetches the barbershop data from the API. If no data is returned,
    it loads the cached data from a local file. The barbershop data is then 
    formatted and passed to the 'index.html' template, along with the Google API key.

    Returns:
        render_template: The rendered index page with the barbershop data and API key.
    """
    # Fetch barbershop data from the API
    barbershops_data = fetch_data_from_api()
    
    # If the barbershops data is empty, load the local cached data (if available)
    if not barbershops_data:
        barbershops_data = load_data()
    
    # Ensure the data is up to date (optional step: can be omitted)
    save_data(barbershops_data)
    
    # Format barbershop data for display
    formatted_barbershops = [{
        'name': shop['attributes']['BARBERSHOP'],
        'address': shop['attributes']['ADDRESS'],
        'phone': shop['attributes']['PHONE'],
        'latitude': shop['geometry']['y'],
        'longitude': shop['geometry']['x']
    } for shop in barbershops_data]

    return render_template('index.html', barbershops=formatted_barbershops, google_api_key=GOOGLE_API_KEY)

@application.route('/add', methods=['GET', 'POST'])
def add_barbershop():
    """
    Handle adding a new barbershop.

    This route allows users to add a new barbershop. If the request method 
    is POST, it validates the form data, creates a new barbershop entry, 
    appends it to the existing data, and saves it to the local file. It 
    then redirects the user to the index page. If the request method is 
    GET, it renders the 'add_barbershop.html' form page.

    Returns:
        render_template: The rendered form page or a redirect to the index page after adding the new barbershop.
    """
    if request.method == 'POST':
        # Validate form data
        if not validate_form_data(request.form):
            return render_template('add_barbershop.html', error="Invalid input data, please check your values.")

        # Capture form data
        new_shop = {
            "attributes": {
                "BARBERSHOP": request.form['name'],
                "ADDRESS": request.form['address'],
                "PHONE": request.form['phone'],
                "WARD": request.form['ward'],
                "LATITUDE": float(request.form['latitude']),
                "LONGITUDE": float(request.form['longitude']),
                "MAR_WARD": request.form['ward_name'],
                "ZIPCODE": request.form['zipcode'],
                "MAR_ID": request.form['mar_id'],
                "GLOBALID": f"{{{request.form['globalid']}}}",
                "GIS_ID": f"UserAddedShop_{len(load_data()) + 1}",
                "CREATOR": None,
                "CREATED": None,
                "EDITOR": None,
                "EDITED": None,
                "OBJECTID": len(load_data()) + 1
            },
            "geometry": {
                "x": float(request.form['longitude']),
                "y": float(request.form['latitude'])
            }
        }

        # Load existing data and append the new shop
        barbershops = load_data()
        barbershops.append(new_shop)

        # Save the updated data to the JSON file
        save_data(barbershops)

        return redirect(url_for('index'))

    return render_template('add_barbershop.html')

def validate_form_data(form_data):
    """
    Validate the form data for the new barbershop.

    This function checks whether the latitude and longitude values in the form 
    are valid floats. If the validation fails, it returns False. Otherwise, it 
    returns True.

    Args:
        form_data (dict): The form data to be validated.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    try:
        # Check if latitude and longitude are valid floats
        latitude = float(form_data['latitude'])
        longitude = float(form_data['longitude'])
    except ValueError:
        return False  # Invalid data
    return True  # Data is valid

if __name__ == '__main__':
    application.run(debug=True)

