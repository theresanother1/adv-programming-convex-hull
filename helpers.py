import numpy as np
import time
import GiftWrapper
import Quickhull


def generate_random_points(num_points):
    x = np.random.uniform(size=(num_points, 2))
    return x


def generate_circle(radius, num_points):
    # Generate points on a circle
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    return np.column_stack((x, y))


def generate_point(num_points):
    # Generate a num_points point at the origin
    return np.tile([0, 0], (num_points, 1))


# generates point within the square of size x
def generate_square(size, num_points):
    points = np.random.uniform(-size/2, size/2, (num_points, 2))
    return points


def generate_line(num_points):
    # Generate points on a line
    x = np.linspace(-20, 20, num_points)
    y = np.zeros(num_points)
    return np.column_stack((x, y))


def generate_random_point_file(num_points, output_file):
    with open(output_file, 'w') as f:
        f.write(f"{num_points}\n")
        for _ in range(num_points):
            x = np.random.uniform(-100.0, 100.0)
            y = np.random.uniform(-100.0, 100.0)
            f.write(f"{x:.6f}, {y:.6f}\n")


def generate_file_from_specific_form(output_file, function, num_points, size):
    with open(output_file, 'w') as f:
        f.write(f"{num_points}\n")
        points = function(size, num_points)
        for point in points:
            f.write(f"{point[0]:.6f}, {point[1]:.6f}\n")


def generate_file_from_specific_form_one_argument(output_file, function, num_points):
    with open(output_file, 'w') as f:
        f.write(f"{num_points}\n")
        points = function(num_points)
        print(points)
        for i in range(num_points):
            f.write(f"{points[0]:.6f}, {points[1]:.6f}\n")


def read_points_from_file(filename):
    # Open the file in read mode
    with open(filename, 'r') as file:
        number_of_points = int(file.readline().strip())
        points = np.loadtxt(file, delimiter=',', max_rows=number_of_points)

    if points[0].size != 2:
        raise ValueError("Each point must have two values (x, y).")

    return points


def all_points_on_line(x: np.ndarray, y: np.ndarray):
    x_size = np.unique(x).size
    y_size = np.unique(y).size
    if x_size == 1 or y_size == 1:
        return True
    else:
        return False


def measure_time(func, points):
    start_time = time.perf_counter()
    hull = func(points)
    end_time = time.perf_counter()
    print(f"Executed algorithm in {(end_time - start_time)} seconds.")
    return (end_time - start_time), hull


def continue_or_finish():
    user_input = input("Continue or end? (C/E)  ").strip().upper()
    if user_input == 'C':
        return True
    else:
        return False


def get_points():
    user_input = input("Read in file or generate random (Read File F, Generate Random R, Circle C, Square S, Line L, Point P):  ").strip().upper()
    if user_input in ['R', 'G']:

        if user_input == 'R':
            user_input = input("Input file name - has to be absolute path!:  ").strip()
            try:
                points = read_points_from_file(user_input)
                return points
            except:
                print("Could not read file.  ")

        if user_input == 'G':
            points_amount = int(input("How many points?  "))
            if points_amount >= 0:
                form = input(
                    "What form? (Circle C, Square S, Line L, Point P, Random R): ").strip().upper()
                if form == 'C':
                    radius = int(input("Determine radius in positive number: "))
                    return generate_circle(points_amount, abs(radius))
                elif form == 'S':
                    return generate_square(points_amount)
                elif form == 'L':
                    return generate_line(points_amount)
                elif form == 'P':
                    return generate_point(points_amount)
                elif form == 'R':
                    return generate_random_points(points_amount)


def execute_algo_console(points):
    while True:
        if points is not None:
            #points = get_points()
            algo = input("Choose your algorithm (Quickhull Q/ Gift Wrapper G ):  ").strip().upper()
            if algo in ['Q', 'G']:
                if algo == 'Q':
                    print(f"starting quickhull calculation for {points.shape[0]} points .... ")
                    measure_time(Quickhull.quick_hull, points)

                    # after finished
                    if continue_or_finish():
                        continue
                    else:
                        break

                if algo == 'G':
                    print(f"starting giftwrapper calculation for {points.shape[0]} points .... ")
                    measure_time(GiftWrapper.gift_wrapping_algorithm, points)

                    if continue_or_finish():
                        continue
                    else:
                        break