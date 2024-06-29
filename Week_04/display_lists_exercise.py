import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *
import numpy as np
import pandas as pd
import math as m
import time

win_w, win_h = 1024, 768
models = {}

def resize(window, w, h):
    global win_w, win_h

    win_w, win_h = w, h
    glViewport(0, 0, w, h)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, win_w/win_h, 0.01, 50)

wireframe_on, animation_on = False, False
def keyboard(window, key, scancode, action, mods):
    global wireframe_on, animation_on

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_SPACE:
            animation_on = not animation_on
        elif key == GLFW_KEY_W:
            wireframe_on = not wireframe_on
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe_on else GL_FILL)
        elif key in (GLFW_KEY_ESCAPE, GLFW_KEY_Q):
            glfwSetWindowShouldClose(window, GLFW_TRUE)
    glfwPostEmptyEvent()

ticks, frame_cnt = 0, 0
def animation(window):
    global ticks, frame_cnt

    ticks += 1
    frame_cnt += 1
    glfwPostEmptyEvent()

def refresh(window):
    global start_time, frame_cnt
    if frame_cnt == 20:
        print("%.2f fps" % (frame_cnt/(time.time()-start_time)), ticks, end='\r')
        start_time = time.time()
        frame_cnt = 0    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glfwSwapBuffers(window)

def compile_list_on_model(model_filename):
    df = pd.read_csv(model_filename, sep='\s+', comment='#',
                     header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    n_vertices = len(positions)
    
    list_id = -1   # Modify to create a display list here

    return list_id, centroid, bbox

def gl_init_models():
    global centroid, bbox, start_time

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    models["bunny"], centroid, bbox = \
        compile_list_on_model("../models/bunny_uv.tri")
    models["horse"], _, _ = compile_list_on_model("../models/horse_uv.tri")
    models["monkey"], _, _ = compile_list_on_model("../models/monkey.tri")
    start_time = time.time() - 0.0001

def main():
    global window

    if not glfwInit():
        glfwTerminate()
        return
    
    window = glfwCreateWindow(1, 1, "Display Lists", None, None)
    glfwMakeContextCurrent(window)  
    glfwSetWindowRefreshCallback(window, refresh)
    glfwSetWindowSizeCallback(window, resize)
    glfwSetKeyCallback(window, keyboard)
    glfwSetWindowPos(window, 20, 50)
    glfwSetWindowSize(window, win_w, win_h)

    gl_init_models()
    while not glfwWindowShouldClose(window):
        if animation_on:
            animation(window)
        refresh(window)
        glfwWaitEvents()
    glfwDestroyWindow(window)
    glfwTerminate()

if __name__ == "__main__":
    main()