import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *
import numpy as np
import pandas as pd
import time, math as m
import imgui
from imgui.integrations.glfw import GlfwRenderer
from gl_helpers import *

impl, t_value = None, 0
win_w, win_h = 1280, 800
Ka = [0.3, 0.3, 0.3]
I, light_pos, eye_pos, eye_at = [1, 1, 1], [0, 0, 10], [0, 0, 0], [0, 0, 0]
rot_x, rot_y, specular_on = 0, 30, True
clear_color = [0.5, 0.85, 0.85]

def draw_gui():
    global I, Ka, clear_color
    global rot_x, rot_y, specular_on

    impl.process_inputs()
    imgui.new_frame()                 # Start the Dear ImGui frame 
    imgui.begin("Control")            # Create a window
    imgui.push_item_width(300)
    _, I = imgui.color_edit3("Light Intensity", *I)
    _, Ka = imgui.color_edit3("Ka", *Ka)
    _, specular_on = imgui.checkbox("Specular Enabled", specular_on)
    imgui.text("Light Position")
    imgui.push_item_width(100)
    _, light_pos[0] = imgui.slider_float("X###light_pos_x", light_pos[0], -10, 10)
    imgui.same_line()
    _, light_pos[1] = imgui.slider_float("Y###light_pos_y", light_pos[1], -10, 10)
    imgui.same_line()
    _, light_pos[2] = imgui.slider_float("Z###light_pos_z", light_pos[2], -10, 10)
    imgui.text("Eye Position")
    _, eye_pos[0] = imgui.slider_float("X###eye_pos_x", eye_pos[0], -10, 10)
    imgui.same_line()
    _, eye_pos[1] = imgui.slider_float("Y###eye_pos_y", eye_pos[1], -10, 10)
    imgui.same_line()
    _, eye_pos[2] = imgui.slider_float("Z###eye_pos_z", eye_pos[2], -10, 10)
    imgui.text("Eye At")
    _, eye_at[0] = imgui.slider_float("X###eye_at_x", eye_at[0], -10, 10)
    imgui.same_line()
    _, eye_at[1] = imgui.slider_float("Y###eye_at_y", eye_at[1], -10, 10)
    imgui.same_line()
    _, eye_at[2] = imgui.slider_float("Z###eye_at_z", eye_at[2], -10, 10)
    imgui.pop_item_width()
    imgui.text("Model Rotation")
    imgui.push_item_width(120)    
    _, rot_x = imgui.slider_float("Rotate X", rot_x, -180, 180)
    imgui.same_line()        
    _, rot_y = imgui.slider_float("Rotate Y", rot_y, -180, 180)
    imgui.pop_item_width()        
    _, clear_color = imgui.color_edit3("Clear Color", *clear_color)
    imgui.text("Application average %.3f ms/frame (%.1f FPS)" % \
        (1000 / imgui.get_io().framerate, imgui.get_io().framerate))
    imgui.pop_item_width()
    imgui.end()

def resize(window, w, h):
    glViewport(0, 0, w, h)	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w/h, 0.1, 50)

def refresh(window):
    glClearColor(*clear_color, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(*eye_pos, *eye_at, 0, 1, 0)

    glRotate(t_value, 0.8, 0.8, 0.2)
    glRotate(rot_x, 1, 0, 0)
    glRotate(rot_y, 0, 1, 0)

    colors[:] = 0.2*normals + Ka

    glVertexPointer(3, GL_FLOAT, 0, positions)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glNormalPointer(GL_FLOAT, 0, normals)
    glTexCoordPointer(2, GL_FLOAT, 0, uvs)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)      
    
    draw_gui()
    imgui.render()
    impl.render(imgui.get_draw_data())    

    glfwSwapBuffers(window)

wireframe_on, animation_on = False, False
def keyboard(window, key, scancode, action, mods):
    global wireframe_on, animation_on, rot_x, rot_y, t_value

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_SPACE:
            animation_on = not animation_on
        elif key == GLFW_KEY_R:
            rot_x = rot_y = t_value = 0
        elif key == GLFW_KEY_W:
            wireframe_on = not wireframe_on
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe_on else GL_FILL)
        elif key in (GLFW_KEY_ESCAPE, GLFW_KEY_Q):
            glfwSetWindowShouldClose(window, GLFW_TRUE)
    glfwPostEmptyEvent()

def animation(window):
    global t_value
    t_value += 1
    glfwPostEmptyEvent()

def gl_init():
    global n_vertices, positions, colors, normals, uvs, centroid, bbox
    global impl, eye_pos, eye_at

    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    imgui.create_context()
    imgui.style_colors_light()
    impl = GlfwRenderer(window, attach_callbacks=False)
    imgui.set_next_window_position(500, 10)
    imgui.set_next_window_collapsed(True)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    df = pd.read_csv("../models/teapot_uv.tri", sep='\s+',
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    n_vertices = len(df.values)
    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    print("no. of vertices: %d, no. of triangles: %d" % 
          (n_vertices, n_vertices//3))
    print("Centroid:", centroid)
    print("BBox:", bbox)
    eye_pos = centroid + (0.5, 1.5, 1.5)
    eye_at = centroid + (0.5, 0, 0)

def main():
    global window

    if not glfwInit():
        glfwTerminate()
        return

    window = glfwCreateWindow(1, 1, "imGui Lighting Exercise", None, None)
    glfwMakeContextCurrent(window)  
    glfwSetWindowRefreshCallback(window, refresh)
    glfwSetWindowSizeCallback(window, resize)
    glfwSetKeyCallback(window, keyboard)
    glfwSetWindowPos(window, 20, 50)
    glfwSetWindowSize(window, 1024, 768)

    gl_init()
    while not glfwWindowShouldClose(window):
        if animation_on:
            animation(window)
        glfwPollEvents()
        refresh(window)
    impl.shutdown()        
    glfwDestroyWindow(window)
    glfwTerminate()

if __name__ == "__main__":
    main()