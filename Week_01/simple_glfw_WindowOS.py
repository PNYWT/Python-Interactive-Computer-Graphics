from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *

def refresh(window):
    glClearColor(0, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    # First triangle (red)
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)
    glVertex3f(-1.0, 1.0, 0) # บนซ้าย
    glVertex3f( 1.0, 1.0, 0) # บนขวา
    glVertex3f(-1.0, -1.0, 0) # ล่างขวา
    glEnd()

    # Second triangle (yellow)
    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 0)
    glVertex3f(1.0, 1.0, 0) # บนขวา
    glVertex3f(1.0, -1.0, 0) # ล่างซ้าย
    glVertex3f(-1.0, -1.0, 0) # ล่างขวา
    glEnd()

    glFlush()

def keyboard(window, key, scancode, action, mods):
    if key in (GLFW_KEY_ESCAPE, GLFW_KEY_Q) and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

def show_versions():
    lists = [['Vendor', GL_VENDOR], ['Renderer', GL_RENDERER],
             ['OpenGL Version', GL_VERSION],
             ['GLSL Version', GL_SHADING_LANGUAGE_VERSION]]
    for x in lists:
        print("%s: %s" % (x[0], glGetString(x[1]).decode("utf-8")))

def main():
    if not glfwInit():
        glfwTerminate()
        return

    glfwWindowHint(GLFW_DOUBLEBUFFER, GL_FALSE)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6)
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_FALSE)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_COMPAT_PROFILE)
    window = glfwCreateWindow(800, 600, "A Simple GLFW Program", None, None)
    glfwMakeContextCurrent(window)
    glfwSetWindowRefreshCallback(window, refresh)    
    glfwSetKeyCallback(window, keyboard)
    show_versions()

    while not glfwWindowShouldClose(window):
        refresh(window)
        glfwPollEvents()

    glfwTerminate()

if __name__ == "__main__":
    main()
