# Final-Project-Team members : Carlos Pena Acosta

Barbershop Locator Application
Overview
The Barbershop Locator Application is a Flask-based web app that allows users to view a list of barbershops in Washington, D.C., fetched from an external API. Users can also add new barbershops, which are saved locally for persistence. The app integrates with the Google Maps API to display barbershop locations on an interactive map.

Features
Fetches barbershop data from the DC GIS external API.
Caches fetched data locally in a data/bbs_data.json file.
Displays barbershop details (name, address, phone, latitude, longitude) in a user-friendly interface.
Allows users to add new barbershop entries via a form.
Validates input data to ensure geographic coordinates are accurate.
Integrates with the Google Maps API for map visualization.
(Work in Progress):
Geolocation functionality, including the search bar and support for addresses beyond the Open Data public API.
Logo image displays locally but is not rendering properly on the live domain.
Technologies Used
Python: Core programming language.
Flask: Framework for creating the web application.
JavaScript: Used for Google Maps API integration.
HTML/CSS: Front-end styling and structure.
DC GIS API: Source of barbershop data.
Google Maps API: For displaying map visualizations.
dotenv: For managing environment variables.
Setup Instructions
1. Prerequisites
Python 3.8+ installed.
A Google Maps API key.
Access to the DC GIS API (public endpoint).
2. Clone the Repository
bash
Copy code
git clone https://github.com/CALBITO/Final-Project.git
cd Final-Project
3. Create and Activate a Virtual Environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
4. Install Dependencies
bash
Copy code
pip install -r requirements.txt
5. Add Your Google API Key
Create a .env file in the root directory and add your Google API key:

makefile
Copy code
GOOGLE_API_KEY=your-google-api-key
6. Run the Application
bash
Copy code
flask run
Visit the app at: http://127.0.0.1:5000

Application Structure
plaintext
Copy code
.
├── app.py                 # Main application file
├── templates/             # HTML templates
│   ├── index.html         # Home page template
│   └── add_barbershop.html # Form for adding a barbershop
├── static/                # Static assets
│   ├── css/               # CSS files
│   └── js/                # JavaScript files
│   └── images/            # Logo and other images
├── data/                  # Cached data storage
│   └── bbs_data.json      # Local barbershop data
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
Troubleshooting
Google API Key Not Working

Ensure the key is valid and has permissions for Maps JavaScript API and Geocoding API.
Check your .env file for typos.
Data Not Displaying

If API fetching fails, the app will load cached data. Check data/bbs_data.json for valid entries.
Ensure the API endpoint (API_URL) is correct.
Cannot Add Barbershop

Ensure latitude and longitude are valid decimal numbers.
Check for missing fields in the form.
Geolocation Issues

Current Limitation: The search bar and geolocation for addresses beyond the Open Data public API is still under development.
Temporary workaround: Manually add latitude and longitude values for precise mapping.
Logo Image Not Displaying on Live Domain

Issue: The logo image renders correctly locally but not on the live domain.
Possible Fixes:
Verify the logo file is uploaded correctly to the server.
Check the file path in the HTML (src) is relative to the deployment environment.
Ensure correct permissions for the static/images/ directory.
Validate the web server configuration (e.g., Nginx, Apache) to serve static files.
Application Not Starting

Verify all dependencies are installed (pip install -r requirements.txt).
Check for syntax errors or missing environment variables.
Key Updates
Code Enhancements
Centralized validation logic to avoid redundancy.
Simplified API and local data caching logic.
Ensured error handling and data-saving mechanisms are robust.
Optimizations
Reduced unnecessary lines of code while maintaining functionality.
Added checks for directory creation and environment variables during app initialization.
Work in Progress
Enhanced geolocation support for a broader range of addresses.
Refinement of the search bar functionality for improved usability.
Fixing live domain logo rendering issues.
Live Application
You can access the live application at https://final-project-barbershapp.onrender.com.

GitHub Repository
The source code is available on GitHub: https://github.com/CALBITO/Final-Project.
