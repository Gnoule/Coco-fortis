import math

# COLOR : NONE(GREY), RED, BLUE, GREEN, 

class Node:
    def __init__(self, pixel_position, pixel_colors={}, color='grey', name="0"):
        self.size = len(pixel_position)
        # used if nodes are all same colors
        if (pixel_colors == {}):
            self.color = color
        else:
            self.color = None
        self.associated_nodes = []
        self.directly_connected_nodes = []
        self.pixel_positions = pixel_position
        self.pixel_colors = pixel_colors
        self.activate = True
        self.name = name
        self.centered_in_nodes = False


    # connection_type = HORIZONTAL OR VERTICAL
    # diff = difference between this node and other node
    def AddAssociatedNode(self, original_node_index, new_node, connection_type, diff):
        i = 0
        if diff[0] == 0:
            absDiff = diff[1]
        elif diff[1] == 0:
            absDiff = diff[0]
        else:
            absDiff = math.sqrt(diff[0]**2 + diff[1]**2)
            

        for val in self.associated_nodes:
            if new_node == val[0]:
                if abs(absDiff) <= abs(val[2]):
                    del self.associated_nodes[i]
                    break 
                else:
                    return
            i += 1
        self.associated_nodes.append([original_node_index, new_node, connection_type, diff])
        if abs(absDiff) <= 1:
            self.directly_connected_nodes.append(new_node)

    def GetAssociatedNode(self):
        return self.associated_nodes
    
    def GetPixelPositions(self):
        return self.pixel_positions
    
    def GetPixelColor(self):
        return self.pixel_colors

    def SetPixelPositions(self, new_pos):
        self.pixel_positions = new_pos

    def GetApproximatePixelPos(self):
        return self.pixel_positions[0]
    
    def DeactivateNode(self):
        self.activate = False

    def GetActiveStatus(self):
        return self.activate
    
    def GetCenteredInNodes(self):
        return self.centered_in_nodes
    
    def SetCenteredInNodes(self, value):
        self.centered_in_nodes = value

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
    
    # TODO return color if contructed on color graph
    def GetColor(self):
        if self.color == None:
            return self.pixel_colors[self.pixel_positions[0]]
        return self.color
    
    def GetAllColor(self):
        if self.color is not None:
            return [self.color]
        return list(set(self.pixel_colors.values()))

    
    # TODO
    def SetColor(self, new_color):
        pass
    
    # return size
    def GetSize(self):
        return self.size

    # TODO return if node has a hole
    def IsEmpty(self):
        return False
    

    def IsConnected(self):
        if len(self.directly_connected_nodes) > 0:
            return True
        return False 


    # function to get the min pos and max pos (on X and Y)
    #return : {max_x:val, max_y:val, min_x:val, min_y:val}
    @staticmethod
    def GetMinMaxPos(pixel_positions):
        min_x = pixel_positions[0][0]
        min_y = pixel_positions[0][1]
        max_x = pixel_positions[0][0]
        max_y = pixel_positions[0][1]
        for pos in pixel_positions:
            if pos[0] < min_x:
                min_x = pos[0]
            if pos[0] > max_x:
                max_x = pos[0]

            if pos[1] < min_y:
                min_y = pos[1]
            if pos[1] > max_y:
                max_y = pos[1]
        
        return {
            "min_x": min_x,
            "min_y": min_y,
            "max_x": max_x,
            "max_y": max_y
        }

             
    
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
    


