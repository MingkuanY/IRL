from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np


X_CONS = 3024
Y_CONS = 1514


def render_text_on_image(lines, font_path, output_path):
    image = Image.new("RGBA", (X_CONS, Y_CONS), (3, 3, 3, 255))  # Dark blue background
    draw = ImageDraw.Draw(image)

    font_name = ImageFont.truetype(font_path, 60)
    font_occupation = ImageFont.truetype(font_path, 40)
    font_interests = ImageFont.truetype(font_path, 30)

    for line in lines:
        content = line.strip().split(',')
        if len(content) == 5:
            name, occupation, interests, x, y = content
            x, y = int(x), int(y)

            draw.text((x, y), name, font=font_name, fill=(94, 255, 124), align="right")
            draw.text((x, y + 60), occupation, font=font_occupation, fill=(45, 227, 227), align="right")
            draw.text((x, y + 100), interests, font=font_interests, fill=(45, 227, 227), align="right")
        else:
            print("Error: Invalid input format in the text file.")
        
    
    
   
    image.save(output_path) #replace result with image to revert

if __name__ == "__main__":
    font_path = "SourceSansPro-Semibold.ttf"
    input_text_path = "data.txt"
    output_path = "output.png"

    cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Video Stream', cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)

    while True:
        with open(input_text_path, "r") as input_file:
            lines = input_file.readlines()

        render_text_on_image(lines, font_path, output_path)
        frame = cv2.imread(output_path)

        # Apply horizontal flipping to mirror the output
        mirrored_frame = cv2.flip(frame, 1)

        cv2.imshow('Video Stream', mirrored_frame)

        key = cv2.waitKey(500)
        if key == 27:  # Press 'Esc' to exit
            break

    cv2.destroyAllWindows()
