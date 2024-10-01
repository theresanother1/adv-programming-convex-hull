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
        return np.array([points[0, :], points[-1, :]])

    # Split points into upper and lower sets, initially include all points
    upper_set = np.ones(points.shape[0], dtype=bool)
    lower_set = np.ones(points.shape[0], dtype=bool)

    # do not include left and right point in either set
    upper_set[left_idx] = upper_set[right_idx] = False
    lower_set[left_idx] = lower_set[right_idx] = False

    # include only those points, which are left to line
    upper_set[upper_set] = is_left(left_idx, right_idx, points, upper_set) > 1e-9

    # include only those points, which are left to line
    lower_set[lower_set] = is_left(right_idx, left_idx, points, lower_set) > 1e-9

    # Combine results
    return np.vstack((points[left_idx], find_hull(points, left_idx, right_idx, upper_set), points[right_idx], find_hull(points, right_idx, left_idx, lower_set)))


def find_hull(og_points: np.ndarray, p1_idx: int, p2_idx: int, current_subset_mask: np.ndarray) -> np.ndarray:
    if not np.any(current_subset_mask):
        return np.empty((0, 2))

    # Find point with maximum distance
    distances = is_left(p1_idx, p2_idx, og_points, current_subset_mask)
    max_dist_idx = np.argmax(distances)
    max_point_idx = np.where(current_subset_mask)[0][max_dist_idx]

    # get new subsets
    region_left_to_max = current_subset_mask.copy()
    region_max_to_right = current_subset_mask.copy()
    region_left_to_max[current_subset_mask] = is_left(p1_idx, max_point_idx, og_points, current_subset_mask) > 1e-9
    region_max_to_right[current_subset_mask] = is_left(max_point_idx, p2_idx, og_points, current_subset_mask) > 1e-9

    # Combine results
    return np.vstack((find_hull(og_points, p1_idx, max_point_idx, region_left_to_max),
                      og_points[max_point_idx],
                      find_hull(og_points, max_point_idx, p2_idx, region_max_to_right)))


def is_left(a_idx: int, b_idx: int, points: np.ndarray, current_points_mask: np.ndarray) -> np.ndarray:
    return np.cross(points[b_idx] - points[a_idx], points[current_points_mask] - points[a_idx])


# slower version for step tracing
def quick_hull_step_through(points: np.ndarray) -> (np.ndarray, dict, dict):
    global step_upper
    convex_hull = []
    if points.shape[0] < 3:
        return points, points[0, :], points[1, :]

        # Find leftmost and rightmost points
    minmax, left_idx, right_idx = get_min_max_starters(points)

    # if min max is None --> all points are on one line, all points are hull
    if minmax is None:
        return np.array([points[0, :], points[-1, :]]), minmax[0, :], minmax[1:, ]

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
