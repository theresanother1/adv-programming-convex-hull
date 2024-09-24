import numpy as np
import Quickhull
import Simple_View
import time


def generate_random_points(num_points):
    return np.random.uniform(100, 500, size=(num_points, 2))


def generate_circle(num_points, radius):
    # Generate points on a circle
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    return np.column_stack((x, y))


def generate_point(num_points):
    # Generate a num_points point at the origin
    return np.tile([0, 0], (num_points, 1))


def generate_square(num_points):
    points = np.array([])
    for i in range(num_points):
        x = (i % 4) * 2 - 1
        y = (i // 4) * 2 - 1
        # print(x, y)
        points = np.append(points, (x, y))
    return points


def generate_line(num_points):
    # Generate points on a line
    x = np.linspace(-20, 20, num_points)
    y = np.zeros(num_points)
    return np.column_stack((x, y))


def generate_point_file(num_points, output_file):
    with open(output_file, 'w') as f:
        f.write(f"{num_points}\n")
        for _ in range(num_points):
            x = np.random.uniform(-100.0, 100.0)
            y = np.random.uniform(-100.0, 100.0)
            f.write(f"{x:.6f}, {y:.6f}\n")


def read_points_from_file(filename):
    # Open the file in read mode
    with open(filename, 'r') as file:
        number_of_points = int(file.readline().strip())
        points = np.loadtxt(file, delimiter=',', max_rows=number_of_points)

    if points[0].size != 2:
        raise ValueError("Each point must have two values (x, y).")

    return points


def run_quickhull_with_visu(points: np.ndarray):
    win = init_window_and_draw_points(points)
    win.getMouse()
    chResult = Quickhull.convex_hull_visu(points, win)
    print(chResult)


def init_window_and_draw_points(points: np.ndarray):
    x, y = Quickhull.get_min_max(points)
    win = Simple_View.init_window(x, y)
    Simple_View.draw_points_init(points, win)
    return win


def measure_time(func, points):
    start_time = time.perf_counter()
    func(points)
    end_time = time.perf_counter()
    print("Elapsed time in secs: ", end_time - start_time)


def continue_or_finish():
    user_input = input("Continue or end? (C/E)  ").strip().upper()
    if user_input == 'C':
        return True
    else:
        return False


def get_points():
    user_input = input("Read in file or generate random (R/G):  ").strip().upper()
    if user_input in ['R', 'G']:

        if user_input == 'R':
            user_input = input("Input file name - has to be absolute path!:  ").strip()
            try:
                points = read_points_from_file(user_input)
                return points
            except:
                print("Could not read file.  ")

        if user_input == 'G':
            user_input = int(input("How many points?  "))
            if user_input >= 0:
                return generate_random_points(user_input)


def execute_algo_console():
    while True:
        points = get_points()

        algo = input("Choose your algorithm (Quickhull Q/ ... ):  ").strip().upper()
        if algo in ['Q', '... ']:
            if algo == 'Q':
                visu = input("With visualisation? (y/n)  ").strip()
                if visu == 'y':
                    run_quickhull_with_visu(points)

                    # after finished
                    if continue_or_finish():
                        continue
                    else:
                        break

                if visu == 'n':

                    measure_time(Quickhull.convex_hull_fast, points)

                    if continue_or_finish():
                        continue
                    else:
                        break

            if algo == '... ':
                print("Not implemented yet")
