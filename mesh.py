import numpy as np
from OpenGL.GL import *
import ctypes

class Mesh:
    def __init__(self, vertices, indices=None):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32) if indices else None
        
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1) if self.indices is not None else None
        
        self.setup_mesh()

    def setup_mesh(self):
        glBindVertexArray(self.VAO)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        if self.EBO:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
        
        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.VAO)
        if self.indices is not None:
            glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        else:
            glDrawArrays(GL_TRIANGLES, 0, len(self.vertices) // 8)
        glBindVertexArray(0)

class Cube(Mesh):
    def __init__(self):
        # 24 unique vertices, 4 for each face.
        # Each vertex: Position (x,y,z), Normal (nx,ny,nz), TexCoord (s,t)
        vertices = [
            # Back face (-Z)
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0, 1.0,

            # Front face (+Z)
            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0, 0.0,
             0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  0.0, 1.0,

            # Left face (-X)
            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0, 0.0,
            -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  1.0, 1.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0, 1.0,
            -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  0.0, 0.0,

            # Right face (+X)
             0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0, 1.0,
             0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0, 1.0,
             0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0, 0.0,

            # Bottom face (-Y)
            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0, 1.0,
             0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0, 1.0,
             0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0, 0.0,

            # Top face (+Y)
            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0, 1.0,
             0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0, 1.0,
             0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0, 0.0
        ]
        
        # 36 indices to form 12 triangles
        indices = [
            0,  1,  2,   2,  3,  0,
            4,  5,  6,   6,  7,  4,
            8,  9, 10,  10, 11,  8,
            12, 13, 14,  14, 15, 12,
            16, 17, 18,  18, 19, 16,
            20, 21, 22,  22, 23, 20
        ]
        
        super().__init__(vertices, indices)

class Plane(Mesh):
    def __init__(self, w=1.0, h=1.0, tile=1.0, tile_w=None, tile_h=None):
        if tile_w is None:
            tile_w = tile
        if tile_h is None:
            tile_h = tile

        vertices = [
             w, 0.0,  h,  0.0, 1.0, 0.0,  tile_w, 0.0,
            -w, 0.0,  h,  0.0, 1.0, 0.0,  0.0, 0.0,
            -w, 0.0, -h,  0.0, 1.0, 0.0,  0.0, tile_h,

             w, 0.0,  h,  0.0, 1.0, 0.0,  tile_w, 0.0,
            -w, 0.0, -h,  0.0, 1.0, 0.0,  0.0, tile_h,
             w, 0.0, -h,  0.0, 1.0, 0.0,  tile_w, tile_h
        ]
        super().__init__(vertices)

class Sphere(Mesh):
    def __init__(self, radius=1.0, sectors=36, stacks=18):
        vertices = []
        indices = []
        
        import math
        
        lengthInv = 1.0 / radius
        
        for i in range(stacks + 1):
            stackAngle = math.pi / 2 - i * math.pi / stacks
            xy = radius * math.cos(stackAngle)
            z = radius * math.sin(stackAngle)
            
            for j in range(sectors + 1):
                sectorAngle = j * 2 * math.pi / sectors
                
                x = xy * math.cos(sectorAngle)
                y = xy * math.sin(sectorAngle)
                
                vertices.extend([x, y, z])
                
                nx = x * lengthInv
                ny = y * lengthInv
                nz = z * lengthInv
                vertices.extend([nx, ny, nz])
                
                s = j / sectors
                t = i / stacks
                vertices.extend([s, t])
                
        for i in range(stacks):
            k1 = i * (sectors + 1)
            k2 = k1 + sectors + 1
            
            for j in range(sectors):
                if i != 0:
                    indices.extend([k1, k2, k1 + 1])
                if i != (stacks - 1):
                    indices.extend([k1 + 1, k2, k2 + 1])
                k1 += 1
                k2 += 1
                
        super().__init__(vertices, indices)