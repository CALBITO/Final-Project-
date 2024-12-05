import os
import json
import requests
import logging
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask application instance
application = Flask(__name__)

# Constants
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
API_URL = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Business_Goods_and_Service_WebMercator/MapServer/36/query"
API_PARAMS = {'where': '1=1', 'outFields': '*', 'outSR': 4326, 'f': 'json'}
DATA_DIR = os.path.join(application.root_path, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'bbs_data.json')

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Check if Google API Key is loaded
if not GOOGLE_API_KEY:
    logging.warning("Google API Key is missing. Please check your .env file.")

# Helper Functions
def fetch_data_from_api():
    """
    Fetch barbershop data from the API.
    Returns:
        list: A list of barbershop features or an empty list if the request fails.
    """
    try:
        response = requests.get(API_URL, params=API_PARAMS)
        response.raise_for_status()
        return response.json().get('features', [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return []

def save_data(data):
    """
    Save barbershop data to a local JSON file.
    """
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info("Barbershop data saved locally.")
    except IOError as e:
        logging.error(f"Error saving data to file: {e}")

def load_data():
    """
    Load barbershop data from the local JSON file.
    Returns:
        list: A list of barbershop data or an empty list if the file doesn't exist.
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except IOError as e:
            logging.error(f"Error loading data from file: {e}")
    return []

def validate_form_data(form_data):
    """
    Validate the form data for the new barbershop.
    Args:
        form_data (dict): The form data to be validated.
    Returns:
        bool: True if valid, False otherwise.
    """
    required_fields = ['name', 'address', 'phone', 'latitude', 'longitude']
    for field in required_fields:
        if not form_data.get(field):
            return False
    try:
        float(form_data['latitude'])
        float(form_data['longitude'])
        return True
    except ValueError:
        return False

# Routes
@application.route('/')
def index():
    """
    Render the index page with a list of barbershops.
    """
    barbershops_data = fetch_data_from_api()
    if not barbershops_data:
        logging.warning("Using cached data as API fetch failed.")
        barbershops_data = load_data()

    save_data(barbershops_data)

    formatted_barbershops = [
        {
            'name': shop['attributes']['BARBERSHOP'],
            'address': shop['attributes']['ADDRESS'],
            'phone': shop['attributes']['PHONE'],
            'latitude': shop['geometry']['y'],
            'longitude': shop['geometry']['x']
        }
        for shop in barbershops_data if 'geometry' in shop
    ]

    return render_template('index.html', barbershops=formatted_barbershops, google_api_key=GOOGLE_API_KEY)

@application.route('/add', methods=['GET', 'POST'])
def add_barbershop():
    """
    Handle adding a new barbershop.
    """
    if request.method == 'POST':
        if not validate_form_data(request.form):
            return render_template('add_barbershop.html', error="Invalid input data. Please check your values.")

        new_shop = {
            "attributes": {
                "BARBERSHOP": request.form['name'],
                "ADDRESS": request.form['address'],
                "PHONE": request.form['phone'],
                "WARD": request.form.get('ward', ''),
                "ZIPCODE": request.form.get('zipcode', ''),
                "GIS_ID": f"UserAddedShop_{len(load_data()) + 1}",
            },
            "geometry": {
                "x": float(request.form['longitude']),
                "y": float(request.form['latitude'])
            }
        }

        barbershops = load_data()
        barbershops.append(new_shop)
        save_data(barbershops)

        return redirect(url_for('index'))

    return render_template('add_barbershop.html')

# Run the application
if __name__ == '__main__':
    application.run(debug=True)
