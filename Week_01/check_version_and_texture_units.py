from OpenGL.GL import *
from glfw.GLFW import *
  
def draw():
	pass

glfwInit()
window = glfwCreateWindow(200, 200, "Version Check", None, None)
glfwMakeContextCurrent(window)

lists = [['Vendor', GL_VENDOR], ['Renderer',GL_RENDERER],
         ['OpenGL Version', GL_VERSION],
         ['GLSL Version', GL_SHADING_LANGUAGE_VERSION]]
for x in lists:
    print("%s: %s" % (x[0], glGetString(x[1]).decode("utf-8")))

unit_count = glGetIntegerv(GL_MAX_TEXTURE_UNITS)
print("Number of texture units (fixed-function OpenGL) = %d" % unit_count)

unit_count = glGetIntegerv(GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS)
print("Number of texture units (modern OpenGL) = %d" % unit_count)