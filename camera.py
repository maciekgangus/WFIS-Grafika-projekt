import glm
from math import sin, cos, radians

class Camera:
    def __init__(self, position=glm.vec3(0.0, 0.0, 3.0), up=glm.vec3(0.0, 1.0, 0.0), yaw=-90.0, pitch=0.0):
        self.position = position
        self.world_up = up
        self.yaw = yaw
        self.pitch = pitch
        
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3(0.0)
        self.up = glm.vec3(0.0)
        
        self.movement_speed = 5.0
        self.mouse_sensitivity = 0.1
        
        self.update_camera_vectors()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def process_keyboard(self, direction, delta_time):
        velocity = self.movement_speed * delta_time
        if direction == "FORWARD":
            self.position += self.front * velocity
        if direction == "BACKWARD":
            self.position -= self.front * velocity
        if direction == "LEFT":
            self.position -= self.right * velocity
        if direction == "RIGHT":
            self.position += self.right * velocity

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = glm.vec3()
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))