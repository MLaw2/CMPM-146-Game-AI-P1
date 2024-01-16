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
    print(source_point)
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

def breadth_first_search (start_box, goal_box, boxes, adj_boxes, boxes_visited):
    queue = [start_box]
    while queue: # queue and process
        current_box = pop(queue)
        if current_box == goal_box: # success test
            print("we found the thing")
            # return path_to(goal, graph)
        else:
            for new in adj_boxes (current_box, boxes): # generate successors
                # for each box we put into the list of boxes visited
                # it's not a list, it's a dictionary
                # when we explore a box, we add it as a key to the dictionary, and the value is the previous box we visited from
                # thus if a box does not have a value in the dictionary, or simply does not exist, we understand that the box is new.
                if new.prev == None: # haven’t been here before
                    new.prev = current_node # so set the backpointer
                    append_to(queue, new) # add to END of queue
        return(Failure) # can’t get there from here
