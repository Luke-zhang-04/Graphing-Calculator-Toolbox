from GraphingCalculatorToolbox import graphingCalculator


graph = graphingCalculator(int(input("Please enter Screen Size: "))) #user inputs screen size

graph.draw_axes(int(input("Please enter xMin: ")),int(input("Please enter xMax: ")),int(input("Please enter yMin: ")),int(input("Please enter increment for x: ")),int(input("Please enter increment for y: "))) #User draws up a grid

TOV = graph.makeTableofValues (int(input("Please enter number of points: ")), input("Enter equation: y=")) #Using given data, user enters desired number of points and an equation (in the function)
#graph.plotPoints(TOV[0], TOV[1]) #makeTableofValues returns a tuple of a list of x values and a list of y values
graph.plotPoints()

graph.screen.update()
graph.screen.mainloop()
