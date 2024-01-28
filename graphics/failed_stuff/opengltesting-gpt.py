import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

from OpenGL.GLUT import glutInit, glutInitDisplayMode, glutCreateWindow, glutDisplayFunc, glutMainLoop


# Vertex shader source code
vertex_shader = """
#version 330 core
in vec4 a_position;

void main()
{
    gl_Position = a_position;
}
"""

# Your fragment shader code
fragment_shader = """
float[]  left_uv_to_rect_x  = float[16]( -0.7530364531010308,  0.8806592947908687, -0.8357813137161849,   0.3013989721607643,  0.9991764544369446, -0.2578159567698274,  0.3278667335649757, -0.4602577277109663,  -0.23980700925448195, -0.056891370605734376, -0.1248008903440144,  0.7641381600051023,   0.20935445281014292, -0.06256983016261788,  0.25844580123833516, -0.5098143951663658 );
float[]  left_uv_to_rect_y  = float[16](  0.5612597403791647, -1.1899589356849427,  0.4652815794139322,  -0.2737933233160801,  0.3774305703820774, -0.8110333901413378,  1.2705775357104372, -0.7461290557575936,  -0.19222925521894155,  0.936404121235537,    -1.7109388784623627,  0.9147182510080394,   0.33073407860855586, -1.1463700238163494,   1.4965795269835196,  -0.7090919632511286 );
float[] right_uv_to_rect_x  = float[16]( -0.2117125319456463, -0.432262579698108,   0.41675063901331316, -0.14650788483832153, 1.0941580384494245, -0.30628109185189906, 0.109119134429531,   0.11642874201014344, -0.2761527408488216,  -0.4335709010559027,    0.9626491769528918, -0.5572405188216735,   0.18342869894719088,  0.37981945016058366, -0.8718621504058989,   0.5218968716935535 );
float[] right_uv_to_rect_y  = float[16](  1.0129568069314265, -2.110976542118192,   1.4108474581893895,  -0.7746290913232183, -0.746419837008027,   1.747642287758405, - 1.5753294007072252,  0.7143402603200871,   0.5607717274125551,  -1.5019493985594772,    1.2539128525783017, -0.42999735712430215, -0.21517910830152714,  0.5965062719847273,  -0.5664205050494074,   0.18545738302854597);

float polyval2d(float X, float Y, float[16] C) {
  float X2 = X * X; float X3 = X2 * X;
  float Y2 = Y * Y; float Y3 = Y2 * Y;
  return (((C[ 0]     ) + (C[ 1]      * Y) + (C[ 2]      * Y2) + (C[ 3]      * Y3)) +
          ((C[ 4] * X ) + (C[ 5] * X  * Y) + (C[ 6] * X  * Y2) + (C[ 7] * X  * Y3)) +
          ((C[ 8] * X2) + (C[ 9] * X2 * Y) + (C[10] * X2 * Y2) + (C[11] * X2 * Y3)) +
          ((C[12] * X3) + (C[13] * X3 * Y) + (C[14] * X3 * Y2) + (C[15] * X3 * Y3)));
}

vec3 uvToRayDirection(vec2 uv, float[16]  left_uv_to_rect_x, float[16]  left_uv_to_rect_y, 
                               float[16] right_uv_to_rect_x, float[16] right_uv_to_rect_y) {
    vec2 screenUV = vec2(mod((2.0 * (1.0-uv.x)), 1.0), uv.y);
    float[16] xCoeffs = left_uv_to_rect_x; if(uv.x < 0.5) { xCoeffs = right_uv_to_rect_x; }
    float[16] yCoeffs = left_uv_to_rect_y; if(uv.x < 0.5) { yCoeffs = right_uv_to_rect_y; }
    return vec3(polyval2d(screenUV.x, screenUV.y, xCoeffs),
                polyval2d(screenUV.x, screenUV.y, yCoeffs), 1.0);
}

vec3 uvToRayOrigin(vec2 uv) { 
    return vec3(0.032 * ((uv.x > 0.5) ? -1.0 : 1.0), 0.0, 0.0); 
}

void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
    vec2 uv = fragCoord/iResolution.xy;

    vec3 ray_origin = uvToRayOrigin(uv);
    vec3 ray_dir    = uvToRayDirection(uv, left_uv_to_rect_x, 
                                           left_uv_to_rect_y, 
                                           right_uv_to_rect_x, 
                                           right_uv_to_rect_y);

    vec3 plane_pos = ray_origin + ray_dir * 0.15;
    
    vec2 Pos = floor(plane_pos.xy * 100.0);
    float PatternMask = mod(Pos.x + mod(Pos.y, 2.0), 2.0);

    fragColor = vec4(vec3(PatternMask), 1.0);
}
"""

# Shader initialization function
def compile_shader(shader_source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_source)
    glCompileShader(shader)

    # Check compilation status
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader))

    return shader

# Shader program initialization function
def create_program(vertex_shader_source, fragment_shader_source):
    program = glCreateProgram()

    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)

    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    # Check linking status
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(program))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program

# PyOpenGL initialization
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutCreateWindow("OpenGL Shader Example")

# Initialize OpenGL context
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-1, 1, -1, 1, -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Shader program creation
shader_program = create_program(vertex_shader, fragment_shader)

# Main loop
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_QUADS)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glVertex2f(-1, 1)
    glEnd()
    glutSwapBuffers()

# Register display function
glutDisplayFunc(display)

# Start the main loop
glutMainLoop()
