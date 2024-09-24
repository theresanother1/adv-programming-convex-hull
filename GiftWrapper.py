import numpy as np

def leftmost_point(points):
    
    leftmost = points[0]
    for point in points:
        if point[0] < leftmost[0] or (point[0] == leftmost[0] and point[1] < leftmost[1]):
            leftmost = point
    return leftmost

def orientation(p, q, r):
   
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # kollinear
    elif val > 0:
        return 1  # im Uhrzeigersinn
    else:
        return -1  # gegen den Uhrzeigersinn

def gift_wrapping_algorithm(points):
    
    convex_hull = []
    start = leftmost_point(points)
    point_on_hull = start

    while True:
        convex_hull.append(point_on_hull)
        next_point = points[0]  
        for point in points:
            if np.array_equal(point, point_on_hull):
                continue
            
            if np.array_equal(next_point, point_on_hull) or orientation(point_on_hull, next_point, point) == -1:
                next_point = point

        point_on_hull = next_point

        
        if np.array_equal(point_on_hull, start):
            break

    return np.array(convex_hull)
