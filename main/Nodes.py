import math

# COLOR : NONE(GREY), RED, BLUE, GREEN, 

class Node:
    def __init__(self, pixel_position):
        self.size = len(pixel_position)
        self.color = 'grey'
        self.associated_nodes = []
        self.pixel_positions = pixel_position


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
    
    
    # Start of functions that will take care of rotations
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
    
    def GetNormalizedRotations(self):

        def normalize(pixels):
            min_x = min(p[0] for p in pixels)
            min_y = min(p[1] for p in pixels)
            return sorted([(x - min_x, y - min_y) for x, y in pixels])

        center_x = sum(x for x, _ in self.pixel_positions) / self.size
        center_y = sum(y for _, y in self.pixel_positions) / self.size
        center = (center_x, center_y)

        rotations = []
        for i in range(4):
            angle = i * (math.pi / 2)
            rotated = [Node.Rotate(center, p, angle) for p in self.pixel_positions]
            rotations.append(normalize(rotated))
        return rotations
