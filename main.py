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
        self.relPos: Vector = currentPos

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
                vectorForce += (dir * force)

        acceleration = vectorForce / self.mass
        self.nextVel = self.currentVel + (acceleration * time)



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
    def Update(self,time) -> None:


        self.currentVel = self.nextVel
        self.currentPos += (self.currentVel * time)
        self.relPos += self.currentVel * scale * time
        if self.name == "earth":
            print(self.relPos.GetVector(), "\n")
        else:
            print(self.relPos.GetVector() )


app = tkinter.Tk()
width = app.winfo_screenwidth()
height = app.winfo_screenheight()
app.destroy()

HEIGHT = height
WIDTH = width
"""
planet = Actor("planet", (250,250))
planet.scale = 0.01
image = pygame.image.load('CarWhiteDragon256.png').convert_alpha()
"""
x = width/2
y = height/2
xOffset = 0
yOffset = 0
scale = 0.0001
right = True
fullscreen = False
objects = []
objects.append(Object("Sun","#ffdf22", 1989000000000000000000000000000,695700000,Vector(100000,0)))
objects.append(Object("earth", "#00ff00", 5972000000000000000000000, 6000000))
def draw():
    global fullscreen
    if not fullscreen:
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        fullscreen = True
    screen.fill("#000010")
    for object in objects:
        screen.draw.filled_circle(object.relPos.GetVector(), object.GetRadius() * scale,object.GetColour())

def on_mouse_down(pos,button):
    global scale
    scaleSpeed = 1.1
    if button == mouse.WHEEL_UP:
        for object in objects:
            xDiff = (object.relPos.x - pos[0]) * scaleSpeed
            yDiff = (object.relPos.y - pos[1]) * scaleSpeed
            object.relPos.x = pos[0] + xDiff
            object.relPos.y = pos[1] + yDiff
        scale *= scaleSpeed
    if button == mouse.WHEEL_DOWN:
        for object in objects:
            xDiff = (object.relPos.x - pos[0]) / scaleSpeed
            yDiff = (object.relPos.y - pos[1]) / scaleSpeed
            object.relPos.x = pos[0] + xDiff
            object.relPos.y = pos[1] + yDiff

        scale /= scaleSpeed


def on_mouse_move(rel, buttons):
    if mouse.LEFT in buttons:
        for object in objects:
            object.relPos.x += rel[0]
            object.relPos.y += rel[1]




def update(time):
    for object in objects:
        object.CalculateNextPos(time)
    for object in objects:
        object.Update(time)

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
