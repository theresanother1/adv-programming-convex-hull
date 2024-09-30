import numpy as np

####################################################################
#
#               IMPLEMENTATION QUICKHULL
#
#
# - has a slower version for step tracing
# - faster version for faster execution times


step_upper = 0


# optimized version for faster execution
def quick_hull(points: np.ndarray) -> np.ndarray:
    if points.shape[0] < 3:
        return points

    # Find leftmost and rightmost points
    minmax, left_idx, right_idx = get_min_max_starters(points)

    # if min max is None --> all points are on one line, all points are hull
    if minmax is None:
        return points

    left, right = minmax[0, :], minmax[1, :]

    # Split points into upper and lower sets, initially include all points
    upper_set = np.ones(points.shape[0], dtype=bool)
    lower_set = np.ones(points.shape[0], dtype=bool)

    # do not include left and right point in either set
    upper_set[left_idx] = upper_set[right_idx] = False
    lower_set[left_idx] = lower_set[right_idx] = False

    # include only those points, which are left to line
    upper_set[upper_set] = is_left(left, right, points[upper_set]) > 1e-9
    # include only those points, which are left to line
    lower_set[lower_set] = is_left(right, left, points[lower_set]) > 1e-9

    # find hull points
    hull_upper = find_hull(points, left, right, upper_set)
    hull_lower = find_hull(points, right, left, lower_set)

    # Combine results
    return np.vstack((left, hull_upper, right, hull_lower))


def find_hull(points: np.ndarray, p1: np.ndarray, p2: np.ndarray, point_set: np.ndarray) -> np.ndarray:
    if not np.any(point_set):
        return np.empty((0, 2))

    # Find point with maximum distance
    distances = is_left(p1, p2, points[point_set])
    max_dist_idx = np.argmax(distances)
    max_point = points[point_set][max_dist_idx]

    # do not apply along axis due to introduced overhead
    region_left_to_max = point_set.copy()
    region_max_to_right = point_set.copy()
    region_left_to_max[point_set] = is_left(p1, max_point, points[point_set]) > 1e-9
    region_max_to_right[point_set] = is_left(max_point, p2, points[point_set]) > 1e-9

    # Find hull points
    hull1 = find_hull(points, p1, max_point, region_left_to_max)
    hull2 = find_hull(points, max_point, p2, region_max_to_right)

    # Combine results
    return np.vstack((hull1, max_point, hull2))


def is_left(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.cross(b - a, c - a)


# slower version for step tracing
def quick_hull_step_through(points: np.ndarray) -> (np.ndarray, dict, dict):
    global step_upper
    convex_hull = []
    if points.size == 0:
        return convex_hull

    minmax, min_idx, max_idx = get_min_max_starters(points)

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

    hull_part1, max_val = left_to_line_and_furthest(left, right, points)
    hull_part2, max_val2 = left_to_line_and_furthest(right, left, points)
    convex_hull.extend(find_hull_step_through(hull_part1, left, right, upper, left, right, step_upper, max_val))
    convex_hull.extend(find_hull_step_through(hull_part2, right, left, lower, right, left, step_lower, max_val2))

    return convex_hull, upper, lower


def find_hull_step_through(points: np.ndarray, left: np.ndarray, right: np.ndarray, steps, min, max, step, max_point):
    global step_upper
    convex_hull = []
    if len(points) == 0:
        return convex_hull
    else:
        hull_part1, max_point_new = left_to_line_and_furthest(left, max_point, points)
        hull_part2, max_point2_new = left_to_line_and_furthest(max_point, right, points)

        step_upper = step + 1
        array = []

        # add current step to steps
        print([left], [max_point], [right])
        array.extend([left])
        array.extend([max_point])
        array.extend([right])
        steps[step] = array

        convex_hull.extend([left])
        convex_hull.extend(
            find_hull_step_through(hull_part1, left, max_point, steps, min, max, step_upper, max_point_new))
        convex_hull.extend([max_point])

        # increase step so all steps are added to steps
        step_upper = step_upper + 1
        convex_hull.extend(
            find_hull_step_through(hull_part2, max_point, right, steps, min, max, step_upper, max_point2_new))
        convex_hull.extend([right])

        return convex_hull


def all_points_on_h_or_v_line(x: np.ndarray, y: np.ndarray) -> bool:
    if len(np.unique(y)) == 1 or len(np.unique(x)) == 1:
        return True
    else:
        return False


def get_min_max_starters(points: np.ndarray):
    isLine = all_points_on_h_or_v_line(points[:, 0], points[:, 1])
    if isLine:
        return None, None, None
    else:
        min_index = np.argmin(points[:, 0])
        max_index = np.argmax(points[:, 0])
        return np.array([[points[min_index, 0], points[min_index, 1]],
                         [points[max_index, 0], points[max_index, 1]]]), min_index, max_index


def is_left_of(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> (float, np.ndarray):
    # Where a = line point 1; b = line point 2; c = point to check against
    # result == 0 -> colinear, result > -threshold = left, < -threshold = right
    ab = b - a
    ac = c - a
    # use threshold due to rounding errors --> if slightly larger than zero --> considered left
    threshold = 1e-9
    cross_product = np.cross(ab, ac)
    if cross_product >= threshold:
        cross_product = find_dist(cross_product, a, b)
        return cross_product
    else:
        return 0


def left_to_line_and_furthest(a: np.ndarray, b: np.ndarray, points: np.ndarray) -> (np.ndarray, np.ndarray):
    is_left_result = np.apply_along_axis(lambda p: np.array([is_left_of(a, b, p), p[0], p[1]]), 1, points)
    filtered_result = is_left_result[is_left_result[:, 0] != 0][:, 1:]
    if len(filtered_result) == 1:
        max_value = filtered_result[0]
    else:
        max_value = is_left_result[np.argmax(is_left_result[:, 0])][1:]
    return filtered_result, max_value


def find_dist(distance, a, b):
    return distance / np.linalg.norm(b - a)


def get_quickhull_step_results(points):
    quickhull_hull, steps_quickhull_upper, steps_quickhull_lower = quick_hull_step_through(points)
    steps_quickhull_upper = dict(sorted(steps_quickhull_upper.items()))
    steps_quickhull_lower = dict(sorted(steps_quickhull_lower.items()))
    list_results = []
    list_results.extend(steps_quickhull_upper.values())
    list_results.extend(steps_quickhull_lower.values())
    return quickhull_hull, list_results
