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
    box_path, boxes = breadth_first_search(mesh.get("adj"),source_box,dest_box)
    path = points_from_boxes(box_path,source_point,destination_point)
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

# def breadth_first_search (start_box, goal_box, boxes, adj_boxes, boxes_visited):
#     visited = []
#     queue = [start_box]
#     while queue: # queue and process
#         current_box = pop(queue)
#         if current_box == goal_box: # success test
#             print("we found the thing")
#             # return path_to(goal, graph)
#         else:
#             for new in adj_boxes(current_box, boxes): # generate successors
#                 # for each box we put into the list of boxes visited
#                 # it's not a list, it's a dictionary
#                 # when we explore a box, we add it as a key to the dictionary, and the value is the previous box we visited from
#                 # thus if a box does not have a value in the dictionary, or simply does not exist, we understand that the box is new.
#                 if new.prev == None: # haven’t been here before
#                     new.prev = current_node # so set the backpointer
#                     append_to(queue, new) # add to END of queue
#         return(Failure) # can’t get there from here

def breadth_first_search(mesh, start_box, end_box):
    # Check if start and end boxes are valid
    print(start_box,end_box)
    if start_box not in mesh or end_box not in mesh:
        return "Invalid start or end box"

    # Initialize a queue for BFS
    queue = [start_box]
    # Keep track of visited boxes to avoid loops
    all_seen = {}
    all_seen[start_box] = mesh.get(start_box)

    # Dictionary to store the path: key is the current box, value is the previous box
    path = {start_box: None}

    while queue:
        current_box = queue.pop()

        # Check if the current box is the end box
        if current_box == end_box:
            # Reconstruct the path from end to start
            result_path = []
            while current_box is not None:
                result_path.insert(0, current_box)
                current_box = path[current_box]
            return result_path, all_seen

        # Explore neighbors of the current box
        for neighbor_box in mesh[current_box]:
            if neighbor_box not in all_seen:
                # all_seen[neighbor_box] = mesh.get(neighbor_box)
                all_seen[neighbor_box] = current_box
                queue.append(neighbor_box)
                path[neighbor_box] = current_box

    # If no path is found
    return "No path found"

# def dijkstras_algorithm(mesh, start_box, end_box):
#     # Check if start and end boxes are valid
#     if start_box not in mesh or end_box not in mesh:
#         return "Invalid start or end box"
    
#     # Priority queue to store boxes with their distances
#     priority_queue = [(0, start_box)]
    
#     # Dictionary to store the distance to each box
#     distances = {box: float('inf') for box in mesh}
#     distances[start_box] = 0
    
#     # Dictionary to store the path: key is the current box, value is the previous box
#     path = {start_box: None}
    
#     while priority_queue:
#         current_distance, current_box = heapq.heappop(priority_queue)
        
#         # Check if the current box is the end box
#         if current_box == end_box:
#             # Reconstruct the path from end to start
#             result_path = []
#             while current_box is not None:
#                 result_path.insert(0, current_box)
#                 current_box = path[current_box]
#             return result_path
        
#         # Update distances and explore neighbors
#         for neighbor_box in mesh[current_box]:
#             new_distance = current_distance + 1  # Assuming unit distance between neighboring boxes
            
#             if new_distance < distances[neighbor_box]:
#                 distances[neighbor_box] = new_distance
#                 heapq.heappush(priority_queue, (new_distance, neighbor_box))
#                 path[neighbor_box] = current_box
    
#     # If no path is found
#     return "No path found"

def points_from_boxes(boxes,start,end):
    points = [start]
    for box in boxes:
        points.append(get_closest_point(points[-1],box))
    points[0] = start
    points[-1] = end
    return points

def get_hp(point1,point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_closest_point(old_point, next_box):
    x_min, x_max, y_min, y_max = next_box

    new_point = [next_box[0], next_box[1]]
    new_points = [[next_box[0], next_box[2]], [next_box[0], next_box[3]],
                  [next_box[1], next_box[2]], [next_box[1], next_box[3]]]

    current_hp = get_hp(old_point,new_point)

    for point in new_points:
        if x_min <= point[0] <= x_max and y_min <= point[1] <= y_max:
            distance = get_hp(old_point,point)
            if distance < current_hp:
                new_point = point
                current_hp = distance
    return new_point