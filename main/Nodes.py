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
    
    
    # Start of functions that will take care of rotations
    @staticmethod
    def Rotate(origin, point, angle, decimals=5):
        def clean(value):
            value = round(value, decimals)
            if abs(value) < 1e-10:
                return 0
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
            return sorted([(int(round(x - min_x)), int(round(y - min_y))) for x, y in pixels])

        # translate positions to origin before rotating
        translated = [(x - self.pixel_positions[0][0], y - self.pixel_positions[0][1]) for x, y in self.pixel_positions]

        rotations = []
        for i in range(4):
            angle = i * (math.pi / 2)
            rotated = [Node.Rotate((0, 0), p, angle) for p in translated]
            rotations.append(normalize(rotated))

        return rotations
    
    def ExtractSubPatternPositions(self, target_value):
        return [pos for pos in self.pixel_colors if self.pixel_colors[pos] == target_value]
    


