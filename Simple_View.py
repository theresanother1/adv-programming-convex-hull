import graphics as graphics

# slow down visualization time
import numpy as np

SLOWDOWN_PER_STEP = 0.25


def draw_points_init(points: np.ndarray, win):
    # loop to draw all points in list
    for i in points:
        gPoint = graphics.Circle(graphics.Point(i[0], i[1]), 5)
        gPoint.setFill("blue")
        gPoint.draw(win)


def init_window(x, y):
    # initialize graphics window globally
    win = graphics.GraphWin("Convex Hull", 1000, 1000)
    win.setCoords(x[0], y[0], x[1], y[1])
    win.master.resizable(True, True)
    win.setBackground("white")
    return win


# Graphical Functions to display points

def highlight_point(p: np.ndarray, win):
    print(p)
    hullPoint = graphics.Circle(graphics.Point(p[0], p[1]), 7.5)
    hullPoint.setFill("yellow")
    hullPoint.draw(win)


def join_points(a: np.ndarray, b: np.ndarray):
    line = graphics.Line(graphics.Point(a[0], a[1]), graphics.Point(b[0], b[1]))
    return line


'''
    # Generate points by clicking on the canvas
    pointList = []
    for _ in range(NUM_POINTS):
        p = win.getMouse()
        x, y = p.getX(), p.getY()
        pointList.append([x,y])
        print(x, y)
        win.redraw()
    '''