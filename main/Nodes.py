import math

# COLOR : NONE(GREY), RED, BLUE, GREEN, 

class Node:
    def __init__(self, pixel_position, pixel_colors={}, color='grey'):
        self.size = len(pixel_position)
        # used if nodes are all same colors
        if (pixel_colors == {}):
            self.color = color
        else:
            self.color = None
        self.associated_nodes = []
        self.pixel_positions = pixel_position
        self.pixel_colors = pixel_colors


    # connection_type = HORIZONTAL OR VERTICAL
    def AddAssociatedNode(self, new_node, connection_type):
        if (new_node in self.associated_nodes):
            return
        self.associated_nodes.append((new_node, connection_type))

    def GetAssociatedNode(self):
        return self.associated_nodes
    
    def GetPixelPositions(self):
        return self.pixel_positions

    def GetApproximatePixelPos(self):
        return self.pixel_positions[0]

    def BiggerSize(self, size):
        if (size >= self.size):
            return True
        return False
    
    #check if node is of same color
    def CheckUniColor(self):
        if self.color == None:
            origi = self.pixel_colors[self.pixel_positions[0]]
            for color in self.pixel_colors.values():
                if color != origi:
                    return False
            return True

        else:
            return True
    
    
    def Rotate(origin, point, angle, decimals=5):
        def clean(value):
            value = round(value, decimals)
            # Avoid -0.0: if very close to zero → 0
            if abs(value) < 1e-10:
                return 0
            # If integer value: returns int
            if value == int(value):
                return int(value)
            return value

        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return clean(qx), clean(qy)


    def RotateNode(self, angle):
        if not self.pixel_positions:
            return

        # Calculating the node center (barycentre)
        x_sum = sum(p[0] for p in self.pixel_positions)
        y_sum = sum(p[1] for p in self.pixel_positions)
        n = self.size
        center = (x_sum / n, y_sum / n)

        # Apply rotation to each pixel
        self.pixel_positions = [Node.Rotate(center, p, angle) for p in self.pixel_positions]

    # check if form is fillet or not (if has hole in it)
    def CheckIfHole():
        pass


#Test Area

# Create a square node centered around (1, 1)
# node = Node([(0, 0), (0, 2), (2, 2), (2, 0)])
# node.size = len(node.pixel_positions)
# node.color = 'BLUE'

# print("Before rotation :")
# for p in node.pixel_positions:
#     print(p)

# # 270-degree rotation (3pi/2 radians)
# node.RotateNode((3*math.pi)/2)

# print("\nAfter 270 rotation :")
# for p in node.pixel_positions:
#     print(p)

