from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import random
import time

X_CONS = 3024
Y_CONS = 1514
recent_name = " "
animation_time = 5
current_animation_time = 0
current_text_animation_time = 0
image_orig = Image.new("RGBA", (X_CONS, Y_CONS), (3, 3, 3, 255))  # Dark blue background

star = Image.open("starry1.png")
def determine_animation(name):
    if name == "Katherine_Huang":
        return True
    else:
        return False

def render_text_on_image(lines, font_path, output_path):
    global recent_name, animation_time, current_animation_time, current_text_animation_time, star, image_orig
    image = image_orig.copy() # Dark blue background
    
    draw = ImageDraw.Draw(image)

    font_name = ImageFont.truetype(font_path_blade, 60)
    font_occupation = ImageFont.truetype(font_path, 40)
    font_interests = ImageFont.truetype(font_path, 30)

    for line in lines:
        content = line.strip().split(',')
        print(random.randint(0,20))

        if len(content) == 12:
            name, first, last, hometown,team_role,position,interests,organization,contact,image_link, x, y = content
            x_real, y_real = float(x), float(y)
            x_real*=X_CONS
            y_real*=Y_CONS
            x,y = 300,300
            if (name!=recent_name):
                current_text_animation_time = 0
                if determine_animation(name):
                    current_animation_time = animation_time
            
            if current_animation_time > 0:
                # draw.text((x, int(Y_CONS/2)), "MATCH", font=font_name, fill=(0, 0, 255), align="right")
                for i in range(50):
                    position = (random.randint(0,X_CONS), random.randint(0,Y_CONS))  # Adjust the position where you want to paste the image
                    image.paste(star, position)
                current_animation_time-=1

            if current_text_animation_time < 150:
                current_text_animation_time+=0.5

            recent_name = name

            draw.text((x_real, y_real), (first+"\n"+last), font=font_name, fill=(75, 75, 75), align="right")
            draw.text((x, y), (first+" "+last)[:min((150,int(current_text_animation_time)))], font=font_name, fill=(94, 255, 124), align="right")
            draw.text((x, y + 60), hometown[:min((150,int(current_text_animation_time)))], font=font_occupation, fill=(45, 227, 227), align="right")
            draw.text((x, y + 100), interests[:min((150,int(current_text_animation_time)))], font=font_interests, fill=(45, 227, 227), align="right")
            draw.text((x, y + 140), team_role[:min((150,int(current_text_animation_time)))], font=font_interests, fill=(45, 227, 227), align="right")

        else:
            print("Error: Invalid input format in the text file.")
        
    
    
   
    return np.array(image)

if __name__ == "__main__":
    font_path = "blah.ttf"
    font_path_blade = "blade.ttf"
    input_text_path = "output.csv"
    output_path = "output.png"

    cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Video Stream', cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)

    while True:
        print("FRAME")
        currtime = time.time()
        with open(input_text_path, "r") as input_file:
            lines = input_file.readlines()

        print(time.time()-currtime)
        line = lines[1] if len(lines) > 1 else ""
        
        # frame = cv2.imread(output_path)
        frame = render_text_on_image([line], font_path, output_path)
        print(time.time()-currtime)

        # Apply horizontal flipping to mirror the output
        mirrored_frame = cv2.flip(frame, 1)

        cv2.imshow('Video Stream', mirrored_frame)

        key = cv2.waitKey(1)
        if key == 27:  # Press 'Esc' to exit
            break
        print(time.time()-currtime)

    cv2.destroyAllWindows()
