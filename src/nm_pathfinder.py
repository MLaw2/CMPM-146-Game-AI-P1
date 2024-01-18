import heapq
import math
def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    path = []

    boxes = {}

    #search(source_point, destination_point, mesh)
    #print(source_point)
    #print(destination_point)
    #print(mesh.get("adj"))
    # print(source_point)
    source_box = get_box_for_point(source_point,mesh.get("boxes"))
    dest_box = get_box_for_point(destination_point,mesh.get("boxes"))
    box_path, boxes = dijkstras_algorithm(mesh.get("adj"),source_box,dest_box)
    
    #path = points_from_boxes(box_path,source_point,destination_point)
    path = make_path(box_path, source_point, destination_point)
    
    # print(path)
    #print(source_point)
    return path, boxes.keys()

# BOX FORMAT: (x1, x2, y1, y2)
# BOX FORMAT: ( 0,  1,  2,  3)
# x1 is Left Edge
# x2 is Right Edge
# y1 is Upper Edge
# y2 is Lower Edge
#points are a1 and b1

def get_box_for_point(point,boxes):
    for box in boxes:
        if box[0] < point[0] and box[1] > point[0]:
            if box[2] < point[1] and box[3] > point[1]:
                return box

def dijkstras_algorithm(mesh, start_box, end_box):
    # Check if start and end boxes are valid
    if start_box not in mesh or end_box not in mesh:
        return "Invalid start or end box"
    
    # Priority queue to store boxes with their distances
    priority_queue = [(0, start_box)]
    visited_boxes = {}
    # Dictionary to store the distance to each box
    distances = {box: float('inf') for box in mesh}
    distances[start_box] = 0
    
    # Dictionary to store the path: key is the current box, value is the previous box
    path = {start_box: None}
    
    while priority_queue:
        current_distance, current_box = heapq.heappop(priority_queue)
        visited_boxes[current_box] = "0"
        # Check if the current box is the end box
        if current_box == end_box:
            # Reconstruct the path from end to start
            result_path = []
            while current_box is not None:
                result_path.insert(0, current_box)
                current_box = path[current_box]
            return result_path, visited_boxes
        
        # Update distances and explore neighbors
        for neighbor_box in mesh[current_box]:
            new_distance = current_distance + 1  # Assuming unit distance between neighboring boxes
            
            if new_distance < distances[neighbor_box]:
                distances[neighbor_box] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor_box))
                path[neighbor_box] = current_box
    
    # If no path is found
    return "No path found"

def calculate_detail_point(point, box1, box2):
    for i in range(4):
        if i <= 1: # x axis
            if box1[i] == box2[0] or box1[i] == box2[1]: # if the x bounds collide
                value_range = find_edge_range(box1[2], box1[3], box2[2], box2[3]) # find the range in y axis
                new_point = (box1[i], find_optimal_value(point[1], value_range))
                return new_point
        elif i >= 2: # y axis
            if box1[i] == box2[2] or box1[i] == box2[3]: # if the y bounds collide
                value_range = find_edge_range(box1[0], box1[1], box2[0], box2[1]) # find the range in x axis
                new_point = (find_optimal_value(point[0], value_range), box1[i])
                return new_point
    print("wtf")
    return

    
def find_optimal_value(value, range):
    if value <= range[0]:
        return range[0]
    if value >= range[1]:
        return range[1]
    else:
        return value
    

def find_edge_range(a1, a2, b1, b2):
    return (max(a1, b1), min(a2, b2))
    
def make_path(boxes, start, end):
    path = []
    current_point = start
    for i in range(len(boxes)):
        path.append(current_point)
        current_box = boxes[i]
        if i < len(boxes) - 1:
            next_box = boxes[i + 1]
            current_point = calculate_detail_point(current_point, current_box, next_box)
    path.append(end)
    return path