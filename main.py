import math

import pgzrun
import pygame
import time
import random
import tkinter
letterList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
def ColourPick(col1,col2,rad1,rad2):
    # Changes from 2-digit hex to integers
    col1Red = int(col1[1:3],16)
    col1Green = int(col1[3:5],16)
    col1Blue = int(col1[5:7],16)
    col2Red = int(col2[1:3],16)
    col2Green = int(col2[3:5],16)
    col2Blue = int(col2[5:7],16)
    newColRed = int((col1Red*rad1 + col2Red*rad2)//(rad1+rad2))
    newColGreen = int((col1Green*rad1 + col2Green*rad2)//(rad1+rad2))
    newColBlue = int((col1Blue * rad1 + col2Blue * rad2) // (rad1 + rad2))
    newCol = f"#{hex(newColRed).split('x')[1].zfill(2)}{hex(newColGreen).split('x')[1].zfill(2)}{hex(newColBlue).split('x')[1].zfill(2)}"
    return newCol

# Returns the new radius
def RadPick(rad1,rad2):
    rad3 = math.sqrt(rad1**2 + rad2 **2)
    return rad3

print(ColourPick("#ffffff","#000000",3,2))
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
        self.acceleration = Vector()
        self.isDestroyed = False

    # Calculates the forces and gets the next position
    def CalculateNextPos(self,time) -> None:

        G = 0.00000000006674
        vectorForce =  Vector(0,0)
        for object in objects:
            difference = object.GetPos() - self.GetPos()

            distance = difference.GetMagnitude()
            if distance != 0:
                if distance >= self.radius + object.radius:
                    dir = difference.GetNormalized()
                    force = (G * self.GetMass() * object.GetMass())/(distance ** 2)
                    vectorForce += dir * force
                else:
                    self.Collide(object)


        self.acceleration = vectorForce / self.mass

        self.nextVel = self.currentVel + self.acceleration * time


    # Returns current position as a Vector
    def GetPos(self) -> Vector:
        return self.currentPos

    def GetColour(self) -> str:
        return self.colour

    # Makes sure colour variable is in format #xxxxxx where x is between 0 and f for a hexadecimal format
    def SetColour(self, colour):
        global letterList
        if (colour[0] != "#" or len(colour) != 7):
            raise "Colour needs to be formatted correctly"
        else:
            for char in colour[1:]:
                if char.lower() not in letterList:
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

        self.currentPos +=  (self.currentVel + self.nextVel) * time /2
        self.currentVel = self.nextVel
    def Collide(self,other):
        global newObjects
        if( not other.isDestroyed):
            self.isDestroyed = True
            other.isDestroyed = True
            newName = self.name + other.name
            newColour = ColourPick(self.colour,other.colour,self.radius,other.radius)
            newMass  = self.mass + other.mass
            newRadius = RadPick(self.radius, other.radius)
            newPos = (self.currentPos * self.radius + other.currentPos * other.radius) / (self.radius + other.radius)
            newVel = (self.currentVel * self.mass + other.currentVel * other.mass) / newMass
            newObjects.append(Object(newName,newColour,newMass,newRadius,newPos,newVel))



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

# Sun
objects.append(Object("Sun", "#FDB813", 1988500000000000000000000000000, 695700000,
                      Vector(0, 0), Vector(0, 0)))

# Planets
objects.append(Object("Mercury", "#A6A6A6", 330110000000000000000000, 2439700,
                      Vector(57910000000, 0), Vector(0, 47870)))

objects.append(Object("Venus", "#E6C27A", 4867500000000000000000000, 6051800,
                      Vector(108200000000, 0), Vector(0, 35020)))

objects.append(Object("Earth", "#2878B5", 5972200000000000000000000, 6371000,
                      Vector(149600000000, 0), Vector(0, 29780)))

objects.append(Object("Mars", "#C1440E", 641710000000000000000000, 3389500,
                      Vector(227900000000, 0), Vector(0, 24077)))

objects.append(Object("Jupiter", "#D2B48C", 1898200000000000000000000000, 69911000,
                      Vector(778500000000, 0), Vector(0, 13070)))

objects.append(Object("Saturn", "#EAD6A6", 568340000000000000000000000, 58232000,
                      Vector(1433000000000, 0), Vector(0, 9680)))

objects.append(Object("Uranus", "#7FFFD4", 86810000000000000000000000, 25362000,
                      Vector(2872000000000, 0), Vector(0, 6800)))

objects.append(Object("Neptune", "#4166F5", 102413000000000000000000000, 24622000,
                      Vector(4495000000000, 0), Vector(0, 5430)))

# Dwarf planet
objects.append(Object("Pluto", "#C9B29B", 13030000000000000000000, 1188300,
                      Vector(5906000000000, 0), Vector(0, 4740)))

# Earth's Moon
objects.append(Object("Moon", "#BDBDBD", 73420000000000000000000, 1737400,
                      Vector(149984400000, 0), Vector(0, 30802)))


"""
for i in range(500):
    objects.append(Object(str(i),f"#{hex(random.randint(0,255)).split('x')[1].zfill(2)}{hex(random.randint(0,255)).split('x')[1].zfill(2)}{hex(random.randint(0,255)).split('x')[1].zfill(2)}",random.randint(5000,5000000000),random.randint(200,1000),Vector(random.randint(-100000,100000),random.randint(-100000,100000)),Vector(random.randint(-10000,10000),random.randint(-10000,10000))))
"""
"""
objects.append(Object("One","#ff0000",3000000000000000000000000000000,20000000000,Vector(28867513459.48,0),Vector(0,63281.75)))
objects.append(Object("Two","#00ff00",3000000000000000000000000000000,20000000000,Vector(-14433756729.74,25000000000.0),Vector(-54803.60,-31640.88)))
objects.append(Object("Three","#0000ff",3000000000000000000000000000000,20000000000,Vector(-14433756729.74,-25000000000.0),Vector(54803.60,-31640.88)))
"""
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
newObjects = []
def update(time):
    global newObjects, objects
    print(objects[1].currentPos.GetVector())
    newObjects = []
    for object in objects:
        object.CalculateNextPos(time*1000000)
    for object in objects:
        object.Update(time*1000000)
    for object in objects:
        if (not object.isDestroyed):
            newObjects.append(object)
    objects = newObjects

pgzrun.go()
