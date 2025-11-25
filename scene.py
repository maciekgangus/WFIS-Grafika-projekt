import glm
import random
import numpy as np
from OpenGL.GL import *
from mesh import Cube, Plane, Sphere, Mesh
from shader import Shader
from texture import Texture
from car import Car

class Scene:
    def __init__(self):
        self.shader = Shader("shaders/basic.vert", "shaders/basic.frag")
        self.rain_shader = Shader("shaders/rain.vert", "shaders/rain.frag")
        self.shadow_shader = Shader("shaders/shadow.vert", "shaders/shadow.frag")
        
        self.cube = Cube()
        self.sphere = Sphere(radius=1.0)
        self.plane = Plane(w=5.0, h=50.0, tile_w=1.0, tile_h=10.0)
        self.sidewalk = Plane(w=1.5, h=50.0, tile_w=1.0, tile_h=16.7)
        self.grass = Plane(w=1.0, h=50.0, tile_w=2.0, tile_h=25.0)

        self.textures = {
            "tex_road": Texture("textures/road.png"),
            "tex_road_spec": Texture("textures/road_spec.png"),
            "tex_building": Texture("textures/building.png"),
            "tex_building_emit": Texture("textures/building_emission.png"),
            "tex_sidewalk": Texture("textures/sidewalk.png"),
            "tex_grass": Texture("textures/grass.png"),
            "tex_billboard": Texture("textures/billboard.png"),
            "tex_billboard_emit": Texture("textures/billboard_emission.png"),
            "tex_black": Texture("textures/black.png"),
            "tex_moon": Texture("textures/moon.png"),
            "tex_car_body": Texture("textures/car_body.png"),
            "tex_headlight": Texture("textures/headlight.png"),
            "tex_taillight": Texture("textures/taillight.png"),
            "tex_windshield": Texture("textures/windshield.png")
        }

        self.buildings = []
        self.lights = []
        self.rain_drops = []
        self.cars = []

        self.billboard_pillars = []
        self.billboard_front = Plane(w=8.0, h=2.0, tile_w=1.0, tile_h=1.0)

        self.street_lamps = []

        self.setup_city()
        self.setup_billboard()
        self.setup_street_lamps()
        self.setup_rain()
        self.setup_shadows()
        self.setup_cars()

    def get_texture(self, name):
        return self.textures.get(name, self.textures["tex_black"])

    def setup_shadows(self):
        self.SHADOW_WIDTH = 2048
        self.SHADOW_HEIGHT = 2048
        self.depthMapFBO = glGenFramebuffers(1)
        
        self.depthMap = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.depthMap)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, self.SHADOW_WIDTH, self.SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        borderColor = [1.0, 1.0, 1.0, 1.0]
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, borderColor)
        
        glBindFramebuffer(GL_FRAMEBUFFER, self.depthMapFBO)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depthMap, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def setup_city(self):
        z_step = 10
        x_left = -10.0
        x_right = 10.0

        for z in range(-50, 50, z_step):
            scale_y = random.uniform(8.0, 25.0)
            self.buildings.append({
                'pos': glm.vec3(x_left, scale_y / 2.0, z),
                'scale': glm.vec3(5.0, scale_y, 8.0)
            })

            scale_y = random.uniform(8.0, 25.0)
            self.buildings.append({
                'pos': glm.vec3(x_right, scale_y / 2.0, z),
                'scale': glm.vec3(5.0, scale_y, 8.0)
            })

    def setup_billboard(self):
        self.billboard_pos = glm.vec3(0.0, 10.0, 0.0)

        self.billboard_pillars = [
            {'pos': glm.vec3(-5.5, 5.0, 0.0), 'scale': glm.vec3(0.4, 10.0, 0.4)},
            {'pos': glm.vec3(5.5, 5.0, 0.0), 'scale': glm.vec3(0.4, 10.0, 0.4)}
        ]

        for i in range(4):
            x_offset = -6.0 + (i * 4.0)
            self.lights.append({
                'pos': glm.vec3(x_offset, 8.2, 0.0),
                'color': glm.vec3(1.2, 1.3, 1.4)
            })

    def setup_street_lamps(self):
        lamp_z_positions = [-25, -15, -5, 15, 25, 35]
        lamp_height = 7.0
        arm_length = 3.0

        for z in lamp_z_positions:
            left_x = -7.0

            self.street_lamps.append({
                'type': 'post',
                'pos': glm.vec3(left_x, lamp_height / 2, z),
                'scale': glm.vec3(0.2, lamp_height, 0.2)
            })

            arm_y = lamp_height - 0.5
            arm_x = left_x + arm_length / 2
            self.street_lamps.append({
                'type': 'arm',
                'pos': glm.vec3(arm_x, arm_y, z),
                'scale': glm.vec3(arm_length, 0.15, 0.15),
                'rotation': 0
            })

            self.lights.append({
                'pos': glm.vec3(left_x + arm_length, arm_y - 0.3, z),
                'color': glm.vec3(0.8, 0.7, 0.5)
            })

            right_x = 7.0

            self.street_lamps.append({
                'type': 'post',
                'pos': glm.vec3(right_x, lamp_height / 2, z),
                'scale': glm.vec3(0.2, lamp_height, 0.2)
            })

            arm_x = right_x - arm_length / 2
            self.street_lamps.append({
                'type': 'arm',
                'pos': glm.vec3(arm_x, arm_y, z),
                'scale': glm.vec3(arm_length, 0.15, 0.15),
                'rotation': 0
            })

            self.lights.append({
                'pos': glm.vec3(right_x - arm_length, arm_y - 0.3, z),
                'color': glm.vec3(0.8, 0.7, 0.5)
            })
    
    def setup_cars(self):
        self.cars.append(Car(self, pos=glm.vec3(2.5, 0.1, 40.0), color=glm.vec3(1,0,0), speed=15.0))
        self.cars.append(Car(self, pos=glm.vec3(2.5, 0.1, 20.0), color=glm.vec3(0,1,0), speed=13.0))

        self.cars.append(Car(self, pos=glm.vec3(-2.5, 0.1, -40.0), color=glm.vec3(0,0,1), speed=-12.0))
        self.cars.append(Car(self, pos=glm.vec3(-2.5, 0.1, -20.0), color=glm.vec3(1,1,0), speed=-16.0))

    def setup_rain(self):
        self.rain_count = 2000
        self.rain_data = np.zeros((self.rain_count, 3), dtype=np.float32)
        for i in range(self.rain_count):
            self.rain_data[i] = [
                random.uniform(-20, 20),
                random.uniform(0, 20),
                random.uniform(-50, 50)
            ]
        
        self.rainVAO = glGenVertexArrays(1)
        self.rainVBO = glGenBuffers(1)
        
        glBindVertexArray(self.rainVAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.rainVBO)
        glBufferData(GL_ARRAY_BUFFER, self.rain_data.nbytes, self.rain_data, GL_DYNAMIC_DRAW)
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

    def update_rain(self, dt):
        for i in range(self.rain_count):
            self.rain_data[i][1] -= 10.0 * dt
            if self.rain_data[i][1] < 0:
                self.rain_data[i][1] = 20.0
                self.rain_data[i][0] = random.uniform(-20, 20)
                self.rain_data[i][2] = random.uniform(-50, 50)
                
        glBindBuffer(GL_ARRAY_BUFFER, self.rainVBO)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.rain_data.nbytes, self.rain_data)
    
    def update_cars(self, dt):
        for car in self.cars:
            car.update(dt)

    def render_scene_objects(self, shader):
        if shader == self.shader:
            self.get_texture("tex_road").bind(0)
            self.get_texture("tex_black").bind(1)
            self.get_texture("tex_road_spec").bind(2)
        model = glm.mat4(1.0)
        shader.set_mat4("model", model)
        self.plane.draw()
        
        if shader == self.shader:
            self.get_texture("tex_sidewalk").bind(0)
            self.get_texture("tex_black").bind(1)
            self.get_texture("tex_black").bind(2)

        model = glm.translate(glm.mat4(1.0), glm.vec3(-6.5, 0.01, 0.0))
        shader.set_mat4("model", model)
        self.sidewalk.draw()

        model = glm.translate(glm.mat4(1.0), glm.vec3(6.5, 0.01, 0.0))
        shader.set_mat4("model", model)
        self.sidewalk.draw()

        if shader == self.shader:
            self.get_texture("tex_grass").bind(0)
            self.get_texture("tex_black").bind(1)
            self.get_texture("tex_black").bind(2)

        model = glm.translate(glm.mat4(1.0), glm.vec3(-9.0, 0.02, 0.0))
        shader.set_mat4("model", model)
        self.grass.draw()

        model = glm.translate(glm.mat4(1.0), glm.vec3(9.0, 0.02, 0.0))
        shader.set_mat4("model", model)
        self.grass.draw()

        if shader == self.shader:
            self.get_texture("tex_building").bind(0)
            self.get_texture("tex_building_emit").bind(1)
            self.get_texture("tex_black").bind(2)
        for b in self.buildings:
            model = glm.translate(glm.mat4(1.0), b['pos'])
            model = glm.scale(model, b['scale'])
            shader.set_mat4("model", model)
            self.cube.draw()

        if shader == self.shader:
            self.get_texture("tex_sidewalk").bind(0)
            self.get_texture("tex_black").bind(1)
            self.get_texture("tex_black").bind(2)
        for pillar in self.billboard_pillars:
            model = glm.translate(glm.mat4(1.0), pillar['pos'])
            model = glm.scale(model, pillar['scale'])
            shader.set_mat4("model", model)
            self.cube.draw()

        if shader == self.shader:
            self.get_texture("tex_sidewalk").bind(0)
            self.get_texture("tex_black").bind(1)
            self.get_texture("tex_black").bind(2)
        model = glm.translate(glm.mat4(1.0), self.billboard_pos)
        model = glm.scale(model, glm.vec3(16.0, 4.0, 0.8))
        shader.set_mat4("model", model)
        self.cube.draw()

        if shader == self.shader:
            self.get_texture("tex_billboard").bind(0)
            self.get_texture("tex_billboard_emit").bind(1)
            self.get_texture("tex_black").bind(2)
        model = glm.translate(glm.mat4(1.0), self.billboard_pos)
        model = glm.translate(model, glm.vec3(0.0, 0.0, 0.41))
        model = glm.rotate(model, glm.radians(90.0), glm.vec3(1.0, 0.0, 0.0))
        shader.set_mat4("model", model)
        self.billboard_front.draw()

        if shader == self.shader:
            self.get_texture("tex_sidewalk").bind(0)
            self.get_texture("tex_black").bind(1)
            self.get_texture("tex_black").bind(2)
        for lamp in self.street_lamps:
            model = glm.translate(glm.mat4(1.0), lamp['pos'])
            model = glm.scale(model, lamp['scale'])
            shader.set_mat4("model", model)
            self.cube.draw()

        for car in self.cars:
            for part in car.parts:
                if shader == self.shader:
                    self.get_texture(part['texture_name']).bind(0)
                    if part['emission_texture_name']:
                        self.get_texture(part['emission_texture_name']).bind(1)
                    else:
                        self.get_texture('tex_black').bind(1)
                    self.get_texture('tex_black').bind(2)
                
                model = glm.translate(glm.mat4(1.0), car.pos)
                model = glm.translate(model, part['pos_offset'])
                model = glm.scale(model, part['scale'])
                shader.set_mat4("model", model)
                self.cube.draw()

    def render(self, view, projection, view_pos):
        lightPos = glm.vec3(30.0, 50.0, -80.0)
        lightProjection = glm.ortho(-60.0, 60.0, -60.0, 60.0, 1.0, 200.0)
        lightView = glm.lookAt(lightPos, glm.vec3(0.0), glm.vec3(0.0, 1.0, 0.0))
        lightSpaceMatrix = lightProjection * lightView
        
        self.shadow_shader.use()
        self.shadow_shader.set_mat4("lightSpaceMatrix", lightSpaceMatrix)
        
        glViewport(0, 0, self.SHADOW_WIDTH, self.SHADOW_HEIGHT)
        glBindFramebuffer(GL_FRAMEBUFFER, self.depthMapFBO)
        glClear(GL_DEPTH_BUFFER_BIT)
        self.render_scene_objects(self.shadow_shader)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
        glViewport(0, 0, 1280, 720) 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_mat4("lightSpaceMatrix", lightSpaceMatrix)
        
        lightDir = glm.normalize(glm.vec3(0.0) - lightPos)
        self.shader.set_vec3("dirLight.direction", lightDir) 
        self.shader.set_vec3("dirLight.ambient", 0.2, 0.2, 0.3)
        self.shader.set_vec3("dirLight.diffuse", 0.5, 0.5, 0.7)
        self.shader.set_vec3("dirLight.specular", 0.5, 0.5, 0.5)
        
        num_lights = min(len(self.lights), 50)
        self.shader.set_int("numLights", num_lights)
        for i, light in enumerate(self.lights):
            if i >= 50: break
            self.shader.set_vec3(f"pointLights[{i}].position", light['pos'])
            self.shader.set_vec3(f"pointLights[{i}].ambient", 0.0, 0.0, 0.0)
            self.shader.set_vec3(f"pointLights[{i}].diffuse", light['color'].x, light['color'].y, light['color'].z)
            self.shader.set_vec3(f"pointLights[{i}].specular", 1.0, 1.0, 1.0)
            self.shader.set_float(f"pointLights[{i}].constant", 1.0)
            self.shader.set_float(f"pointLights[{i}].linear", 0.09)
            self.shader.set_float(f"pointLights[{i}].quadratic", 0.032)

        self.shader.set_int("texture1", 0)
        self.shader.set_int("texture_emission", 1)
        self.shader.set_int("texture_specular", 2)
        self.shader.set_int("shadowMap", 3)
        
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.depthMap)

        self.get_texture("tex_black").bind(0)
        self.get_texture("tex_moon").bind(1)
        self.get_texture("tex_black").bind(2)
        
        model = glm.translate(glm.mat4(1.0), lightPos)
        model = glm.scale(model, glm.vec3(10.0, 10.0, 10.0))
        self.shader.set_mat4("model", model)
        self.sphere.draw()
        
        self.render_scene_objects(self.shader)
        
        self.rain_shader.use()
        self.rain_shader.set_mat4("view", view)
        self.rain_shader.set_mat4("projection", projection)
        model = glm.mat4(1.0)
        self.rain_shader.set_mat4("model", model)
        
        glBindVertexArray(self.rainVAO)
        glDrawArrays(GL_POINTS, 0, self.rain_count)