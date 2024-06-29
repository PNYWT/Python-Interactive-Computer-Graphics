import sys, os
from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *
import numpy as np
import pandas as pd
import time
from ctypes import c_void_p
import imgui
from imgui.integrations.glfw import GlfwRenderer

win_w, win_h = 1024, 768
impl = None
Kd1 = [0.86, 0.86, 0.4]

def print_shader_info_log(shader, prompt=""):
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not result:
        print("%s: %s" % (prompt, glGetShaderInfoLog(shader).decode("utf-8")))
        os._exit()

def print_program_info_log(shader, prompt=""):
    result = glGetProgramiv(shader, GL_LINK_STATUS)
    if not result:
        print("%s: %s" % (prompt, glGetProgramInfoLog(shader).decode("utf-8")))
        os._exit()

def create_shaders():
    global prog_id
    global vao, vbo

    vert_code = '''
#version 130
void main()
{
   gl_Position = gl_Vertex;
}'''
    frag_code = '''
#version 130
void main()
{
   gl_FragColor = vec4(0.5, 0.5, 1, 1);
}'''

    vert_id = glCreateShader(GL_VERTEX_SHADER)
    frag_id = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vert_id, vert_code)
    glShaderSource(frag_id, frag_code)

    glCompileShader(vert_id)
    glCompileShader(frag_id)
    print_shader_info_log(vert_id, "Vertex Shader")
    print_shader_info_log(frag_id, "Fragment Shader")

    prog_id = glCreateProgram()
    glAttachShader(prog_id, vert_id)
    glAttachShader(prog_id, frag_id)

    glLinkProgram(prog_id)
    print_program_info_log(prog_id, "Link error")

    # Fix me!
    # Implement VAO and VBO here.

def draw_gui():
    global Kd1, Kd2, light_position

    impl.process_inputs()
    imgui.new_frame()                 # Start the Dear ImGui frame 
    imgui.begin("Control")            # Create a window
    _, Kd1 = imgui.color_edit3("Kd1", *Kd1)

    imgui.text("Application average %.3f ms/frame (%.1f FPS)" % \
        (1000 / imgui.get_io().framerate, imgui.get_io().framerate))
    imgui.end()

wireframe_on, animation_on = False, True
def keyboard(window, key, scancode, action, mods):
    global wireframe_on, animation_on, texture_func

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_SPACE:
            animation_on = not animation_on        
        elif key == GLFW_KEY_W:
            wireframe_on = not wireframe_on
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe_on else GL_FILL)
        elif key in (GLFW_KEY_ESCAPE, GLFW_KEY_Q):
            glfwSetWindowShouldClose(window, GLFW_TRUE)
    glfwPostEmptyEvent()

def resize(window, w, h):
    global win_w, win_h

    win_w, win_h = w, h
    glViewport(0, 0, w, h)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, win_w/win_h, 0.01, 20)

def refresh(window):
    global start_time, frame_cnt
    if frame_cnt == 20:
        print("%.2f fps" % (frame_cnt/(time.time()-start_time)), end='\r')
        start_time = time.time()
        frame_cnt = 0

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)   
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*eye_pos, *centroid, 0, 1, 0)

    glUseProgram(prog_id)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)

    draw_gui()
    imgui.render()
    impl.render(imgui.get_draw_data())
        
    glfwSwapBuffers(window)

frame_cnt = 0
def animation(window):
    global frame_cnt

    frame_cnt += 1

def init_model():
    global n_vertices, positions, normals, uvs, centroid, bbox, eye_pos
    global impl, start_time

    glClearColor(0.01, 0.01, 0.2, 1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    imgui.create_context()
    imgui.style_colors_dark()
    impl = GlfwRenderer(window, attach_callbacks=False)
    imgui.set_next_window_position(500, 10)
    imgui.set_next_window_collapsed(True)

    df = pd.read_csv("../models/armadillo.tri", sep='\s+',   
                     comment='#', header=None, dtype=np.float32)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)
    centroid = df.values[:, 0:3].min(axis=0) + 0.5*bbox + (0.5, 0, 0)
    eye_pos = centroid + (0, 0, 8)

    positions = df.values[:, 0:3]
    normals = df.values[:, 3:6]
    uvs = df.values[:, 6:8]

    n_vertices = len(positions)
    print("no. of vertices: %d, no. of triangles: %d" % 
          (n_vertices, n_vertices//3))
    print("Centroid:", centroid)
    print("BBox:", bbox)
    start_time = time.time() - 1e-4

def main():
    global window

    if not glfwInit():
        glfwTerminate()
        return

    window = glfwCreateWindow(1, 1, "VAO and VBO Exercise", None, None)
    glfwMakeContextCurrent(window)  
    glfwSetWindowRefreshCallback(window, refresh)
    glfwSetWindowSizeCallback(window, resize)
    glfwSetKeyCallback(window, keyboard)
    glfwSetWindowPos(window, 20, 50)
    glfwSetWindowSize(window, win_w, win_h)

    init_model()
    create_shaders()
    while not glfwWindowShouldClose(window):
        if animation_on:
            animation(window)
        glfwWaitEvents()
        refresh(window)
    glfwDestroyWindow(window)
    glfwTerminate()

if __name__ == "__main__":
    main()