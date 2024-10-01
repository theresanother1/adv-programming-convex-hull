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
    points = np.random.uniform(-size / 2, size / 2, (num_points, 2))
    return points


def generate_line(num_points):
    # Generate points on a line
    x = np.linspace(-100, 100, num_points)
    y = np.zeros(num_points)
    return np.column_stack((x, y))


def generate_random_point_file(num_points, output_file):
    with open(output_file, 'w') as f:
        f.write(f"{num_points}\n")
        for _ in range(num_points):
            x = np.random.uniform(-100.0, 100.0)
            y = np.random.uniform(-100.0, 100.0)
            f.write(f"{x:.6f}, {y:.6f}\n")


def generate_one_point_file(num_points, output_file):
    with open(output_file, 'w') as f:
        f.write(f"{num_points}\n")
        for _ in range(num_points):
            x = np.random.uniform(-100.0, 100.0)
            y = np.random.uniform(-100.0, 100.0)
            f.write(f"{x:.6f}, {y:.6f}\n")


def generate_circle_file(num_points, output_file, size: int):
    with open(output_file, 'w') as f:
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        points = np.column_stack((size * np.cos(angles), size * np.sin(angles)))
        f.write(f"{num_points}\n")
        for index in range(num_points):
            x = points[:, 0][index]
            y = points[:, 1][index]
            f.write(f"{x:.6f}, {y:.6f}\n")


def generate_line_file(num_points, output_file):
    with open(output_file, 'w') as f:
        f.write(f"{num_points}\n")
        x = np.linspace(-100, 100, num_points)
        y = np.zeros(num_points)
        points = np.column_stack((x, y))
        for index in range(num_points):
            x = points[:, 0][index]
            y = points[:, 1][index]
            f.write(f"{x:.6f}, {y:.6f}\n")


def read_points_from_file(filename):
    # Open the file in read mode
    with open(filename, 'r') as file:
        number_of_points = int(file.readline().strip())
        points = np.loadtxt(file, delimiter=',', max_rows=number_of_points)

    if points[0].size != 2:
        raise ValueError("Each point must have two values (x, y).")

    return points, number_of_points


def all_points_on_h_or_v_line(x: np.ndarray, y: np.ndarray) -> bool:
    if len(np.unique(y)) == 1 or len(np.unique(x)) == 1:
        return True
    else:
        return False


def measure_time(func, points):
    try:
        print(f"starting execution with {points.shape}")
        start_time = time.perf_counter()
        hull = func(points)
        end_time = time.perf_counter()
        print(f"Executed algorithm in {(end_time - start_time)} seconds.")
        return (end_time - start_time), hull
    except Exception as e:
        print("Could not execute algorithm due to: ", e)
        return 0, np.array([])



def continue_or_finish():
    user_input = input("Continue or end? (C/E)  ").strip().upper()
    if user_input == 'C':
        return True
    else:
        return False


def get_points():
    while True:
        user_input = input(
            "Read in file or generate random (Read File F, Generate Random R):  ").strip().upper()
        if user_input in ['R', 'G']:
            if user_input == 'R':
                user_input = input("Input file name - has to be absolute path!:  ").strip()
                try:
                    points, number_of_points = read_points_from_file(user_input)
                    return points
                except:
                    print("Could not read file.  ")

            if user_input == 'G':
                points_amount = int(input("How many points?  "))
                if points_amount >= 0:
                    return generate_random_points(points_amount)


def execute_algo_console():
    while True:
        points = get_points()
        if points is not None:
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


'''
THESE WILL NOT RUN WITHOUT THE CORRECT FILES PROVIDED 

'''


def measure_time_on(func, number, index):
    circle = f"circle_points_{number}_on_complexity_{index}.txt"
    line = f"line_points_{number}_on_complexity_{index}.txt"
    random = f"random_test_points_{number}_on_complexity_{index}.txt"
    points, number_of_points = read_points_from_file(circle)
    print("reading file from ")
    print(f"random_test_points_{number}_on_complexity_{index}.txt")
    start_time = time.perf_counter()
    hull = func(points)
    end_time = time.perf_counter()
    print(f"Executed algorithm in {(end_time - start_time)} seconds.")
    return end_time - start_time

def run_o_complexity_comparison(filename):
    n = [100, 1000, 10000, 100000, 1000000, 10000000]  # , 100000000]
    runs = 10
    results = {}
    for number in n:
        if number == 100000000:
            runs = 8

        result = sum(run for index in range(runs) for run in
                     [measure_time_on(Quickhull.quick_hull, number, index)]) / runs
        results[number] = result
        print(result)

    with open(filename, 'w') as file:
        file.write("Quickhull O(n) complexity\n")
        for n, time in results.items():
            file.write(f'n = {n}, time = {time}\n')
    return results


def run_o_complexity_comparison_giftwrapper(filename):
    n = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
    runs = 10
    results = {}
    index = 0
    for number in n:
        if number == 100000000:
            runs = 2
        generate_test_files_random(number)
        result = sum(run for index in range(runs) for run in
                     [measure_time_on(GiftWrapper.gift_wrapping_algorithm, number, index)]) / runs
        results[number] = result
        print(result)
        index += 1
    with open(filename, 'w') as file:
        file.write("Giftwrapper O(n) complexity\n")
        for n, time in results.items():
            file.write(f'n = {n}, time = {time}\n')
    return results


def generate_files():
    n = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
    results = {}
    index = 0
    for number in n:
        generate_test_files_circle(number)
        # generate_test_files_line(number)
        index += 1

    return results


def generate_test_files_random(number):
    for index in range(10):
        generate_random_point_file(number, f"random_test_points_{number}_on_complexity_{index}.txt")


def generate_test_files_circle(number):
    for index in range(10):
        generate_circle_file(number, f"circle_points_{number}_on_complexity_{index}.txt", number)


def generate_test_files_line(number):
    for index in range(10):
        generate_line_file(number, f"line_points_{number}_on_complexity_{index}.txt")
