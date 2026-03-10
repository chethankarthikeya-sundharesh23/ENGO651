# Calgary Building Permits Map

## Overview

This project is a web application that visualizes building permit data from the City of Calgary on an interactive map. Users can search for permits issued within a selected date range, and the results are displayed as clustered markers on the map.

The application uses a Python Flask backend to fetch data from the Calgary Open Data API and a JavaScript frontend with Leaflet.js to render the map.

In **Lab 4**, the application was extended by integrating a **Mapbox styled vector tileset layer** representing Calgary Traffic Incidents (2017). This layer can be toggled on and off by the user and demonstrates how Mapbox Studio can be used to design and publish custom map styles that can be integrated into a web mapping application.

---

## Features

* Interactive map displaying Calgary building permits
* Date range search for filtering permits
* Marker clustering for better visualization of large datasets
* Loading spinner while data is being fetched
* Error handling when no permits are found
* Secure handling of API keys (not stored in the source code)
* Toggleable **Traffic Incidents 2017** layer designed in Mapbox Studio
* Integration of **Mapbox vector tiles** into a Leaflet web map

---

## Technologies Used

* **Python**
* **Flask**
* **JavaScript**
* **Leaflet.js**
* **Mapbox Studio**
* **HTML / CSS**
* **Calgary Open Data API**

---

## Data Sources

### Building Permits

Building permit data is retrieved from the City of Calgary Open Data Portal.

Dataset:
https://data.calgary.ca/resource/c2es-76ed.geojson

### Traffic Incidents (2017)

Traffic incident data used for the Mapbox styled layer.

Dataset:
https://data.calgary.ca/

This dataset was uploaded to **Mapbox Studio**, converted to a **vector tileset**, and styled as a map layer.

---

## Mapbox Layer (Lab 4)

The Traffic Incidents dataset was uploaded to Mapbox Studio and converted into a vector tileset. A custom style was created to visualize traffic incidents as circular markers.

Design choices include:

* **Red circle markers** to represent traffic incidents and hazards
* **Zoom-dependent radius** to reduce clutter at smaller scales and improve visibility at larger scales
* **Slight blur and opacity adjustments** to soften overlapping points
* Integration of the styled layer into the Leaflet web application as a toggleable overlay

Users can enable or disable the Traffic Incidents layer using the **Leaflet layer control**.

---

## Project Structure

```
project-folder
│
├── app.py
│
├── templates
│   └── index.html
│
├── static
│   ├── script.js
│   └── style.css
│
└── README.md
```

---

## Installation and Setup

### 1. Clone the repository

```
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2. Install dependencies

```
pip install flask requests
```

### 3. Add API keys

Create the following files in the root directory:

`api_key.txt`

```
YOUR_API_KEY_ID
```

`api_key_secret.txt`

```
YOUR_API_KEY_SECRET
```

These files are ignored by Git to keep the keys secure.

---

### 4. Run the application

```
python app.py
```

---

### 5. Open the application

Open your browser and go to:

```
http://127.0.0.1:5000
```

---

## How to Use

1. Select a **start date** and **end date**.
2. Click **Search**.
3. The map will display building permits issued during that date range.
4. Markers will automatically cluster when zoomed out.
5. Use the **layer control** on the map to toggle the **Traffic Incidents 2017** layer on or off.

---

## Notes

* If no permits exist for the selected date range, an error message will be displayed.
* Large datasets are limited to 500 results per request to maintain performance.
* The traffic incident layer is hosted using **Mapbox vector tiles**, which allows efficient rendering of large spatial datasets.
