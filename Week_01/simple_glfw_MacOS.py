from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glfw
import numpy as np

# Vertex shader source code
vertex_shader_source = """
#version 330 core
layout(location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""

# Fragment shader source code
fragment_shader_source = """
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0, 0.0, 0.0, 1.0); // red color
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

def create_shader_program():
    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(program))
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    return program

def refresh(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shader_program)
    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray(0)
    glUseProgram(0)
    glfw.swap_buffers(window)

def keyboard(window, key, scancode, action, mods):
    if key in (GLFW_KEY_ESCAPE, GLFW_KEY_Q) and action == GLFW_PRESS:
        glfw.set_window_should_close(window, GLFW_TRUE)

def show_versions():
    lists = [['Vendor', GL_VENDOR], ['Renderer', GL_RENDERER],
             ['OpenGL Version', GL_VERSION],
             ['GLSL Version', GL_SHADING_LANGUAGE_VERSION]]
    for x in lists:
        print("%s: %s" % (x[0], glGetString(x[1]).decode("utf-8")))

def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)  # To make it work on macOS
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "A Simple GLFW Program", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_refresh_callback(window, refresh)
    glfw.set_key_callback(window, keyboard)
    show_versions()

    global VAO, VBO, shader_program
    # Vertex data
    vertices = np.array([
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.0,  0.5, 0.0
    ], dtype=np.float32)

    shader_program = create_shader_program()

    # Create and bind the VAO
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Create and bind the VBO
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Define the vertex attributes
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Unbind the VAO
    glBindVertexArray(0)

    while not glfw.window_should_close(window):
        refresh(window)
        glfw.poll_events()

    # Clean up
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader_program)

    glfw.terminate()

if __name__ == "__main__":
    main()