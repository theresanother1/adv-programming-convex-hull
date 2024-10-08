# **************************************************************** #
#
#                   APRG Group 5 Task 2
#                 Theresa, Robert, Salome
#                        202409xx
#
# **************************************************************** #

''' Introduction to the code:

GUI:

    ++++++++++++++++++++++++++++ app ++++++++++++++++++++++++++++
    -------------------------- - area - -------------------------
    | _________ d1 _____________  ___________ d2 ________________|
    ||                          ||                               |
    || p1 (plot)    p2 (plot)   ||          (Buttons)            |
    ||                          ||                               |
    ||                          ||_______________________________|
    ||                          |____________ d3 ________________|
    ||                          ||                               |
    ||                          ||                               |
    ||                          ||          (Text)               |
    ||                          ||                               |
    ||__________________________||_______________________________|
    |------------------------------------------------------------|

USER INTERACTIONS:

    - p1 shows the data being processed with Giftwrapper
    - p2 shows the data being processed with Quickhull
    - p1 and p2 run one after another so execution time measurements and
      the comparison of numbers of steps can be performed
    - the reset button clears the animation plots and stops any ongoing
      animation


NOTES:

    - Inquiring AI-Bots to help work on this code it is likely to make use of
      the PyQt5 library on top of pyqtgraph. To keep it clean however this code
      relies on "native" pyqtgraph only for visualisations and user
      interactions without relying on PyQt5 or QtGui imports. Pyqtgraph is
      typically bundled with PySide (2 and 6)
    - For better manageability and ease of debugging  the choice was made to
      organise the code in such a way that pyqtgraph is only needed to be
      imported in one single file, and all actions related to the use of that
      library are handled in one place. As the program makes use of Event
      Buttons, the file was chosen to be where the main loop runs.

'''


import pyqtgraph as pg
from pyqtgraph.dockarea import Dock, DockArea
import helpers
from GiftWrapper import gift_wrapping_algorithm, gift_wrapping_step_through
import Quickhull
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np

# ************************* GLOBAL VARIABLES ******************************** #

######################
# GUI Interface setup
######################

# GUI: Main Window, Areas
app = pg.mkQApp("APRG Task 2, Group 7")
area = DockArea()
area.resize(1600, 600)
area.setWindowTitle("Convex Hull - Group 7")

# GUI: Docks
d1 = Dock("Plots", size=(1200, 600))
d2 = Dock("Control Panel", size=(400, 300))
d3 = Dock("Info-Panel", size=(400, 300))

# GUI: Widgets
# ## (for holding plots)
plots_panel = pg.GraphicsLayoutWidget()

# ## (for holding user interaction features)
control_container = QtWidgets.QWidget()
control_layout = QtWidgets.QVBoxLayout()
control_panel = pg.LayoutWidget()
# ## (for holding program information)
info_container = QtWidgets.QWidget()
info_layout = QtWidgets.QVBoxLayout()

# GUI: Plots
p1 = plots_panel.addPlot(row=0, col=0, title="Gift Wrapper")
p2 = plots_panel.addPlot(row=0, col=1, title="Quickhull")

# @Salome das hier hat nur das fenster komisch am bildschirm verschoben, daher auskommentiert
# plots_panel.ci.layout.setColumnStretchFactor(1, 0)
# plots_panel.ci.layout.setColumnStretchFactor(1, 1)

# GUI: Buttons
btn_loadData = pg.QtWidgets.QPushButton('Load New Data')
btn_generateData = pg.QtWidgets.QPushButton('Generate Random Data')
btn_step = pg.QtWidgets.QPushButton('Step Through')
btn_result = pg.QtWidgets.QPushButton('Show Result')
btn_run = pg.QtWidgets.QPushButton('Quick Run')
btn_reset = pg.QtWidgets.QPushButton('Reset')
text_amount = pg.QtWidgets.QLineEdit()
text_amount.setPlaceholderText('Enter number of points to generate')  # Set a placeholder text

# GUI: Program Text
text_label = QtWidgets.QLabel("Load File or generate random points")
additional_info_quickhull = QtWidgets.QLabel("")
additional_info_giftwrapper = QtWidgets.QLabel("")
text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
additional_info_quickhull.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
additional_info_giftwrapper.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
text_label.setWordWrap(True)
additional_info_quickhull.setWordWrap(True)
additional_info_giftwrapper.setWordWrap(True)

# GUI: Layout
# ## adding text to Widget
info_layout.addStretch()
info_layout.addWidget(text_label)
info_layout.addWidget(additional_info_quickhull)
info_layout.addWidget(additional_info_giftwrapper)
info_layout.addStretch()
info_container.setLayout(info_layout)
# ## adding Buttons to a Widget
control_panel.addWidget(btn_loadData, row=0, col=0)
control_panel.addWidget(btn_run, row=0, col=1)
control_panel.addWidget(text_amount, row=0, col=2)
control_panel.addWidget(btn_step, row=1, col=0)
control_panel.addWidget(btn_result, row=1, col=1)
control_panel.addWidget(btn_generateData, row=1, col=2)
control_panel.addWidget(btn_reset, row=3, col=1)
control_layout.addWidget(control_panel)
control_container.setLayout(control_layout)
# ## adding Widgets to a dock
d1.addWidget(plots_panel)
d2.addWidget(control_container)
d3.addWidget(info_container)
# ## adding docks to a area
area.addDock(d1, 'left')
area.addDock(d2, 'right')
area.addDock(d3, 'bottom', d2)

# GUI: Make it beautiful
colors = ['r', 'g', 'b']
button_style = """
    QPushButton {
        background-color: #ff007f;
        color: black;
        font-size: 16px;
        border-radius:30px;
        padding:20px 10px;
        min-height: 40px;
        width: 130px; 
    }
    QPushButton:hover {
        background-color: #e56a89;
    }
    QPushButton:disabled {
        background-color: #b32d5e;
    }
"""

styleTextEntry = """
    QLineEdit {
        font-size: 16 px;
        border-radius: 30px;
        padding: 20px 10px;
        width: 130px; 
        min-height: 30px;   
        background-color: white;
    }
"""
text_amount.setStyleSheet(styleTextEntry)
btn_loadData.setStyleSheet(button_style)
btn_generateData.setStyleSheet(button_style)
btn_step.setStyleSheet(button_style)
btn_result.setStyleSheet(button_style)
btn_run.setStyleSheet(button_style)
btn_reset.setStyleSheet(button_style)
control_container.setStyleSheet("background-color: black;")
info_container.setStyleSheet("background-color: black;")
text_label.setStyleSheet("color: white; font-size:16px")

# global variables for quickhull algo step throug
steps_quickhull_upper = np.array([])
steps_quickhull_lower = np.array([])
steps_quickhull = []
steps_giftwrapper = np.array([])
quickhull_hull = np.array([])

#######################
# DATA HANDLING
#######################

data = None
animation_timer = None
animation_active = False
step_animation_timer = None
animation_interval = 500  # Animation steps speed in ms
step_index = 0
step_index_plot2 = 0
current_plot = 1  # tracking for step through functionality
points_amount = 0

# Initialisation of the buttons (states at program start)
btn_step.setEnabled(False)
btn_run.setEnabled(False)
btn_result.setEnabled(False)
btn_reset.setEnabled(False)


# ****************  FUNCTION DEFINITIONS AND EVENT HANDLING  **************** #

# Activities (and their methods) in the program flow are triggered solely by
# event buttons (once the interface is running)

#######################
# GUI Interface Setup
#######################


def clear_all_plots():
    p1.clear()
    p2.clear()


def plot_points(x, y):
    p1.plot(x, y, pen=None, symbol='o')
    p2.plot(x, y, pen=None, symbol='o')


def reset_plots():
    global step_index, animation_active, current_plot, step_index_plot2, current_plot, steps_quickhull

    p1.clear()
    p2.clear()

    animation_active = False
    reset_data()

    if animation_timer is not None and animation_timer.isActive():
        animation_timer.stop()

    btn_step.setText("Step Through")

    if data is not None:
        #btn_step.setEnabled(True)
        btn_result.setEnabled(True)
        #btn_run.setEnabled(True)
    else:
        #btn_step.setEnabled(False)
        btn_result.setEnabled(False)
        #btn_run.setEnabled(False)

    btn_loadData.setEnabled(True)
    btn_generateData.setEnabled(True)

    text_label.setText("Plots are cleared, Input Data is still shown")


######################
# DATA HANDLING
######################


# LOAD DATA FROM FILE
def load_data():
    global data, animation_active, btn_step, btn_result, btn_run

    text_label.setText("Select Data")
    file_dialog = QtWidgets.QFileDialog()
    file_name, _ = file_dialog.getOpenFileName(None, "Select Data File *.txt", )

    if file_name:
        try:
            return helpers.read_points_from_file(file_name)
        except Exception as e:
            text_label.setText("Failed to load file: " + str(e) + "Load again")
            return None
    else:
        text_label.setText("Load Data")
        btn_step.setEnabled(False)
        btn_result.setEnabled(False)
        btn_run.setEnabled(False)

    animation_active = False

    return None


# PREPROCESS DATA FROM SOURCE FILE
def read_values_from_data(data):
    if data is not None:
        try:
            x = data[:, 0]
            y = data[:, 1]
            return x, y
        except Exception as e:
            text_label.setText("Error extracting 'x' and 'y' values: "
                               + str(e))

            return None, None
    else:
        return None, None


# PLOTTING DATA
def plotting():
    global animation_active, data
    reset_data()
    data, number_of_points = load_data()
    x, y = read_values_from_data(data)

    clear_all_plots()

    if x is not None and y is not None:
        update_plot_after_generating(x, y, number_of_points)
    else:
        disable_algo_relevant_buttons()

    btn_loadData.setEnabled(True)
    btn_generateData.setEnabled(True)
    animation_active = False


# RESET Plots and animation, replot current points
def reset_data():
    global current_plot, steps_quickhull, step_index, step_index_plot2, \
        animation_timer, step_animation_timer, animation_active
    current_plot = 1
    steps_quickhull = []
    step_index = 0
    step_index_plot2 = 0
    step_animation_timer = None
    animation_timer = None
    animation_active = False
    x, y = read_values_from_data(data)
    if x is not None:
        if x.size <= 100:
            plot_points(x, y)
        if x.size > 20:
            btn_run.setEnabled(False)
            btn_step.setEnabled(False)
        elif x.size <= 20:
            btn_run.setEnabled(True)
            btn_step.setEnabled(True)



# update plots after generating random data
def update_plot_after_generating(x, y, number_of_points):
    if x.size <= 100:
        plot_points(x, y)
        text_label.setText(f"Generated {number_of_points} points. You can load new data or run the algorithms"
                            f"\nQuick run and Step through only available for <= 20 points.")
        btn_result.setEnabled(True)
        btn_reset.setEnabled(True)
    if x.size <= 20:
        btn_step.setEnabled(True)
        btn_run.setEnabled(True)
    if x.size > 100:
        text_label.setText(f"Generated {number_of_points} points. Not plotted - too many points.")
        btn_result.setEnabled(True)
        btn_reset.setEnabled(True)


def disable_algo_relevant_buttons():
    btn_step.setEnabled(False)
    btn_result.setEnabled(False)
    btn_run.setEnabled(False)
    btn_reset.setEnabled(False)


# Plot random points
def plotting_random():
    global animation_active, data, current_plot, step_index, step_index_plot2, points_amount
    reset_data()

    points_amount = text_amount.text()
    try:
        data = helpers.generate_random_points(int(points_amount))
    except:
        return
    clear_all_plots()

    x, y = read_values_from_data(data)

    if x is not None and y is not None:
        update_plot_after_generating(x, y, len(x))

    else:
        disable_algo_relevant_buttons()

    btn_loadData.setEnabled(True)
    btn_generateData.setEnabled(True)
    animation_active = False


# QUICK RUN ANIMATION

def update_curve(p, x, y, i):
    global animation_active, animation_timer
    if i < len(x):
        p.plot(x[:i + 1], y[:i + 1], pen='r')
        p.plot([x[i]], [y[i]], pen=None, symbol='o', symbolSize=10,
               symbolBrush='g')
        animation_timer.i += 1
    else:
        animation_timer.stop()
        animation_active = False
        btn_loadData.setEnabled(True)
        btn_generateData.setEnabled(True)


def animation_start(p, x, y, text):
    global animation_active, animation_timer

    try:
        animation_active = True
        text_label.setText(text)

        animation_timer = QtCore.QTimer()
        animation_timer.timeout.connect(lambda: update_curve(
            p, x, y, animation_timer.i))
        animation_timer.i = 0
        animation_timer.start(animation_interval)

    except Exception as e:
        print("Error during animation: " + str(e))
        animation_active = False


def quick_run():
    global animation_active, step_animation_timer

    # Ensure there's data to process and no ongoing animation
    if data is None or animation_active:
        return

    # Disable buttons to prevent user interaction during the animation
    animation_active = True
    btn_loadData.setEnabled(False)
    btn_generateData.setEnabled(False)
    btn_step.setEnabled(False)
    btn_result.setEnabled(False)

    # Initialize the animation timer
    step_animation_timer = QtCore.QTimer()

    # Start the automated quick run animation
    animate_quick_run()


def animate_quick_run():
    global animation_active, step_animation_timer, current_plot, step_index, step_index_plot2

    # Ensure there's data to process
    if data is None or step_animation_timer is None:
        return

    # Call the step_through function to handle the next step in the animation
    step_through()

    # Check if the animation is complete
    if current_plot == 2 and step_index_plot2 > len(steps_quickhull):
        # Animation is complete after finishing the second plot
        animation_active = False

        # Stop the timer
        if step_animation_timer.isActive():
            step_animation_timer.stop()

        # Reset button states to allow further interactions
        btn_loadData.setEnabled(True)
        btn_generateData.setEnabled(True)
        btn_step.setEnabled(True)
        btn_result.setEnabled(True)
        text_label.setText("Quick Run Animation Completed")

        # Reset the plot states
        current_plot = 1
        step_index = 0
        step_index_plot2 = 0
    else:
        # Continue animation by scheduling the next call
        step_animation_timer.singleShot(animation_interval, animate_quick_run)


def plot_convex_hull(p, points, hull_points):
    p.clear()
    p.plot(points[:, 0], points[:, 1], pen=None, symbol='o')
    for i in range(len(hull_points)):
        start = hull_points[i]
        end = hull_points[(i + 1) % len(hull_points)]
        p.plot([start[0], end[0]], [start[1], end[1]], pen='r', symbol='o',
               symbolSize=10, symbolBrush='g')


def show_results():
    global data

    if data is None:
        return

    text_label.setText("Calculating results .... ")

    # Reading the points out of the data
    x, y = read_values_from_data(data)

    points = np.column_stack((x, y))

    if (len(x) > 10000):
        text_label.setText(f"\n GUI processes only <= 10000 points.")
        return

    p1.clear()
    p2.clear()

    # Calculating the convex hull with the quickhull wrapping algorithm
    print("Start calculate quickhull.")
    time_q, convex_hull_quickhull = helpers.measure_time(Quickhull.quick_hull, points)
    print("Finished calculate quickhull.")

    # Calculating the convex hull with the gift wrapping algorithm
    print("Start calculate giftwrapper.")
    time_g, gift_wrapper_convex_hull = helpers.measure_time(gift_wrapping_algorithm, points)
    print("Finished calculate giftwrapper.")

    hulls_are_equal = len(convex_hull_quickhull) == len(gift_wrapper_convex_hull)

    # Plotting the convex hull only for values smaller 100
    if x.size <= 100:
        plot_convex_hull(p1, points, gift_wrapper_convex_hull)
        plot_convex_hull(p2, points, convex_hull_quickhull)
        text_label.setText(f"\nExecution time for {len(x)}:"
                           f"\nGift Wrapper time:  {time_g} secs"
                           f"\nQuickhull Time:  {time_q} secs ")
    else:
        text_label.setText(f"\nNo data points plotted - too many points"
                           f"\nExecution time for {len(x)} points: "
                           f"\nGift Wrapper time:  {time_g} secs"
                           f"\nQuickhull Time:  {time_q} secs "
                           f"\nHulls are equal:  {hulls_are_equal}")


# paints the line in step by step plotting, repaints discarded lines
def repaint_line_step(a_x, a_y, p, only_points):
    index = 0
    while index < len(a_x):
        if only_points:
            p.plot(a_x[:index + 1], a_y[:index + 1], symbol='o',
                   symbolSize=10, symbolBrush='g')
        else:
            p.plot(a_x[:index + 1], a_y[:index + 1], pen='r', symbol='o',
                   symbolSize=10, symbolBrush='g')
        index += 1


# resets the whole plot
def reset_paint_step(og_x, og_y, p):
    p.clear()
    p.plot(og_x, og_y, pen=None, symbol='o')


# almost the same as plot_current_step, split for readability!
def revert_previous_step(p, steps, index):
    previous_step = np.array(steps[index - 1])
    hull_prev_x = previous_step[:, 0]
    hull_prev_y = previous_step[:, 1]
    repaint_line_step(hull_prev_x, hull_prev_y, p, True)


def plot_current_step(p, steps, index):
    current_step = np.array(steps[index])
    hull_x_step = current_step[:, 0]
    hull_y_step = current_step[:, 1]
    repaint_line_step(hull_x_step, hull_y_step, p, False)


def step_through():
    global step_index, current_plot, data, steps_quickhull_upper, step_index_plot2, quickhull_hull, \
        steps_quickhull_lower, steps_quickhull, steps_giftwrapper, is_comparison_phase, current_selected_point

    if data is None:
        return

    # Reading the points out of the data
    x, y = read_values_from_data(data)
    points = np.column_stack((x, y))

    if current_plot == 1:
        p = p1
    if current_plot == 2:
        p = p2

    if current_plot == 1 and step_index == 0:
        # Calculating the konvex hull with the Gift-Wrapping Algoritmus
        steps_giftwrapper = gift_wrapping_step_through(points)
        step_index += 1

        # Just a Boolean to activate the compare modi for the first step.
        is_comparison_phase = True

    elif current_plot == 1 and step_index < len(steps_giftwrapper):

        # Access to the actual step
        current_step = steps_giftwrapper[step_index]
        hull_points = current_step['hull']
        compared_points = current_step['compared_points']
        selected_point = current_step.get('selected_point', None)

        hull_x = hull_points[:, 0]
        hull_y = hull_points[:, 1]

        p.clear()

        # Visualize the given point cloud as black dots in our blot
        p.plot(points[:, 0], points[:, 1], pen=None, symbol='o', symbolSize=8, symbolBrush='k')

        # Visualizing the hull in red
        p.plot(hull_x, hull_y, pen='r')

        # To visualize which point is been right now used. Its marked by a blue point
        p.plot([hull_x[-1]], [hull_y[-1]], pen=None, symbol='o', symbolSize=10, symbolBrush='b')

        if is_comparison_phase:
            # Visualize the actual compared points to the makred point.
            if len(compared_points) > 0:
                for point in compared_points:
                    # A green line is been used to visualize the relationship between the compared and the current point
                    p.plot([hull_x[-1], point[0]], [hull_y[-1], point[1]], pen='g')
                    # The compared points are marked green and in addition as dots with an x 
                    p.plot([point[0]], [point[1]], pen=None, symbol='x', symbolSize=8, symbolBrush='g')

            # Now the marked modi is been activate to mark the perfect point for the convex hull
            is_comparison_phase = False
            current_selected_point = selected_point  # The current selected point is been saved for the next phase
        else:
            # Visualize the Point as and red dot 
            if current_selected_point is not None:
                p.plot([current_selected_point[0]], [current_selected_point[1]], pen=None, symbol='o', symbolSize=12,
                       symbolBrush='r')

            # Chaning to the next step and reset the phase 
            step_index += 1
            is_comparison_phase = True
            current_selected_point = None  # The current selected point is now also been reseted

        btn_step.setText("Next Step")
        text_label.setText(f"Step {step_index}/{len(steps_giftwrapper)}")

    elif current_plot == 1 and step_index == len(steps_giftwrapper):
        # Switch to Quickhull plot
        current_plot = 2
        step_index_plot2 = 0  # Initialize the index for Quickhull steps
        quickhull_hull, steps_quickhull = Quickhull.get_quickhull_step_results(points)
        text_label.setText("Starting Quickhull animation...")

    # Get Quickhull steps for plotting
    elif current_plot == 2 and step_index_plot2 == 0:
        quickhull_hull, steps_quickhull = Quickhull.get_quickhull_step_results(points)
        step_index_plot2 += 1

    # Print Quickhull steps
    elif current_plot == 2 and 0 <= step_index_plot2 < len(steps_quickhull):
        if step_index_plot2 > 0:
            revert_previous_step(p, steps_quickhull, step_index_plot2)

        plot_current_step(p, steps_quickhull, step_index_plot2)
        step_index_plot2 += 1

    # Print complete hull - for beauty reasons
    elif current_plot == 2 and step_index_plot2 == len(steps_quickhull):
        quickhull_hull = np.array(quickhull_hull)
        hull_x_step = quickhull_hull[:, 0]
        hull_y_step = quickhull_hull[:, 1]
        reset_paint_step(x, y, p)
        repaint_line_step(hull_x_step, hull_y_step, p, False)

    else:
        if current_plot < 3:
            current_plot += 1
            step_index = 0
            step_index_plot2 = 0
            text_label.setText("Continuing with the next algorithm")
        else:
            btn_step.setText("Step Through")
            text_label.setText("Step Through is completed")
            current_plot = 1
            step_index = 0
            step_index_plot2 = 0
            btn_loadData.setEnabled(True)
            btn_generateData.setEnabled(True)


###########################
# UI EVENT BUTTON HANDLING
###########################

btn_loadData.clicked.connect(plotting)
btn_generateData.clicked.connect(plotting_random)
btn_run.clicked.connect(quick_run)
btn_result.clicked.connect(show_results)
btn_step.clicked.connect(step_through)
btn_reset.clicked.connect(reset_plots)

###############
# MAIN LOOP
###############

area.show()

# Qt event loop
if __name__ == '__main__':
    pg.exec()
