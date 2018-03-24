from hex_metrics import *

class HexMesh(object):
    
    def __init__(self):
        self.vertices = []
        self.indices = []
        self.triangles = 0
        self.colors = []
    
#    def add_triangle(self, v1, v2, v3):
#        vertex_index = len(self.vertices)
#        self.triangles += 1
#        match_vert = self.matching_vert(self.vertices, HexMetrics().perturb(v1))
#        if type(match_vert) == int:
#            self.indices.append(match_vert)
#        else:
#            self.vertices.append(HexMetrics().perturb(v1))
#            self.indices.append(vertex_index)
#            vertex_index += 1
#        
#        match_vert = self.matching_vert(self.vertices, HexMetrics().perturb(v2))
#        if type(match_vert) == int:
#            self.indices.append(match_vert)
#        else:
#            self.vertices.append(HexMetrics().perturb(v2))
#            self.indices.append(vertex_index)
#            vertex_index += 1
#            
#        match_vert = self.matching_vert(self.vertices, HexMetrics().perturb(v3))
#        if type(match_vert) == int:
#            self.indices.append(match_vert)
#        else:
#            self.vertices.append(HexMetrics().perturb(v3))
#            self.indices.append(vertex_index)

# Old method, shared vertices -------------------------------- #                
    def add_triangle(self, v1, v2, v3, color):
        vertex_index = len(self.vertices)
        #print("v1:", v1, "v2", v2, "v3", v3)
        #perturbed        
        self.vertices.append(HexMetrics().perturb(v1))
        self.vertices.append(HexMetrics().perturb(v2))
        self.vertices.append(HexMetrics().perturb(v3))
        
#        #Unperturbed
#        #self.vertices.append(v1)
#        #self.vertices.append(v2)
#        #self.vertices.append(v3)

        self.colors.append(color)
        self.triangles += 1
        
    def matching_vert(self, vert_list, value):
        for i in range(len(vert_list)):
            if value == vert_list[i]:
                return i
        return False
