import time
import numpy as np
import graphics as graphics
import Simple_View


def get_min_max(points: np.ndarray):
    return points[np.argmin(points[:, 0])], points[np.argmax(points[:, 0])]


def convex_hull_visu(points, win):
    convexHull = np.array([])

    # find left-most and right-most points and add to result
    leftPoint, rightPoint = get_min_max(points)

    # print(leftPoint)
    convexHull = np.append(convexHull, leftPoint)
    convexHull = np.append(convexHull, rightPoint)

    # display/highlight points to yellow color using highlightPoint() function and join both points with a line

    Simple_View.highlight_point(leftPoint, win)
    Simple_View.highlight_point(rightPoint, win)
    Simple_View.join_points(leftPoint, rightPoint).draw(win)

    # call upperHull algorithm for upper part of convex hull
    allPointsUpper = sub_hull_visu(leftPoint, rightPoint, points, win)

    # call upperHull algorithm for lower part of convex hull (lower hull)
    allPointsLower = sub_hull_visu(rightPoint, leftPoint, points, win)

    # create final result array
    convexHull = np.append(convexHull, allPointsUpper)
    convexHull = np.append(convexHull, allPointsLower)
    convexHull = convexHull.reshape(-1, 2)

    # close graphics window at the end
    if win.isClosed():
        print("win closed")
        print("convexHull is ")
        print(convexHull)
        return
    else:
        try:
            win.getMouse()
            win.close()
        except graphics.GraphicsError as e:
            print(e)
            return

    return convexHull


def sub_hull_visu(a: np.ndarray, b: np.ndarray, points: np.ndarray, win) -> np.ndarray:
    # base case for when there are no points to the left of selected vector
    if points.size == 0:
        return np.array([])

    furthestPoint = np.array([])
    resultPoints = np.array([])

    # Filter points that are to the left of the line segment
    upperHullPoints = points[np.apply_along_axis(lambda p: is_left(a, b, p), 1, points)]

    # find p farthest from the line
    if upperHullPoints.size != 0:
        maxDis, furthestPoint = get_max_dist_and_point(a, b, upperHullPoints)
        print("maxDis = ", maxDis)
        print("Furthest Point is ", furthestPoint)

    # add the furthest point to convexHull result
    if furthestPoint.size != 0:
        resultPoints = np.append(resultPoints, furthestPoint)
        Simple_View.highlight_point(furthestPoint, win)
        Simple_View.join_points(a, furthestPoint).draw(win)
        Simple_View.join_points(b, furthestPoint).draw(win)

    # calling upperHull algorithm on region 1 (left of vector a, furthestPoint) and region 3 (left of vector furthestPoint, b)
    region1 = sub_hull_visu(a, furthestPoint, upperHullPoints, win)
    region3 = sub_hull_visu(furthestPoint, b, upperHullPoints, win)

    # create final result array
    resultPoints = np.append(resultPoints, region1)
    resultPoints = np.append(resultPoints, region3)

    # sleep function to slow down convexHull building to visualize for graphics value -> enable to slow down graphics viz and see step-by-step calculation
    time.sleep(Simple_View.SLOWDOWN_PER_STEP)
    return resultPoints


def convex_hull_fast(points):
    convexHull = np.array([])

    # find left-most and right-most points and add to result
    leftPoint, rightPoint = get_min_max(points)

    convexHull = np.append(convexHull, leftPoint)
    convexHull = np.append(convexHull, rightPoint)

    # call upperHull algorithm for upper part of convex hull
    allPointsUpper = sub_hull_fast(leftPoint, rightPoint, points)

    # call upperHull algorithm for lower part of convex hull (lower hull)
    allPointsLower = sub_hull_fast(rightPoint, leftPoint, points)

    # create final result array
    convexHull = np.append(convexHull, allPointsUpper)
    convexHull = np.append(convexHull, allPointsLower)
    convexHull = convexHull.reshape(-1, 2)
    return convexHull


def sub_hull_fast(a: np.ndarray, b: np.ndarray, points: np.ndarray) -> np.ndarray:
    # base case for when there are no points to the left of selected vector
    if points.size == 0:
        return np.array([])

    furthestPoint = np.array([])
    resultPoints = np.array([])

    # Filter points that are to the left of the line segment
    upperHullPoints = points[np.apply_along_axis(lambda p: is_left(a, b, p), 1, points)]

    # find p farthest from the line
    if upperHullPoints.size != 0:
        maxDis, furthestPoint = get_max_dist_and_point(a, b, upperHullPoints)

    # add the furthest point to convexHull result
    if furthestPoint.size != 0:
        resultPoints = np.append(resultPoints, furthestPoint)

    # calling upperHull algorithm on region 1 (left of vector a, furthestPoint) and region 3 (left of vector furthestPoint, b)
    region1 = sub_hull_fast(a, furthestPoint, upperHullPoints)
    region3 = sub_hull_fast(furthestPoint, b, upperHullPoints)

    # create final result array
    resultPoints = np.append(resultPoints, region1)
    resultPoints = np.append(resultPoints, region3)

    return resultPoints


# Geometric Calculation Functions
def find_distance(a: np.ndarray, b: np.ndarray, p: np.ndarray) -> float:
    ab = b - a
    ap = p - a
    distance = np.abs(np.cross(ab, ap)) / np.linalg.norm(ab)
    return distance


def is_left(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> bool:
    ab = b - a
    ac = c - a

    # calculate cross product --> if > 0 --> is left
    return np.cross(ab, ac) > 0


def get_max_dist_and_point(a: np.ndarray, b: np.ndarray, left_points: np.ndarray):
    # Calculate distances for left points
    distances = np.array([find_distance(a, b, p) for p in left_points])

    # Find the maximum distance and the corresponding point
    max_dis = np.max(distances)
    furthest_point = left_points[np.argmax(distances)]
    return max_dis, furthest_point
