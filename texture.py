from OpenGL.GL import *
from PIL import Image

class Texture:
    def __init__(self, path):
        self.ID = self.load_texture(path)

    def load_texture(self, path):
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        try:
            image = Image.open(path)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            img_data = image.tobytes()
            width, height = image.size
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)
            
            print(f"Successfully loaded texture: {path}")
            return texture_id
        except Exception as e:
            print(f"Failed to load texture: {path}")
            print(e)
            return 0

    def bind(self, unit=0):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.ID)