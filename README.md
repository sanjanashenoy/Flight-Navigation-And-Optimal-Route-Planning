# Flight-Navigation-And-Optimal-Route-Planning

An optimal route planning navigation system for flights.

## Overview

This project provides a system for planning optimal flight routes based on various factors such as cost, weather conditions, and predicted delays. It includes a web interface for users to input their origin and destination airports and receive the best route information.

## Project Structure

- **templates/index.html**: The HTML file for the web interface.
- **data_preparation.py**: Data is cleaned.
- **insert_data**: Data is inserted into the PostgreSQL database.
- **app.py**: The main application code to run the server.
- **cleaned_routes.csv**: Dataset containing cleaned route information.
- **cleaned_routes_with_predicted_delay.csv**: Dataset containing routes with predicted delays.
- **Flight_delay.csv**: Dataset containing weather information for airports.

## Getting Started

1. **Database Connection:**
   - Follow the instructions in `Guide for Route Optimisation.docx` to connect the project files to your database.
   
2. **File Placement:**
   - Ensure all files are within the same directory as the main code files. The `index.html` file should be within the `templates` folder.
   - The datasets (`cleaned_routes.csv`, `cleaned_routes_with_predicted_delay.csv`, and `Flight_delay.csv`) should not be placed inside a `datasets` folder but should be in the same directory as the main code files.

## To Run The Application

1. python data_preparation.py
2. python insert_data.py
3. Run the application: python app.py
   

## Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Enter the origin and destination airports in the provided fields.
3. Submit the form to get the optimal route, weather information, and predicted delays.

## Notes

- The datasets have been zipped for convenience but should be extracted and placed in the correct directory as mentioned above.
