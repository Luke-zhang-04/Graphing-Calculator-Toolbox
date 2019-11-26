from GraphingCalculatorToolbox import *

input_screen_size(int(input("Please enter Screen Size: "))) #user inputs screen size

draw_grid(int(input("Please enter xMin: ")),int(input("Please enter xMax: ")),int(input("Please enter yMin: ")),int(input("Please enter increment for x: ")),int(input("Please enter increment for y: "))) #User draws up a grid

TOV = makeTableofValues (int(input("Please enter number of points: "))) #Using given data, user enters desired number of points and an equation (in the function)
plotPoints (TOV[0], TOV[1]) #makeTableofValues returns a tuple of a list of x values and a list of y values

screen.update()
screen.mainloop()
