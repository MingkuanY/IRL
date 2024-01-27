from PIL import Image, ImageDraw, ImageFont
import pyautogui
import cv2

X_CONS = 3024 #TODO figure out what's happening with this...
Y_CONS = 1514

def render_text_on_image(lines, font_path, output_path):
    #screen_width, screen_height = pyautogui.size()
    print("hello")


    image = Image.new("RGBA", (X_CONS, Y_CONS), (0, 0, 1, 255))  # Dark blue background
    draw = ImageDraw.Draw(image)

    # Load the fonts
    font_name = ImageFont.truetype(font_path, 60)
    font_occupation = ImageFont.truetype(font_path, 40)
    font_interests = ImageFont.truetype(font_path, 30)

    # Render each line of text onto the image
    for line in lines:
        content = line.strip().split(',')
        if len(content) == 5:
            name, occupation, interests, x, y = content
            x, y = int(x), int(y)

            # Render name with the biggest label
            draw.text((x, y), name, font=font_name, fill=(94, 255, 124), align="right")

            # Render occupation in italics
            draw.text((x, y + 60), occupation, font=font_occupation, fill=(45, 227, 227), align="right")

            # Render interests smaller
            draw.text((x, y + 100), interests, font=font_interests, fill=(45, 227, 227), align="right")
        else:
            print("Error: Invalid input format in the text file.")

    # Save the image to the same PNG file (overwrite the previous frame)
    image.save(output_path)

if __name__ == "__main__":
    # Specify the path to the font file, input text file, and output PNG file
    font_path = "SourceSansPro-Semibold.ttf"
    input_text_path = "data.txt"
    output_path = "output.png"

    # Create an OpenCV window
    cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('Video Stream', X_CONS, Y_CONS)
    cv2.setWindowProperty('Video Stream', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


    while True:
        # Read all lines from the input file
        with open(input_text_path, "r") as input_file:
            lines = input_file.readlines()

        # Render the frame and update the OpenCV window
        render_text_on_image(lines, font_path, output_path)
        frame = cv2.imread(output_path)
        cv2.imshow('Video Stream', frame)

        # Wait for 0.5 seconds before querying the file again
        key = cv2.waitKey(500)
        if key == 27:  # Press 'Esc' to exit
            break

    cv2.destroyAllWindows()
