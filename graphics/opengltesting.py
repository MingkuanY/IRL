import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from OpenGL.GLU import *
from PIL import Image


def create_checkerboard(x_t, y_t, square_size):
    img = Image.new('RGB', (x_t, y_t), color='green')
    pixels = img.load()

    for i in range(0, x_t, square_size):
        for j in range(0, y_t, square_size):
            if (i // square_size) % 2 == (j // square_size) % 2:
                for x in range(i, i + square_size):
                    for y in range(j, j + square_size):
                        pixels[x, y] = (0, 0, 0)  # Black square

    return np.array(img)


# Given coefficients
left_uv_to_rect_x = np.array([-0.7530364531010308,  0.8806592947908687, -0.8357813137161849,   0.3013989721607643,  0.9991764544369446, -0.2578159567698274,  0.3278667335649757, -0.4602577277109663,  -0.23980700925448195, -0.056891370605734376, -0.1248008903440144,  0.7641381600051023,   0.20935445281014292, -0.06256983016261788,  0.25844580123833516, -0.5098143951663658])

left_uv_to_rect_y = np.array([0.5612597403791647, -1.1899589356849427,  0.4652815794139322,  -0.2737933233160801,  0.3774305703820774, -0.8110333901413378,  1.2705775357104372, -0.7461290557575936,  -0.19222925521894155,  0.936404121235537,    -1.7109388784623627,  0.9147182510080394,   0.33073407860855586, -1.1463700238163494,   1.4965795269835196,  -0.7090919632511286])

right_uv_to_rect_x = np.array([-0.2117125319456463, -0.432262579698108,   0.41675063901331316, -0.14650788483832153, 1.0941580384494245, -0.30628109185189906, 0.109119134429531,   0.11642874201014344, -0.2761527408488216,  -0.4335709010559027,    0.9626491769528918, -0.5572405188216735,   0.18342869894719088,  0.37981945016058366, -0.8718621504058989,   0.5218968716935535])

right_uv_to_rect_y = np.array([1.0129568069314265, -2.110976542118192,   1.4108474581893895,  -0.7746290913232183, -0.746419837008027,   1.747642287758405, - 1.5753294007072252,  0.7143402603200871,   0.5607717274125551,  -1.5019493985594772,    1.2539128525783017, -0.42999735712430215, -0.21517910830152714,  0.5965062719847273,  -0.5664205050494074,   0.18545738302854597])

# Function to evaluate a 2D polynomial from its coefficients
def polyval2d(X, Y, C):
    X2 = X * X
    X3 = X2 * X
    Y2 = Y * Y
    Y3 = Y2 * Y
    return (((C[0]) + (C[1] * Y) + (C[2] * Y2) + (C[3] * Y3)) +
            ((C[4] * X) + (C[5] * X * Y) + (C[6] * X * Y2) + (C[7] * X * Y3)) +
            ((C[8] * X2) + (C[9] * X2 * Y) + (C[10] * X2 * Y2) + (C[11] * X2 * Y3)) +
            ((C[12] * X3) + (C[13] * X3 * Y) + (C[14] * X3 * Y2) + (C[15] * X3 * Y3)))

# Function to calculate the direction a ray takes exiting the eye towards a screen UV
def uv_to_ray_direction(uv, left_uv_to_rect_x, left_uv_to_rect_y, right_uv_to_rect_x, right_uv_to_rect_y):
    screen_uv = np.mod((2.0 * (1.0 - uv[0])), 1.0), uv[1]
    x_coeffs = left_uv_to_rect_x if uv[0] < 0.5 else right_uv_to_rect_x
    y_coeffs = left_uv_to_rect_y if uv[0] < 0.5 else right_uv_to_rect_y
    return np.array([polyval2d(screen_uv[0], screen_uv[1], x_coeffs),
                     polyval2d(screen_uv[0], screen_uv[1], y_coeffs), 1.0])

# Function to calculate the origin of a ray given a shader UV
def uv_to_ray_origin(uv):
    return np.array([0.032 * (-1.0 if uv[0] > 0.5 else 1.0), 0.0, 0.0])

# OpenGL initialization
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)

# OpenGL rendering function
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)


    # Iterate over pixel coordinates
    checkerboard = create_checkerboard(1280, 720, 20)
    for y in range(int(720)):
        for x in range(int(1280)):
            uv = np.array([x / 1280.0, y / 720.0])
            ray_origin = uv_to_ray_origin(uv)
            ray_direction = uv_to_ray_direction(uv, left_uv_to_rect_x, left_uv_to_rect_y,
                                                 right_uv_to_rect_x, right_uv_to_rect_y)
            
            # print(ray_origin)
            plane_pos = (ray_origin + ray_direction * 0.15) * 1000
            # print(plane_pos)
            # Perform ray tracing calculations (here, just a placeholder)
            # Replace this with your actual ray tracing logic
            if any(checkerboard[int(abs(plane_pos[0])),int(abs(plane_pos[1]))]):
            # color = np.array(checkerboard[x,y])
                glVertex2f(uv[0], uv[1])

    glEnd()
    glutSwapBuffers()

# Main function
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutCreateWindow(b"OpenGL Window")
    glutInitWindowSize(1280,720)
    glutDisplayFunc(render)
    init()
    glutMainLoop()

# Run the program
if __name__ == "__main__":
    main()