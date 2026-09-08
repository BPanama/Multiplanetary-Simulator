import math

import pgzrun
import pygame
import time
import random
import tkinter


# Vector class needed for calculations
class Vector:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: float = 0
        self.y: float = 0
        self.SetVector(x, y)

    # Returns the Vector as a list
    def GetVector(self):
        return [self.x, self.y]

    def SetVector(self,x,y) -> None:
        if( (type(x) == int or type(x) == float) and (type(y) == int or type(y) == float) ):
            self.x = x
            self.y = y
        else:
            raise "Vectors need to be a float or int"

    # Returns the magnitude of the vector as a single float
    def GetMagnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # Returns the normalized vector as a vector
    def GetNormalized(self):
        magnitude = self.GetMagnitude()
        return Vector(self.x / magnitude, self.y / magnitude)

    # Adds 2 Vectors using Vector1 + Vector2
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    # Takes away 2 Vectors using Vector1 - Vector2
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector(x,y)

    def __truediv__(self, other):
        x = self.x / other
        y = self.y / other
        return Vector(x,y)


# Object Class for all the planets, stars, etc
class Object:
    letterList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

    def __init__(self, name, colour, mass, radius, currentPos=Vector(), currentVel=Vector()):
        self.name: str = name
        self.colour: str = (00,00,00)
        self.SetColour(colour)
        self.mass: float = 10000
        self.SetMass(mass)
        self.radius: float = 1000
        self.SetRadius(radius)
        self.currentPos: Vector = currentPos
        self.currentVel: Vector = currentVel
        self.force: Vector = Vector()
        self.nextPos: Vector = Vector()
        self.nextVel: Vector = Vector()

    # Calculates the forces and gets the next position
    def CalculateNextPos(self,time) -> None:

        G = 0.00000000006674
        vectorForce =  Vector(0,0)
        for object in objects:
            difference = object.GetPos() - self.GetPos()

            distance = difference.GetMagnitude()
            if distance != 0:
                dir = difference.GetNormalized()
                force = (G * self.GetMass() * object.GetMass())/(distance ** 2)
                vectorForce += dir * force

        acceleration = vectorForce / self.mass
        self.nextVel = self.currentVel + acceleration * time


    # Returns current position as a Vector
    def GetPos(self) -> Vector:
        return self.currentPos

    def GetColour(self) -> str:
        return self.colour

    # Makes sure colour variable is in format #xxxxxx where x is between 0 and f for a hexadecimal format
    def SetColour(self, colour):
        if (colour[0] != "#" or len(colour) != 7):
            raise "Colour needs to be formatted correctly"
        else:
            for char in colour[1:]:
                if char.lower() not in self.letterList:
                    raise "Colours only go from 0-f"
            self.colour = colour

    # Returns the current mass as a float
    def GetMass(self) -> float:
        return self.mass

    # Makes sure the mass variable is a positive float
    def SetMass(self, mass) -> None:
        try:
            mass = float(mass)
            if (mass > 0):
                self.mass = mass
            else:
                raise
        except:
            raise "Mass has to be a positive float"

    # Returns the current radius as a float
    def GetRadius(self) -> float:
        return self.radius

    # Makes sure the mass variable is a positive float
    def SetRadius(self, radius) -> None:
        if(type(radius) != float and type(radius) != int and radius <= 0):
            print("No")

        else:
            self.radius = radius

    # Updates the currentPos and currentVel of the object
    def Update(self, time) -> None:


        self.currentVel = self.nextVel
        self.currentPos += self.currentVel * time

# Finds the width and height of the screen
app = tkinter.Tk()
width = app.winfo_screenwidth()
height = app.winfo_screenheight()
app.destroy()

#Sets the width and height to remove "large" mouse
HEIGHT = height
WIDTH = width

#Sets initial variables
z = 1
fullscreen = False
offset  = Vector()
center = Vector(width/2,height/2)
objects = []

"""objects.append(Object("earth", "#00ff00", 1000000, 500))
objects.append(Object("Sun","#ffdf22", 1000000,500,Vector(7000,-1000)))
objects.append(Object("One","#ffdf88", 1000000,500,Vector(5000,3000)))"""


"""for i in range(200):
    objects.append(Object(str(i),"#ffffff",random.randint(5000,5000000000),random.randint(200,1000),Vector(random.randint(-10000,10000),random.randint(-10000,10000))))"""

objects.append(Object("One","#ffffff",1,2,Vector(3,0),Vector(0,0.1)))
objects.append(Object("Two","#ffffff",1,2,Vector(-3,0),Vector(0,-0.1)))

# Draws the objects onto the screen
def draw():
    # Makes the game fullscreen on the first frame, fixes it not going fullscreen when out of this and the violent flashes when not in the if statement
    global fullscreen
    if not fullscreen:
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        fullscreen = True

    screen.fill("#000010")
    for object in objects:
        pos = ProjectToScreen(object.currentPos)
        rad = object.GetRadius()/z
        if not( pos[0] - rad >width or pos[0] + rad < 0 or pos[1] + rad < 0 or pos[1] - rad > height or rad < 1):

            screen.draw.filled_circle(pos , rad, object.GetColour())

#Turns the object position into the rendered position using the projection formula
def ProjectToScreen(objectPos:Vector) -> Vector:
    return ((objectPos- offset) / z + center).GetVector()

# Zooms in and out based on the mouse position
def on_mouse_down(pos,button):
    global z,offset, center
    scaleSpeed = 1.1
    # Moves the offset to look the same when center changes
    mouseDiff = Vector(pos[0] - center.x,  pos[1] - center.y)
    offset += mouseDiff * z
    #Changes the center into the mouse position
    center = Vector(pos[0],pos[1])
    #Zooms in/out
    if button == mouse.WHEEL_UP:
        z /= scaleSpeed
    if button == mouse.WHEEL_DOWN:
        z *= scaleSpeed

# Pan the simulation
def on_mouse_move(rel, buttons):
    global offset
    if mouse.LEFT in buttons:
        offset.x -= rel[0] * z
        offset.y -= rel[1] * z


# Updates the simulation
def update(time):
    for object in objects:
        object.CalculateNextPos(time*100)
    for object in objects:
        object.Update(time*100)

pgzrun.go()

"""
#region Variable Tests

object1 = Object("earth", "#ffffff", 5972000000000000000000000, 6000000)
print("\nColour Tests \n")
try:
    object1.SetColour("orange")
    print("Accepted")
except:
    print("Rejected")

try:
    object1.SetColour("#000000")
    print("Accepted")
except:
    print("Rejected")

try:
    object1.SetColour("#555555")
    print("Accepted")
except:
    print("Rejected")

try:
    object1.SetColour("#GGGGGG")
    print("Accepted")
except:
    print("Rejected")

try:
    object1.SetColour("test")
    print("Accepted")
except:
    print("Rejected")

print("\nMass Tests \n")
try:
    object1.SetMass(0)
    print("Accepted")
except:
    print("Rejected")
try:
    object1.SetMass(10000000000)
    print("Accepted")
except:
    print("Rejected")
try:
    object1.SetMass(-5)
    print("Accepted")
except:
    print("Rejected")
try:
    object1.SetMass("test")
    print("Accepted")
except:
    print("Rejected")

print("\nRadius Tests \n")
try:
    object1.SetRadius(0)
    print("Accepted")
except:
    print("Rejected")
try:
    object1.SetRadius(10000000000)
    print("Accepted")
except:
    print("Rejected")
try:
    object1.SetRadius(-5)
    print("Accepted")
except:
    print("Rejected")
try:
    object1.SetRadius("test")
    print("Accepted")
except:
    print("Rejected")

print("\nVector Tests \n")

try:
    testVector = Vector(0,0)
    print("Accepted")
except:
    print("Rejected")
try:
    testVector = Vector(100000, 100000)
    print("Accepted")
except:
    print("Rejected")
try:
    testVector = Vector(-10, -10)
    print("Accepted")
except:
    print("Rejected")
try:
    testVector = Vector("test", "test")
    print("Accepted")
except:
    print("Rejected")

#endregion
"""
