import csv
import heapq
from termcolor import colored

def dijkstra(graph, start):
    # Initialize distances to all nodes as infinity, except for the start node which has a distance of 0
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Initialize priority queue with start node and its distance
    pq = [(0, start)]
    
    # Initialize empty dictionary to keep track of the previous node in the shortest path
    prev = {}
    
    while pq:
        # Get the node with the smallest distance from the priority queue
        curr_dist, curr_node = heapq.heappop(pq)
        
        # If the current distance is greater than the previously calculated distance to this node, skip it
        if curr_dist > distances[curr_node]:
            continue
        
        # For each neighbor of the current node, calculate the distance to that neighbor through the current node
        for neighbor, dist in graph[curr_node].items():
            new_dist = distances[curr_node] + dist
            
            # If the new distance is smaller than the previously calculated distance to the neighbor, update it
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev[neighbor] = curr_node
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances, prev

file_path = input("Enter the full path of the CSV file: ")
file_name = input("Enter the name of the CSV file: ")
filename = f"{file_path}/{file_name}.csv"


# Load the road index data from a CSV file
graph = {}
with open(filename) as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        start = row[1]
        end = row[2]
        dist = float(row[3])
        
        if start not in graph:
            graph[start] = {}
        graph[start][end] = dist
        
        if end not in graph:
            graph[end] = {}
        graph[end][start] = dist

# Define a function to find the shortest path for a given vehicle and origin/destination
def find_shortest_path(vehicle, origin, destination):
    # Use Dijkstra's algorithm to find the shortest path from the starting node to all other nodes
    distances, prev = dijkstra(graph, str(origin))
    
    # Use the previous node dictionary to reconstruct the shortest path from the ending node to the starting node
    path = []
    curr_node = str(destination)
    while curr_node != str(origin):
        path.append(curr_node)
        curr_node = prev[curr_node]
    path.append(str(origin))
    path.reverse()
    
    # Print the shortest path for the given vehicle
    print(colored(f"Vehicle {vehicle}: {' -> '.join(path)} (distance = {distances[str(destination)]:.2f})", 'blue', attrs=['bold']))

# Get user input for each vehicle's origin and destination
origins = set()
destinations = set()
for vehicle in range(1, 29):
    while True:
        print(f"\nVehicle {vehicle}:")
        origin = int(input("Enter origin Node: "))
        destination = int(input("Enter destination Node: "))
        
        # Check if the origin and destination are already being used by another vehicle
        if (origin, destination) in zip(origins, destinations):
            print("Error: Origin and destination already in use by another vehicle. Please try again.")
        else:
            origins.add(origin)
            destinations.add(destination)
            find_shortest_path(vehicle, origin, destination)
            break
