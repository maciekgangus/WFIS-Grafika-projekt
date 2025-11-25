import glfw
from OpenGL.GL import *
import glm
import sys
from camera import Camera
from scene import Scene
from PIL import Image
import numpy as np
from datetime import datetime

SCR_WIDTH = 1280
SCR_HEIGHT = 720
camera = Camera(position=glm.vec3(0.0, 2.0, 10.0))
last_x = SCR_WIDTH / 2.0
last_y = SCR_HEIGHT / 2.0
first_mouse = True
delta_time = 0.0
last_frame = 0.0
p_key_pressed = False

def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

def mouse_callback(window, xpos, ypos):
    global first_mouse, last_x, last_y

    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos

    last_x = xpos
    last_y = ypos

    camera.process_mouse_movement(xoffset, yoffset)

def take_screenshot():
    pixels = glReadPixels(0, 0, SCR_WIDTH, SCR_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE)

    image = np.frombuffer(pixels, dtype=np.uint8).reshape(SCR_HEIGHT, SCR_WIDTH, 3)

    image = np.flip(image, axis=0)

    img = Image.fromarray(image, 'RGB')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    img.save(filename)
    print(f"Screenshot saved: {filename}")

def process_input(window):
    global delta_time, p_key_pressed
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
        if not p_key_pressed:
            take_screenshot()
            p_key_pressed = True
    else:
        p_key_pressed = False

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.process_keyboard("FORWARD", delta_time)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.process_keyboard("BACKWARD", delta_time)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.process_keyboard("LEFT", delta_time)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.process_keyboard("RIGHT", delta_time)

def main():
    global delta_time, last_frame

    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.AUTO_ICONIFY, glfw.FALSE)

    window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "Night City 3D", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glPointSize(2.0)

    scene = Scene()

    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        process_input(window)

        scene.update_rain(delta_time)
        scene.update_cars(delta_time)

        glClearColor(0.05, 0.05, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection = glm.perspective(glm.radians(45.0), SCR_WIDTH / SCR_HEIGHT, 0.1, 300.0)
        view = camera.get_view_matrix()
        
        scene.render(view, projection, camera.position)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()