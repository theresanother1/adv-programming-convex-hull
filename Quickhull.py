import numpy as np
import helpers


def quick_hull(points: np.ndarray):
    convex_hull = []
    if points.size == 0:
        return convex_hull

    minmax = get_min_max_starters(points)

    if minmax is None:
        return convex_hull

    left, right = minmax[0, :], minmax[1, :]
    hull_part1 = find_points_left_to_line(left, right, points)
    # find points to the other side
    hull_part2 = find_points_left_to_line(right, left, points)

    convex_hull.extend(find_hull(hull_part1, left, right))
    convex_hull.extend(find_hull(hull_part2, right, left))

    return convex_hull


def find_hull(points: np.ndarray, left: np.ndarray, right: np.ndarray):
    convex_hull = []
    if points.size == 0:
        return convex_hull
    else:
        max_dist, max_point_to_line = get_max_dist_and_point(left, right, points)

        hull_part1 = find_points_left_to_line(left, max_point_to_line, points)
        hull_part2 = find_points_left_to_line(max_point_to_line, right, points)

        convex_hull.extend([left])
        convex_hull.extend(find_hull(hull_part1, left, max_point_to_line))
        convex_hull.extend([max_point_to_line])
        convex_hull.extend(find_hull(hull_part2, max_point_to_line, right))
        convex_hull.extend([right])

        return convex_hull


def quick_hull_step_through(points: np.ndarray) -> (np.ndarray, dict, dict):
    convex_hull = []
    if points.size == 0:
        return convex_hull

    minmax = get_min_max_starters(points)

    # points are on a line
    if minmax is None:
        return convex_hull

    left, right = minmax[0, :], minmax[1, :]

    # initialise dicts for step tracing
    upper = {}
    lower = {}
    step_lower = 0
    step_upper = 0
    upper[step_upper] = minmax
    lower[step_lower] = minmax
    step_lower += 1
    step_upper += 1

    hull_part1 = find_points_left_to_line(left, right, points)
    # find points to the other side
    hull_part2 = find_points_left_to_line(right, left, points)

    convex_hull.extend(find_hull_step_through(hull_part1, left, right, upper, left, right, step_upper, []))
    convex_hull.extend(find_hull_step_through(hull_part2, right, left, lower, right, left, step_lower, []))

    return convex_hull, upper, lower


def find_hull_step_through(points: np.ndarray, left: np.ndarray, right: np.ndarray, steps, min, max, step, upper):
    convex_hull = []
    if points.size == 0:
        return convex_hull
    else:
        max_dist, max_point_to_line = get_max_dist_and_point(left, right, points)

        hull_part1 = find_points_left_to_line(left, max_point_to_line, points)
        hull_part2 = find_points_left_to_line(max_point_to_line, right, points)

        step_new = step + 1

        array = []

        # add current step to steps
        array.extend([left])
        array.extend([max_point_to_line])
        array.extend([right])
        steps[step] = array

        convex_hull.extend([left])
        convex_hull.extend(
            find_hull_step_through(hull_part1, left, max_point_to_line, steps, min, max, step_new, True))
        convex_hull.extend([max_point_to_line])

        # increase step so all steps are added to steps
        step_new = step_new + 1

        convex_hull.extend(
            find_hull_step_through(hull_part2, max_point_to_line, right, steps, min, max, step_new, False))
        convex_hull.extend([right])

        return convex_hull


def get_min_max_starters(points: np.ndarray):
    isLine = helpers.all_points_on_line(points[:, 0], points[:, 1])
    if isLine:
        return None
    else:
        min_index = np.argmin(points[:, 0])
        max_index = np.argmax(points[:, 0])
        return np.array([[points[min_index, 0], points[min_index, 1]], [points[max_index, 0], points[max_index, 1]]])


def is_left(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> bool:
    # Where a = line point 1; b = line point 2; c = point to check against
    # result == 0 -> colinear, result > -threshold = left, < -threshold = right

    # do not return point itself --> due to threshold == 0
    if np.all(a == c) or np.all(b == c):
        return False

    ab = b - a
    ac = c - a

    # use threshold due to rounding errors --> if slightly less than zero, considered left
    threshold = 1e-9
    if np.cross(ab, ac) >= -threshold:
        return True
    else:
        return False


def find_points_left_to_line(a: np.ndarray, b: np.ndarray, points: np.ndarray):
    return points[np.apply_along_axis(lambda p: is_left(a, b, p), 1, points)]


def get_max_dist_and_point(a: np.ndarray, b: np.ndarray, left_points: np.ndarray):
    # Calculate distances for left points
    distances = np.array([find_distance(a, b, p) for p in left_points])

    # Find the maximum distance and the corresponding point
    max_dis = np.max(distances)
    furthest_point = left_points[np.argmax(distances)]
    return max_dis, furthest_point


def find_distance(a: np.ndarray, b: np.ndarray, p: np.ndarray) -> float:
    ab = b - a
    ap = p - a
    distance = np.abs(np.cross(ab, ap)) / np.linalg.norm(ab)
    return distance


def get_quickhull_step_results(points):
    quickhull_hull, steps_quickhull_upper, steps_quickhull_lower = quick_hull_step_through(points)
    steps_quickhull_upper = dict(sorted(steps_quickhull_upper.items()))
    steps_quickhull_lower = dict(sorted(steps_quickhull_lower.items()))
    list_results = []
    list_results.extend(steps_quickhull_upper.values())
    list_results.extend(steps_quickhull_lower.values())
    return list_results