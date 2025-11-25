import glm
from mesh import Cube

class Car:
    def __init__(self, scene, pos, color, speed):
        self.scene = scene
        self.pos = pos
        self.color = color
        self.speed = speed
        self.start_pos = glm.vec3(pos)

        self.parts = []

        self.parts.append(self._create_part(
            pos_offset=glm.vec3(0, 0.5, 0),
            scale=glm.vec3(1.0, 0.6, 2.2),
            texture_name='tex_car_body'
        ))
        self.parts.append(self._create_part(
            pos_offset=glm.vec3(0, 1.1, -0.4),
            scale=glm.vec3(0.8, 0.5, 1.0),
            texture_name='tex_car_body'
        ))
        self.parts.append(self._create_part(
            pos_offset=glm.vec3(0, 1.1, 0.15),
            scale=glm.vec3(0.79, 0.48, 0.05),
            texture_name='tex_windshield'
        ))

        wheel_y = 0.1
        wheel_z_front = 1.0
        wheel_z_back = -1.0
        wheel_x = 0.5
        wheel_scale = glm.vec3(0.3, 0.5, 0.5)
        self.parts.append(self._create_part(glm.vec3(wheel_x, wheel_y, wheel_z_front), wheel_scale, 'tex_black'))
        self.parts.append(self._create_part(glm.vec3(-wheel_x, wheel_y, wheel_z_front), wheel_scale, 'tex_black'))
        self.parts.append(self._create_part(glm.vec3(wheel_x, wheel_y, wheel_z_back), wheel_scale, 'tex_black'))
        self.parts.append(self._create_part(glm.vec3(-wheel_x, wheel_y, wheel_z_back), wheel_scale, 'tex_black'))

        if self.speed > 0:
            headlight_z, taillight_z = 1.11, -1.11
        else:
            headlight_z, taillight_z = -1.11, 1.11

        self.parts.append(self._create_part(
            pos_offset=glm.vec3(-0.4, 0.4, headlight_z),
            scale=glm.vec3(0.2, 0.15, 0.02),
            texture_name='tex_taillight',
            emission_texture_name='tex_taillight'
        ))
        self.parts.append(self._create_part(
            pos_offset=glm.vec3(0.4, 0.4, headlight_z),
            scale=glm.vec3(0.2, 0.15, 0.02),
            texture_name='tex_taillight',
            emission_texture_name='tex_taillight'
        ))
        self.parts.append(self._create_part(
            pos_offset=glm.vec3(-0.4, 0.4, taillight_z),
            scale=glm.vec3(0.2, 0.15, 0.02),
            texture_name='tex_headlight',
            emission_texture_name='tex_headlight'
        ))
        self.parts.append(self._create_part(
            pos_offset=glm.vec3(0.4, 0.4, taillight_z),
            scale=glm.vec3(0.2, 0.15, 0.02),
            texture_name='tex_headlight',
            emission_texture_name='tex_headlight'
        ))

        self.headlights = []
        self.taillights = []
        
        taillight_color = glm.vec3(1.8, 1.8, 1.5)
        headlight_color = glm.vec3(1.5, 0.1, 0.1)

        self.headlights.append({'pos': glm.vec3(), 'color': headlight_color})
        self.headlights.append({'pos': glm.vec3(), 'color': headlight_color})
        self.taillights.append({'pos': glm.vec3(), 'color': taillight_color})
        self.taillights.append({'pos': glm.vec3(), 'color': taillight_color})
        
        self.scene.lights.extend(self.headlights)
        self.scene.lights.extend(self.taillights)


    def _create_part(self, pos_offset, scale, texture_name, emission_texture_name=None):
        return {
            'pos_offset': pos_offset,
            'scale': scale,
            'texture_name': texture_name,
            'emission_texture_name': emission_texture_name
        }

    def update(self, dt):
        self.pos.z -= self.speed * dt

        if self.speed > 0:
            headlight_z, taillight_z = 1.11, -1.11
        else:
            headlight_z, taillight_z = -1.11, 1.11
        
        self.headlights[0]['pos'] = self.pos + glm.vec3(-0.4, 0.4, headlight_z)
        self.headlights[1]['pos'] = self.pos + glm.vec3(0.4, 0.4, headlight_z)
        self.taillights[0]['pos'] = self.pos + glm.vec3(-0.4, 0.4, taillight_z)
        self.taillights[1]['pos'] = self.pos + glm.vec3(0.4, 0.4, taillight_z)

        if self.speed > 0:
            if self.pos.z < -60.0:
                self.pos.z = self.start_pos.z
        else:
            if self.pos.z > 60.0:
                self.pos.z = self.start_pos.z
