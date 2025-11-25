from OpenGL.GL import *
from OpenGL.GL import shaders
import glm

class Shader:
    def __init__(self, vertex_path, fragment_path):
        self.ID = self.load_shaders(vertex_path, fragment_path)

    def load_shaders(self, vertex_path, fragment_path):
        with open(vertex_path, 'r') as f:
            vertex_code = f.read()
        with open(fragment_path, 'r') as f:
            fragment_code = f.read()

        vertex_shader = shaders.compileShader(vertex_code, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(fragment_code, GL_FRAGMENT_SHADER)
        
        return shaders.compileProgram(vertex_shader, fragment_shader)

    def use(self):
        glUseProgram(self.ID)

    def set_bool(self, name, value):
        glUniform1i(glGetUniformLocation(self.ID, name), int(value))

    def set_int(self, name, value):
        glUniform1i(glGetUniformLocation(self.ID, name), value)

    def set_float(self, name, value):
        glUniform1f(glGetUniformLocation(self.ID, name), value)

    def set_vec3(self, name, x, y=None, z=None):
        if y is None and z is None:
            glUniform3f(glGetUniformLocation(self.ID, name), x[0], x[1], x[2])
        else:
            glUniform3f(glGetUniformLocation(self.ID, name), x, y, z)

    def set_mat4(self, name, mat):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(mat))