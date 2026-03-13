# ENGO 651 – Lab 6: Line Simplification Web Map

## Overview

This project implements a web-based mapping application that demonstrates **polyline simplification** using the Turf.js library. The application allows a user to draw a polyline on a map and generate a simplified version of that line. The simplified line contains fewer vertices while maintaining the general shape of the original geometry.

The goal of this lab is to gain experience using **client-side geospatial analysis tools** in a web mapping environment.

---

## Features

* Interactive web map
* Draw a polyline directly on the map
* Simplify the drawn polyline using Turf.js
* Display the simplified line in a different colour
* Display the number of vertices in the original and simplified lines
* Clear the map and draw a new polyline

---

## Technologies Used

* **Leaflet.js** – interactive web mapping library
* **Leaflet Draw** – drawing tools for Leaflet
* **Turf.js** – JavaScript geospatial analysis library
* **HTML, CSS, JavaScript**

---

## How It Works

1. The user draws a polyline on the map using the drawing toolbar.
2. When the **Simplify** button is clicked:

   * The polyline is converted to GeoJSON.
   * The Turf.js `simplify()` function is applied.
   * A simplified polyline is generated with fewer vertices.
3. The simplified polyline is displayed in **red** on the map.
4. The application displays the number of vertices in:

   * the original polyline
   * the simplified polyline
5. The **Clear** button removes all lines from the map and allows the user to draw a new polyline.

---


## Example Workflow

1. Open the map.
2. Use the **polyline tool** to draw a line.
3. Click **Simplify** to generate a simplified version.
4. Compare the vertex counts displayed in the control panel.
5. Click **Clear** to remove the lines and draw a new one.

