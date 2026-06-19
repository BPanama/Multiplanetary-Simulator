import math
import pgzrun

# Vector class needed for calculations
class Vector:
    def __init__(self, x: float = 0, y: float = 0):
        self.x: float = x
        self.y: float = y

    # Returns the Vector as a list
    def GetVector(self) -> list[2]:
        return [self.x, self.y]

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

# Object Class for all the planets, stars, etc
class Object:
    letterList = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    def __init__(self, name, colour, mass, radius, currentPos = Vector(), currentVel = Vector()):
        self.name: str = name
        self.colour: str = colour
        self.mass: float = mass
        self.radius: float = radius
        self.currentPos: Vector = currentPos
        self.currentVel: Vector = currentVel
        self.force: Vector = Vector()
        self.nextPos: Vector = Vector()
        self.nextVel: Vector = Vector()

    # Calculates the forces and gets the next position
    def CalculateNextPos(self) -> None:
        return

    # Returns current position as a Vector
    def GetPos(self) -> Vector:
        return self.currentPos

    def GetColour(self):
        return self.colour

    def SetColour(self,colour):
        if(colour[0] != "#" or len(colour) != 7):
            raise "Colour needs to be formatted correctly"
        else:
            for char in colour[1:]:
                if char.lower() not in self.letterList:
                    raise "Colours only go from 0-f"



    # Returns the current mass as a float
    def GetMass(self) -> float:
        return self.mass

    # Updates the currentPos and currentVel of the object
    def Update(self) -> None:
        return


object1 = Object("earth","green",5972000000000000000000000, 6000000)

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