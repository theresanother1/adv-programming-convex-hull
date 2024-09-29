import numpy as np

def leftmost_point(points):
    return min(points, key=lambda p: (p[0], p[1]))

def orientation(p, q, r):
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])


#######################################################################################################
# A way to optimze the algorithm by using filtering methodes to filter the points before been used
# But seems they are often to strict and not very usefull in this case
# Filtering by distance, quadratic filtering etc. are been tested

# def calculate_max_distance(points, percentage=0.1):

#     # Berechne die Ausdehnung des Punktbereichs
#     x_min, y_min = np.min(points, axis=0)
#     x_max, y_max = np.max(points, axis=0)
    
#     # Berechne die Diagonale des Bereichs
#     diagonal = np.sqrt((x_max - x_min) ** 2 + (y_max - y_min) ** 2)
    
#     # Setze max_distance auf einen Prozentsatz der Diagonalen
#     max_distance = percentage * diagonal
#     return max_distance

# def filter_points(current_point, points, max_distance):
#     if current_point is None:
#         raise ValueError("current_point cannot be None")

#     filtered_points = []
#     for point in points:
#         if point is None:
#             continue
#         if np.linalg.norm(point - current_point) <= max_distance:
#             filtered_points.append(point)
#     return np.array(filtered_points)

##########################################################################################################

def gift_wrapping_algorithm(points):

    # Todo: füg den ersten punkt noch als letzten punkt ein, damit die hülle komplett ist
    # Checking if the Array is empty
    if points.size == 0:
        raise ValueError("The point cloud is empty")
    
    convex_hull = []
    start = leftmost_point(points)
    point_on_hull = start

    # See the information above about filtering points 
    # max_distance = calculate_max_distance(points, percentage=0.1)

    while True:
        convex_hull.append(point_on_hull)
        next_point = None
        
        # See the information above about filtering points 
        # filtered_points = filter_points(point_on_hull, points, max_distance) 
        # if len(filtered_points) == 0:
        #     raise ValueError("Keine Punkte nach der Filterung gefunden. Prüfe die Filterkriterien.")

        for point in points:
            if np.array_equal(point, point_on_hull):
                continue
        
            if next_point is None:
                next_point = point
                continue
            
            # Cross product is been used to optimize the orientation of this alogrithm 
            cross_product = orientation(point_on_hull, next_point, point)
            if cross_product > 0 or (cross_product == 0 and np.linalg.norm(point - point_on_hull) > np.linalg.norm(next_point - point_on_hull)):
                next_point = point

        # Checking if the points are collinear 
        if next_point is None:
            print("All points could be collinear!")
            break

        point_on_hull = next_point

        if np.array_equal(point_on_hull, start):
            break

    return np.array(convex_hull)
