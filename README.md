## ADV- Prog Project Convex Hull MAI 2024

The following Repo compares the Gift Wrapper algorithm against
the Quickhull algorithm regarding their time complexity. Both are algorithms
which try find the convex hull of an object in the best feasible time in order to
approximate an object in space as best as possible. The Gift Wrapper algorithm checks
all points in space on each iteration, while the Quickhull algorithm favors a
recursive approach, dismissing many points on each iteration.

## Gift Wrapper

The Gift Wrapper algorithm has a theoretical complexity of O(nh). It is a
simple method to find a convex hull out of dataset is by using the Gift Wrapper
algorithm. The algorithm starts by searching for the leftmost point in a set
of points, which often has the lowest x-coordinate. Once the leftmost point is
found the algorithm will start to scan through all the other points to look for
the smallest positive angle. This point is then added to the hull. The whole
process is going to be repeated until the algorithm returns to the starting point.

## Quickhull

The Quickhull has a theoretical O(n log n) (average case), O(n2) (worst
case). Its first step divides the solution space into two parts using a line with
the minimum and maximum point on the x-Axis. Next a triangle is created
with the farthest away points with the part left of the line. The covered area
is within and points inside are automatically checked. The farthest points are
on the hull. Continues with two lines - current left and max distance point and
max distance point and current right. Continue recursively until all points are
either on hull or within area.

## Interaction with the GUI

![GUI](https://i.imgur.com/eC3zltV.png)

The GUI helps the user to interact with the Algorithms and to measure cloud points and the results are then vizualized.
The user has the possible to choose between diffrent kind of buttons.  


Quick Run          |  Step Through    | Show Result
:-------------------------:|:-------------------------:|:-------------------------:
![QuickRun](https://s6.ezgif.com/tmp/ezgif-6-96e163d444.gif) | ![StepThrough](https://s6.ezgif.com/tmp/ezgif-6-d55e53384c.gif) | ![ShowResult](https://s6.ezgif.com/tmp/ezgif-6-19d7fb2403.gif)
The "Quick run" button is been used to visualize automaticaly the alogrithm step by step. | An interactive way to visualize the algorithm step by step can be approached by the "Step Through" button. | The "Show Result" Button is just showing the convex hull points and measures the time the algorithm needed. 

At the textfield a random number can be entered to create a random generated cloud point. Otherwise a file can also be uploaded by using the "Load new Data" Button. The expected Dataformat can be found at the Notes.

## List of libraries needed to build and run

See File ./buildinfo/ListOfLibrariesForAPRGEnv.yml

NOTES:

    - The GUI will only accept points <= 10000, if you want to see execution times for more points, 
      please start the console application in main.py. The GUI is in aprg_Proj2-Gr7_202409xx.py.
      - data from file (.txt) with format first line: number of points second ... n: points in format x, y 
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
