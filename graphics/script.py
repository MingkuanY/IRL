from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import random
import time
import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



X_CONS = 3024
Y_CONS = 1514
recent_name = " "
animation_time = 5
current_animation_time = 0
current_text_animation_time = 0
image_orig = Image.new("RGBA", (X_CONS, Y_CONS), (3, 3, 3, 255))  # Dark blue background
star = Image.open("starry.png")

#############################################################
#                     USER MATCHING
from openai import OpenAI

#get json stuff
# Use the service account key JSON file to authenticate
file_name = '../bend/netwark-10966-firebase-adminsdk-cje0h-e979d7c50d.json'
file_path = os.path.join(os.path.dirname(__file__), file_name)
cred = credentials.Certificate(file_path)
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

# Download images from Firebase Storage to local "model_faces" directory
user_images_bucket_name = "netwark-10966.appspot.com"
user_images_bucket = storage.bucket(user_images_bucket_name)
blobs = user_images_bucket.list_blobs()
best_time = 0
me = ""

for name in blobs:
    name = name.name
    user_doc = db.collection('users').document(name).get().to_dict()
    if float(user_doc["time"]) > best_time:
        best_time = user_doc["time"]
        me = user_doc

print(me)
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are analyzing text and outputting lists."},
    {"role": "user", "content": f"""
                                Roles: Developer, Project Manager, Designer, Artist, Story Teller

                                Interests: Web Dev, UI/UX Design, AR/VR, Game Dev, DevOps, Accessibility, Mobile App Dev, Cybersecurity, Machine Learning, Databases, EdTech, Networking, Design, FinTech

                                Based on the user request, reply with the roles and interests that best match their wants in the format:

                                
                                Roles: role1, role2
                                Interests: interest1, interest2
                                

                                User Request: {me["interested_in_meeting"]}
                                """
                                }
  ]
) 

# Get and print the generated response
generated_response = response.choices[0].message.content
print(generated_response)
roles, interests = [e.split(": ")[1].strip().split(", ") for e in generated_response.strip().split('\n') if e.strip()]
roles = set(roles)
interests = set(interests)
seen = set()

print(generated_response)



blobs = user_images_bucket.list_blobs()
sparkly = []
for name in blobs:
    name = name.name
    user_doc = db.collection('users').document(name).get().to_dict()
    if any(e for e in user_doc["interests"] if e in interests) or user_doc["team_role"] in roles:
        sparkly.append(name)

print(sparkly)




#############################################################
def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server (Gmail in this case)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start the TLS (Transport Layer Security) connection
        server.starttls()
        
        # Log in to the email account
        server.login(sender_email, sender_password)
        
        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())


def send_contact(link, gmail, name):
    # Example usage
    sender_email = 'orca.pranav@gmail.com'
    sender_password = 'ungudzitejywjoqz'
    recipient_email = gmail
    subject = f'Networking Contact: {name}'
    message = link
    send_email(sender_email, sender_password, recipient_email, subject, message)


def determine_animation(name):
    global sparkly
    if name in sparkly:
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

        if len(content) == 14:
            name, first, last, hometown,team_role,position,interests,organization,contact,email,interested_in_meeting,time, x, y = content
            x_real, y_real = float(x), float(y)
            x_real*=X_CONS
            y_real*=Y_CONS
            x,y = 300,300
            if (name!=recent_name):
                current_text_animation_time = 0
                if name not in seen:
                    send_contact(contact,email,first+" "+last)
                seen.add(name)
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
            draw.text((x, y), (first+" "+last)[:min((150,int(current_text_animation_time)))], font=font_name, fill=(255, 255, 255), align="right")
            draw.text((x, y + 60), hometown[:min((150,int(current_text_animation_time)))], font=font_occupation, fill=(241, 252, 102), align="right")
            draw.text((x, y + 100), interests[:min((150,int(current_text_animation_time)))], font=font_interests, fill=(241, 252, 102), align="right")
            draw.text((x, y + 140), team_role[:min((150,int(current_text_animation_time)))], font=font_interests, fill=(241, 252, 102), align="right")

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
