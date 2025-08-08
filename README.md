# ✈️ Flight Route Planning System Using Best-First Search

## Overview
This project is a visually appealing and interactive Flight Route Planner for India, built using Python's Tkinter for GUI and Folium for map visualization. It uses the Best-First Search algorithm with a custom heuristic to find optimal flight paths between major Indian airports, considering multiple attributes like distance, fuel, time, capacity, and safety.

---

## Features
- **Modern GUI:** Elegant, dark-themed interface with dropdowns and buttons for easy route selection.
- **Interactive Map:** Visualizes the selected route and all possible connections on a map of India, with cost annotations.
- **Multi-Attribute Routing:** Calculates route cost using weighted factors (distance, fuel, time, capacity, safety).
- **Best-First Search Algorithm:** Efficiently finds the best route using a heuristic based on real-world coordinates.
- **Error Handling:** User-friendly messages for invalid selections or unreachable routes.

---

## Technologies Used
- **Python 3**
- **Tkinter** (GUI)
- **Folium** (Map Visualization)
- **Webbrowser** (Map Display)
- **Heapq, Math** (Algorithm)

---

## Airports Supported
- Delhi (DEL)
- Mumbai (BOM)
- Bengaluru (BLR)
- Chennai (MAA)
- Kolkata (CCU)

---

## How It Works
1. **Select Start and Destination Airports** from the dropdown menus.
2. **Click "Find Route"** to compute the optimal path using Best-First Search.
3. **View Results:**
   - The route and estimated cost are displayed in the GUI.
   - An interactive map opens in your browser, showing the route and all connections with cost details.
4. **Reset** to plan a new route.

---

## Screenshots
![GUI Screenshot](https://user-images.githubusercontent.com/your-username/your-repo/main/screenshots/gui.png)
![Map Screenshot](https://user-images.githubusercontent.com/your-username/your-repo/main/screenshots/map.png)

---

## Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone https://github.com/hitesh-boldra/Flight-Route-Planning-System-Using-Best-First-Search.git
   cd Flight-Route-Planning-System-Using-Best-First-Search
   ```
2. **Install dependencies:**
   ```bash
   pip install folium
   ```
3. **Run the application:**
   ```bash
   python c2p2.py
   ```

---

## Customization
- You can add more airports and routes by updating the `airport_coordinates`, `airports`, and `route_attributes` dictionaries in `c2p2.py`.
- Adjust the cost weights in `calculate_cost()` for different optimization strategies.

---

## License
This project is licensed under the MIT License.

---

## Author
- **Hitesh Boldra**

---

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Acknowledgements
- Python, Tkinter, Folium
- Open-source community

---

## Contact
For any queries, reach out via [GitHub Issues](https://github.com/hitesh-boldra/Flight-Route-Planning-System-Using-Best-First-Search/issues).
