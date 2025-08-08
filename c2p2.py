import tkinter as tk
from tkinter import ttk, messagebox
import folium
import webbrowser
import heapq
import math

# Coordinates of airports
airport_coordinates = {
    'DEL': (28.61, 77.21),
    'BOM': (19.09, 72.87),
    'BLR': (13.20, 77.71),
    'MAA': (13.01, 80.23),
    'CCU': (22.57, 88.36),
}

# Distance and connections
airports = {
    'DEL': {'BOM': 1400, 'BLR': 2150, 'MAA': 2200, 'CCU': 1500},
    'BOM': {'DEL': 1400, 'BLR': 980, 'MAA': 1030, 'CCU': 1660},
    'BLR': {'DEL': 2150, 'BOM': 980, 'MAA': 290, 'CCU': 1870},
    'MAA': {'DEL': 2200, 'BOM': 1030, 'BLR': 290, 'CCU': 1670},
    'CCU': {'DEL': 1500, 'BOM': 1660, 'BLR': 1870, 'MAA': 1670},
}

# Flight attributes
route_attributes = {
    ('DEL', 'BOM'): {'fuel': 5, 'time': 2, 'capacity': 1, 'safety': 1},
    ('DEL', 'BLR'): {'fuel': 8, 'time': 3.5, 'capacity': 2, 'safety': 2},
    ('DEL', 'MAA'): {'fuel': 9, 'time': 4, 'capacity': 3, 'safety': 1},
    ('DEL', 'CCU'): {'fuel': 6, 'time': 2.5, 'capacity': 1, 'safety': 1},
    ('BOM', 'BLR'): {'fuel': 3, 'time': 1.5, 'capacity': 1, 'safety': 1},
    ('BOM', 'MAA'): {'fuel': 4, 'time': 1.8, 'capacity': 2, 'safety': 1},
    ('BOM', 'CCU'): {'fuel': 7, 'time': 3, 'capacity': 2, 'safety': 2},
    ('BLR', 'MAA'): {'fuel': 1, 'time': 0.8, 'capacity': 1, 'safety': 1},
    ('BLR', 'CCU'): {'fuel': 6, 'time': 3.2, 'capacity': 3, 'safety': 2},
    ('MAA', 'CCU'): {'fuel': 6, 'time': 3, 'capacity': 2, 'safety': 1},
}

# Haversine for heuristic
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def heuristic(current, goal):
    lat1, lon1 = airport_coordinates[current]
    lat2, lon2 = airport_coordinates[goal]
    return haversine_distance(lat1, lon1, lat2, lon2)

# Weighted cost calculation
def calculate_cost(start, end):
    distance = airports[start][end]
    attr = route_attributes.get((start, end), route_attributes.get((end, start), {}))
    return (
        0.4 * distance +
        0.2 * attr.get('fuel', 1) * 100 +
        0.2 * attr.get('time', 1) * 60 +
        0.1 * attr.get('capacity', 1) * 50 +
        0.1 * attr.get('safety', 1) * 30
    )


    # Simplified weighted formula
    return (
        0.5 * distance +   # 50% weight to distance
        0.3 * fuel +       # 30% weight to fuel
        0.2 * time         # 20% weight to time
    )


def reconstruct_path(path, goal):
    route = []
    while goal is not None:
        route.append(goal)
        goal = path[goal]
    return list(reversed(route))

# Best-First Search with heuristic
def best_first_search(start, goal):
    queue = [(heuristic(start, goal), start)]
    visited = set()
    path = {start: None}
    cost_so_far = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)
        if current == goal:
            return reconstruct_path(path, goal), cost_so_far[goal], cost_so_far[goal] + heuristic(current, goal)

        if current in visited:
            continue
        visited.add(current)

        for neighbor in airports[current]:
            step_cost = calculate_cost(current, neighbor)
            new_cost = cost_so_far[current] + step_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(queue, (heuristic(neighbor, goal), neighbor))
                path[neighbor] = current

    return None, 0, 0

# GUI class
class FlightRoutePlanner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flight Route Planner")
        self.geometry("520x400")
        self.configure(bg="black")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Custom.TCombobox", fieldbackground="black", background="black", foreground="black", arrowcolor="back")
        self.style.configure("Rounded.TButton", font=("Segoe UI", 11, "bold"), padding=8, background="black", foreground="white")
        self.style.map("Rounded.TButton", background=[("active", "#48a999")])

        tk.Label(self, text="✈ Flight Route Planner ✈", font=("Segoe UI", 20, "bold"), fg="#33ccff", bg="black").pack(pady=20)

        frame = tk.Frame(self, bg="black")
        frame.pack(pady=10)

        tk.Label(frame, text="Start Airport:", font=("Segoe UI", 12), bg="black", fg="white").grid(row=0, column=0, padx=10, pady=10)
        self.start_var = tk.StringVar(value="Select")
        self.start_combo = ttk.Combobox(frame, textvariable=self.start_var, values=list(airports.keys()), state="readonly", width=18, style="Custom.TCombobox")
        self.start_combo.grid(row=0, column=1)

        tk.Label(frame, text="Destination Airport:", font=("Segoe UI", 12), bg="black", fg="white").grid(row=1, column=0, padx=10, pady=10)
        self.goal_var = tk.StringVar(value="Select")
        self.goal_combo = ttk.Combobox(frame, textvariable=self.goal_var, values=list(airports.keys()), state="readonly", width=18, style="Custom.TCombobox")
        self.goal_combo.grid(row=1, column=1)

        button_frame = tk.Frame(self, bg="black")
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="🚀 Find Route", command=self.find_route, style="Rounded.TButton").grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="🔄 Reset", command=self.reset, style="Rounded.TButton").grid(row=0, column=1, padx=10)

        self.result_label = tk.Label(self, text="", font=("Segoe UI", 11), bg="black", fg="lightgreen")
        self.result_label.pack(pady=10)

    def find_route(self):
        start, goal = self.start_var.get(), self.goal_var.get()
        if start not in airports or goal not in airports or start == goal or start == "Select" or goal == "Select":
            messagebox.showerror("Input Error", "Please select two different airports.")
            return
        route, g_cost, f_cost = best_first_search(start, goal)
        if route:
            self.result_label.config(text=f"Route: {' ➜ '.join(route)}\nEstimated Cost: ₹{int(f_cost)}")
            self.show_route_on_map(route)
        else:
            messagebox.showerror("Route Not Found", "No valid route found.")

    def reset(self):
        self.start_combo.set("Select")
        self.goal_combo.set("Select")
        self.result_label.config(text="")

    def show_route_on_map(self, route):
        india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

        for airport, coords in airport_coordinates.items():
            folium.Marker(coords, popup=airport, icon=folium.Icon(color='blue', icon='plane', prefix='fa')).add_to(india_map)

        for i in range(len(route) - 1):
            start_coords, end_coords = airport_coordinates[route[i]], airport_coordinates[route[i + 1]]
            folium.PolyLine([start_coords, end_coords], color="blue", weight=2.5).add_to(india_map)

        for start in airports:
            for end in airports[start]:
                coords_start, coords_end = airport_coordinates[start], airport_coordinates[end]
                cost = int(calculate_cost(start, end))
                folium.PolyLine([coords_start, coords_end], color="red", weight=1.5, opacity=0.6).add_to(india_map)
                midpoint = [(coords_start[0] + coords_end[0]) / 2, (coords_start[1] + coords_end[1]) / 2]
                folium.Marker(midpoint, popup=f"Cost: ₹{cost}", icon=folium.Icon(color='green')).add_to(india_map)

        india_map.save("flight_route_india_with_costs.html")
        webbrowser.open("flight_route_india_with_costs.html")


# Run
if __name__ == "__main__":
    FlightRoutePlanner().mainloop()
