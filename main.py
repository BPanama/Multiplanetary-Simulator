import math

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

    # Returns the current mass as a float
    def GetMass(self) -> float:
        return self.mass

    # Updates the currentPos and currentVel of the object
    def Update(self) -> None:
        return

# Vector Test

# Tests the non "__x__" functions and initialisation
vector1 = Vector(3, 4)

print("x:", vector1.x, ", y:", vector1.y)
print(vector1.GetVector())
print(vector1.GetMagnitude())
print(vector1.GetNormalized().GetVector())

# Tests the "__x__" functions
vector2 = Vector(3, 4)

vector3 = vector1 + vector2
print(vector3.GetVector())
vector3 = vector1 - vector2
print(vector3.GetVector())

# Object Test
object1 = Object("earth","green",5972000000000000000000000, 6000000)
print(
    f"Name: {object1.name}\n"
    f"Colour: {object1.colour}\n"
    f"Mass: {object1.mass}\n"
    f"Radius: {object1.radius}\n"
    f"Current Position: {object1.currentPos.GetVector()}\n"
    f"Current Velocity: {object1.currentVel.GetVector()}"
)
