from tkinter import *
from time import *
from math import *
import re
tk = Tk()
screen = Canvas(tk, width=600, height=600, background="white") #default screen size

print("Welcome to the Graphing Calculator Toolbox by Luke Zhang and Hima Seth")

def input_screen_size(size): #let user choose the screen size
  global screen_size
  screen_size = size

  global screen
  screen = Canvas(tk, width=screen_size, height=screen_size, background="white")
  screen.pack()

getScaleFactor = lambda a, b : a/b

################ NEW FUNCTION ################
def get_values(eqn): #gets values of a, b, and c - works with decimals too
  eqn.replace(" ", "") #remove any spaces
  eqn += " " #add whitespace to signify end of string
  index = 0
  index2 = None

  #Find value of a
  try: index = eqn.index('x^2')
  except: a = 0 #error: can't find a
  else:
    try: a = float(eqn[0:index]) if index > 0 else 1
    except ValueError: a = -1
  
  #Find value of b
  try: index2 = re.search(r"(x(\+|-| ))", eqn).start() #x and (+ or - or whitespace)
  except: b = 0 #error: can't find b
  else:
    try: b = float(eqn[index+3:index2]) if a != 0 else float(eqn[index:index2])
    except: b = 1

  #find value of c
  try: index = re.search(r"(\+|-)(\d)*(\d |(\.(\d)*(\d )))", eqn).start() #too long to explain
  except: c = 0 #error: can't find c
  else: c = float(eqn[index:-1])

  #return dictionary of values
  return {"a" : a, "b" : b, "c" : c}

################ NEW PROCEDURE #################
def draw_numbers(initial_values, scaled_values, distance, x, y): #draw numbers along the axises
  for i in range(int(distance)//int(scaled_values['xIncrement'])+1): #x Numbers
    screen.create_text(scaled_values['xMin']+i*scaled_values['xIncrement'], y, text = initial_values['xMin']+i*initial_values['xIncrement']) 

  for i in range(int(distance)//int(scaled_values['yIncrement'])+1): #y numbers
    screen.create_text(x, scaled_values['yMin']-i*scaled_values['yIncrement'], text = initial_values['yMin']+i*initial_values['yIncrement'])

################ NEW PROCEDURE ################
def draw_axes(initial_values, scaled_values): #draw x and y axis
  xAxis, yAxis = False, False
  for i in range(screen_size): #Plot x and y axis by going through the entire screen and finding their locations
    if initial_values['xMin']+i*initial_values['xIncrement'] == 0: #Y Axis
      screen.create_line(scaled_values['xMin']+i*scaled_values['xIncrement'], 0, scaled_values['xMin']+i*scaled_values['xIncrement'], screen_size, width = 2.5)
      yAxis = True

    if initial_values['yMin']+i*initial_values['yIncrement'] == 0: #X Axis
      screen.create_line(0, scaled_values['yMin']-i*scaled_values['yIncrement'], screen_size, scaled_values['yMin']-i*scaled_values['yIncrement'], width = 2.5), 
      xAxis = True
    
    if xAxis and yAxis: break

################ NEW FUNCTION ################
def get_xy(initial_values, scaled_values, scaleFactor): #get origin of cartesian plane in relation to the screen.''
  xAxis, yAxis = False, False

  for i in range(initial_values['xMax']-initial_values['xMin']): #Plot x and y axis by going through the entire screen and finding their locations
    if initial_values['xMin']+i == 0: #Y Axis
      yAxis = True
      x = scaled_values['xMin']+i*scaleFactor-25 #x refers to the x coordinate which the y labels should be at

    if initial_values['yMin']+i == 0: #X Axis
      xAxis = True
      y = scaled_values['yMin']-i*scaleFactor+25 #y refers to the y coordinate which the x labels should be at
    
    if xAxis and yAxis: break

  if not xAxis and initial_values["yMax"] <= 0: y = screen_size-25 #If no x Axis drawn and viewport is below the x axis
    
  elif not xAxis and initial_values["yMin"] >= 0: y = 25 #If no x Axis drawn and viewport is above x axis
    
  if not yAxis and initial_values["xMin"] >= 0: x = 25 #If no y Axis drawn and viewport is to the right of the y axis
    
  elif not yAxis and initial_values["xMax"] <= 0: x = screen_size-25 #If no y Axis drawn and viewport is to the left of the y axis
    

  return [x, y]

################ NEW FUNCTION ################
def draw_grid(xMin_local, xMax_local, yMin_local, xIncrement, yIncrement): #draw cartesian plane
  global xMin
  global xMax
  global yMax
  global yMin
  global distance
  global scaleFactor

  xMin = xMin_local
  xMax = xMax_local
  yMin = yMin_local

  distance = xMax_local - xMin_local
  yMax = yMin_local + distance
  scaleFactor = getScaleFactor(screen_size, distance)

  ## Width of squares to determine scaling for points when plotting
  global widthX
  global widthY
  widthX = screen_size/(xMax_local-xMin_local) 
  widthY = screen_size/(yMax-yMin_local)
  
  initial_values = {"xMin": xMin_local, "xMax": xMax_local, "yMin": yMin_local, "yMax": yMax, "xIncrement": xIncrement, "yIncrement": yIncrement} #dict of initial values

  #multiply all values by the scale factor
  xMin_local *= scaleFactor
  xMax_local *= scaleFactor
  yMin_local *= scaleFactor
  yMax *= scaleFactor
  distance *= scaleFactor
  yIncrement *= scaleFactor
  xIncrement *= scaleFactor
  
  #move the plane towards the 0, 0 of the screen
  xMax_local -= xMin_local
  yMax -= yMin_local
  xMin_local = 0
  yMin_local = 0
  yMin_local, yMax = yMax, yMin_local

  scaled_values = {"xMin": xMin_local, "xMax": xMax_local, "yMin": yMin_local, "yMax": yMax,"xIncrement": xIncrement, "yIncrement": yIncrement} #dict of scaled values

  for i in range(int(distance)//int(xIncrement)): #x lines
    screen.create_line(xMin_local+i*xIncrement, 0, xMin_local+i*xIncrement, yMin_local, width = 1)
  for i in range(int(distance)//int(yIncrement)): #y lines
    screen.create_line(0, yMax+i*yIncrement, xMax_local, yMax+i*yIncrement, width = 1)

  tempVar = get_xy(initial_values, scaled_values, scaleFactor) #get origin
  x = tempVar[0]
  y = tempVar[1]

  draw_axes(initial_values, scaled_values) #draw x and y axis thicker
  draw_numbers(initial_values, scaled_values, distance, x, y) #draw numbers and put them against the axis, unless the axis is off screen

################ NEW FUNCTION ################
def makeTableofValues (numPoints): #use arguments to make a table of values
    global numbPoints
    numbPoints = numPoints
    equation = str(input("Enter equation: y="))

    #uses the get_values function to get the a,b,c values
    values = get_values(equation)

    #define abc values in variables
    a = values['a']
    b = values['b']
    c = values['c']
    xValues = []
    yValues = []
    xIncrease = (xMax-xMin)/numPoints
    x = xMin

    #uses abc values to find x and y values
    for i in range  (numPoints):
      yValue = a*x**2 + b*x + c
      xValues.append (x) ##Scale the points based on the origin -- we don't have an origin yet
      yReal = yValue #to scale, multiply by the width of the Ysquares and add it to the origin
      yValues.append (yReal)
      x = x + xIncrease

    return (xValues, yValues)

################ NEW PROCEDURE ################
def plotPoints(xValues, yValues): #plot points from TOV
  xPlotValue = []
  yPlotValue = []
  pointsPlot = []

  xPlotValue = list(map(lambda x: x*scaleFactor, xValues)) #Multiply x values by scale factor
  yPlotValue = list(map(lambda x: x*scaleFactor*-1, yValues)) #Multiply y values by scale factor and invert it like the y axis

  xPlotValue = list(map(lambda x: x-xMin*scaleFactor, xPlotValue)) #move x values based on origin
  yPlotValue = list(map(lambda x: x-yMin*scaleFactor, yPlotValue))  #move y values based on origin

  for t in range(numbPoints-1): #plot the points
      pointsPlot.append(screen.create_line (xPlotValue[t], yPlotValue[t], xPlotValue[t+1], yPlotValue[t+1], fill = "red", smooth= "true", width = 3))

  print("Graphing Complete")
