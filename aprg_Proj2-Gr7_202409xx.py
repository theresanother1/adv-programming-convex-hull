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
    || p3 (plot)    p4 (plot)   ||                               |
    ||                          ||                               |
    ||                          ||          (Text)               |
    ||                          ||                               |
    ||__________________________||_______________________________|
    |------------------------------------------------------------|

USER INTERACTIONS:

    - p1 shows the data being processed with alogrithm A
    - p2 shows the data being processed with alogrithm B
    - p3 shows the data being processed with alogrithm C
    - p1, p2 and p3 run one after another so execution time measurements and
      the comparison of numbers of steps can be performed
    - p4 shows the data from the input file. It is being updated every time
      the "Load Data"-button is pressed
    - the reset button clears the animation plots and stops any ongoing
      animation


NOTES:

    - Inquiring AI-Bots to help work on this code it is likely to make use of
      the PyQt5 library on top of pyqtgraph. To keep it clean however this code
      relies on "native" pyqtgraph only for visualisations and user
      interactions without relying on PyQt5 or QtGui imports. Pyqtgraph is
      typically bundled with PySide (2 and 6)
    - For better managability and ease of debugging  the choice was made to
      organise the code in such a way that pyqtgraph is only needed to be
      imported in one single file, and all actions related to the use of that
      library are handled in one place. As the program makes use of Event
      Buttons, the file was chosen to be where the main loop runs.

'''

import pyqtgraph as pg
from pyqtgraph.dockarea import Dock, DockArea
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np
import pandas as pd


# ************************* GLOBAL VARIABLES ******************************** #

######################
# GUI Interface setup
######################

# GUI: Main Window, Areas
app = pg.mkQApp("APRG Task 2, Group 7")
area = DockArea()
area.resize(1200, 600)
area.setWindowTitle("Convexe Hull - Group 7")

# GUI: Docks
d1 = Dock("Plots", size=(800, 600))
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
p1 = plots_panel.addPlot(row=0, col=0, title="Plot 1")
p2 = plots_panel.addPlot(row=0, col=1, title="Plot 2")
p3 = plots_panel.addPlot(row=1, col=0, title="Plot 3")
p4 = plots_panel.addPlot(row=1, col=1, title="Plot 4")

# GUI: Buttons
btn_loadData = pg.QtWidgets.QPushButton('Load New Data')
btn_step = pg.QtWidgets.QPushButton('Step Through')
btn_result = pg.QtWidgets.QPushButton('Show Result')
btn_run = pg.QtWidgets.QPushButton('Quick Run')
btn_reset = pg.QtWidgets.QPushButton('Reset')

# GUI: Program Text
text_label = QtWidgets.QLabel("Load File")
text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

# GUI: Layout
# ## adding text to Widget
info_layout.addStretch()
info_layout.addWidget(text_label)
info_layout.addStretch()
info_container.setLayout(info_layout)
# ## adding Buttons to a Widget
control_panel.addWidget(btn_loadData, row=0, col=1)
control_panel.addWidget(btn_step, row=1, col=0)
control_panel.addWidget(btn_result, row=1, col=1)
control_panel.addWidget(btn_run, row=1, col=2)
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
    }
    QPushButton:hover {
        background-color: #e56a89;
    }
    QPushButton:disabled {
        background-color: #b32d5e;
    }
"""
btn_loadData.setStyleSheet(button_style)
btn_step.setStyleSheet(button_style)
btn_result.setStyleSheet(button_style)
btn_run.setStyleSheet(button_style)
btn_reset.setStyleSheet(button_style)
control_container.setStyleSheet("background-color: black;")
info_container.setStyleSheet("background-color: black;")
text_label.setStyleSheet("color: white; font-size:16px")


#######################
# DATA HANDLING
#######################

data = None
animation_timer = None
animation_active = False
animation_interval = 200 # Animation steps speed in ms
step_index = 0
current_plot = 1    # tracking for step through functionality

# Initialisation of the buttons (states at program start)
btn_step.setEnabled(False)
btn_run.setEnabled(False)
btn_result.setEnabled(False)
btn_reset.setEnabled(False)


# ****************  FUNCTION DEFINITIONS AND EVENT HANDLING  **************** #

# TODO Functions can be placed elsewhere (in other files) if the do not make
# use pyqtgraph methods.
# Activities (and their methods) in the program flow are triggered solely by
# event buttons (once the interface is running)

#######################
# GUI Interface Setup
#######################


def clear_all_plots():

    p1.clear()
    p2.clear()
    p3.clear()
    p4.clear()


def reset_plots():
    global step_index, animation_active

    p1.clear()
    p2.clear()
    p3.clear()

    animation_active = False
    step_index = 0

    if animation_timer is not None and animation_timer.isActive():
        animation_timer.stop()

    btn_step.setText("Step Through")

    if data is not None:
        btn_step.setEnabled(True)
        btn_result.setEnabled(True)
        btn_run.setEnabled(True)
    else:
        btn_step.setEnabled(False)
        btn_result.setEnabled(False)
        btn_run.setEnabled(False)

    btn_loadData.setEnabled(True)

    text_label.setText("Plots are cleared, Input Data is still shown")

######################
# DATA HANDLING
######################


# LOAD DATA FROM FILE
def load_data():
    global data, animation_active, btn_step, btn_result, btn_run

    text_label.setText("Select Data")
    file_dialog = QtWidgets.QFileDialog()
    file_name, _ = file_dialog.getOpenFileName(None, "Select Data File", "",
                                               "*.csv or *.txt")

    if file_name:
        try:
            # TODO adapt text parsing - just an example
            if file_name.endswith('.csv'):
                data = pd.read_csv(file_name)
            elif file_name.endswith('.txt'):
                data = pd.read_csv(file_name, delimiter=';', header=None,
                                   names=['x', 'y'])
            return data
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


# PREPROCESS DATA FROM SOURCE FILE # TODO adapt text parsing - just an example
def read_values_from_data(data):
    if data is not None:
        try:
            x = data['x'].values
            y = data['y'].values
            return x, y
        except Exception as e:
            text_label.setText("Error extracting 'x' and 'y' values: "
                               + str(e))

            return None, None
    else:
        return None, None


# PLOTTING DATA FOR PLOT 4 # TODO adapt - just an example
def plotting_p4():
    global animation_active
    data = load_data()
    x, y = read_values_from_data(data)

    clear_all_plots()

    if x is not None and y is not None:
        p4.plot(x, y, pen=None, symbol='o')
        text_label.setText("You can load new data or run the algorithms")
        btn_step.setEnabled(True)
        btn_result.setEnabled(True)
        btn_run.setEnabled(True)
        btn_reset.setEnabled(True)
    else:
        btn_step.setEnabled(False)
        btn_result.setEnabled(False)
        btn_run.setEnabled(False)
        btn_reset.setEnabled(False)

    btn_loadData.setEnabled(True)
    animation_active = False


# QUICK RUN ANIMATION

def update_curve(p, x, y, i):
    global animation_active, animation_timer
    if i < len(x):
        p.plot(x[:i+1], y[:i+1], pen='r')
        p.plot([x[i]], [y[i]], pen=None, symbol='o', symbolSize=10,
               symbolBrush='b')
        animation_timer.i += 1
    else:
        animation_timer.stop()
        animation_active = False
        btn_loadData.setEnabled(True)


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
    global data, animation_active, animation_timer

    p1.clear()
    p2.clear()
    p3.clear()

    # Checks if data had successfully been loaded and whether data processing
    # can commence
    if data is None or animation_active:
        return

    # TODO modify according to task - just an example
    # Algorithms will determine the points x, y to be displayed

    x, y = read_values_from_data(data)

    # In order to have animations run one after another (which is necessary
    # if they share the same timer
    total_duration_p1 = len(x) * animation_interval
    total_duration_p2 = len(x) * animation_interval
    total_duration_p1p2 = total_duration_p1 + total_duration_p2

    try:
        animation_start(p1, x, y, "Algorithm 1 is used")
    except Exception as e:
        text_label.setText("Error animating algorithm 1, Continuing with next"
                           "algorithm")
        print("Error during animation: " + str(e))
    try:
        QtCore.QTimer.singleShot(total_duration_p1, lambda: animation_start(
            p2, x, y, "Algorithm 2 is used"))
    except Exception as e:
        text_label.setText("Error animating algorithm 2, Continuing with next"
                           "algorithm")
        print("Error during animation: " + str(e))
    try:
        QtCore.QTimer.singleShot(total_duration_p1p2, lambda: animation_start(
            p3, x, y, "Algorithm 3 is used"))
    except Exception as e:
        text_label.setText("Error animating algorithm 3")
        print("Error during animation: " + str(e))

    animation_active = False


def show_results():
    global data

    if data is None:
        return

    text_label.setText("Showing results with \nAlgorithm 1 (top left), \n"
                       "Algorithm 2 (top right) and \n"
                       "Algorithm 3 (bottom left)")

    # TODO modify according to task - just an example
    # Algorithms will determine the points x, y to be displayed

    x, y = read_values_from_data(data)

    p1.clear()
    p2.clear()
    p3.clear()

    def plot_all(p, x, y):
        p.plot(x, y, pen='r', symbol='o', symbolSize=10, symbolBrush='b')

    plot_all(p1, x, y)
    plot_all(p2, x, y)
    plot_all(p3, x, y)


def step_through():
    global step_index, current_plot, data

    if data is None:
        return

    # TODO modify according to task - just an example
    # Algorithms will determine the points x, y to be displayed

    x, y = read_values_from_data(data)

    p1.clear()
    p2.clear()
    p3.clear()

    if current_plot == 1:
        p = p1
    elif current_plot == 2:
        p = p2
    else:
        p = p3

    if step_index < len(x):
        p.plot(x[:step_index+1], y[:step_index+1], pen='r')
        p.plot([x[step_index]], [y[step_index]], pen=None, symbol='o',
               symbolSize=10, symbolBrush='b')
        step_index += 1
        btn_step.setText("Next Step")
        text_label.setText(str(step_index) + " points connected")
    else:
        if current_plot < 3:
            current_plot += 1
            step_index = 0
            text_label.setText("Continuing with the next algorithm")
        else:
            btn_step.setText("Step Through")
            text_label.setText("Step Through is completed")
            btn_loadData.setEnabled(True)


###########################
# UI EVENT BUTTON HANDLING
###########################

btn_loadData.clicked.connect(plotting_p4)
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
