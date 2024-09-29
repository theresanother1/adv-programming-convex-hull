import helpers

if __name__ == '__main__':
    # helpers.generate_point_file(10000, "test_generate.txt")

 #   NUM_POINTS = 1000

    # points = helpers.read_points_from_file("./test_generate.txt")

    # points = helpers.generate_square(NUM_POINTS)
    # points = helpers.generate_line(NUM_POINTS)
    # points = helpers.generate_point(NUM_POINTS)
    # points = helpers.generate_circle(NUM_POINTS, 80)
    # points = helpers.generate_random_points(NUM_POINTS)

    # print(points)

    # execute to have a first console version of how flow could look like
    #helpers.execute_algo_console()
    helpers.generate_file_from_specific_form("square_visu.txt", helpers.generate_square, 10000, 20)
    #helpers.generate_file_from_specific_form_one_argument("line_visu.txt", helpers.generate_square, 50)