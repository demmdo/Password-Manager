from cryptography.fernet import Fernet
import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("Dark")
app = ctk.CTk()
app.title("Password Manager")
app.attributes("-fullscreen", True)
width = 1920
height = 1080

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width - width) // 2
y = (screen_height - height) // 2

app.geometry(f"{width}x{height}+{x}+{y}")

def glow_effect(widget, steps=25, start_rgb=(239, 68, 68), delay=30):
    theme_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]

    if ctk.get_appearance_mode() == "Dark":
        end_color = theme_color[1]
    else:
        end_color = theme_color[0]


    r16, g16, b16 = app.winfo_rgb(end_color)
    end_rgb = (r16 // 256, g16 // 256, b16 // 256)

    for i in range(steps + 1):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (i / steps))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (i / steps))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (i / steps))

        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        app.after(i * delay, lambda c=hex_color: widget.configure(fg_color=c))


    app.after((steps + 1) * delay,
              lambda: widget.configure(fg_color=theme_color))

def switchSavePage():
    homePage.forget()
    SavePage.pack()

def switchLoadPage():
    homePage.forget()
    SavePage.pack()

def saveToJson():
    password = PasswordEntry.get()
    WebsiteIn = WebsiteEntry.get()
    encrypted = cipher.encrypt(password.encode())


    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[WebsiteIn] = encrypted.decode()


    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)

    ValidationFrame.pack(pady=(30, 0))
    ValidationLabel.configure(text="Saved Password")
    ValidationLabel.pack(padx=30)
    glow_effect(ValidationFrame, steps=50, start_rgb=(0, 255, 0,), delay=10)

def CheckKey():
    global key

    if os.path.exists("key.key"):
        with open("key.key", "rb") as file:
            key = file.read()
        print("Key Read")
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as file:
            file.write(key)

CheckKey()

cipher = Fernet(key)




homePage = ctk.CTkFrame(app, fg_color="transparent")
SavePage = ctk.CTkFrame(app, fg_color="transparent")
LoadPage = ctk.CTkFrame(app, fg_color="transparent")


####################################################################################################
homePage.pack(fill="both", expand=True)

TextFrame = ctk.CTkFrame(homePage, height=50)
TextFrame.pack(pady=(300, 10), anchor="center")

TextLabel = ctk.CTkLabel(TextFrame, text="Do you want to Get or Safe a password?", font=("Arial", 30, "bold"))
TextLabel.pack(padx=30, pady=20)

ButtonFrame = ctk.CTkFrame(homePage, width=1400, fg_color="transparent")
ButtonFrame.pack(fill="both", expand=True)

SaveButton = ctk.CTkButton(ButtonFrame, text="Save Password", height=100, width=300, font=("Arial", 30, "bold"), command=switchSavePage)
SaveButton.pack(pady= 150, padx=(570, 0), side="left", anchor="n")

GetButton = ctk.CTkButton(ButtonFrame, text="Get Password", height=100, width=300, font=("Arial", 30, "bold"), command=switchLoadPage)
GetButton.pack(pady= 150, padx=(0, 570), side="right", anchor="n")

####################################################################################################

####################################################################################################

WebsiteLabel = ctk.CTkLabel(SavePage, text="Enter the Website you want to store the Password from")

WebsiteEntry = ctk.CTkEntry(SavePage, placeholder_text="e.g Google, Yahoo, ...", font=("Arial", 26), width=700, height=50)
WebsiteEntry.pack(pady=(250, 0))

PasswordEntry = ctk.CTkEntry(SavePage, placeholder_text="Enter Your password", font=("Arial", 26), width=700, height=50)
PasswordEntry.pack(pady=(130, 0))

ContinueButton = ctk.CTkButton(SavePage, text="Continue", font=("Arial", 30, "bold"), command=saveToJson)
ContinueButton.pack(pady=(100, 0), anchor="center")

ValidationFrame = ctk.CTkFrame(SavePage)
ValidationLabel = ctk.CTkLabel(ValidationFrame, text="", font=("Arial", 20))

####################################################################################################







LeaveButton = ctk.CTkButton(app, text="Leave", command=app.destroy)
LeaveButton.pack(pady=10, padx=10, anchor="se")
key = None


# 
# 
# 
# readwrite = input("Do you want to read your password? (Y/N)\n")
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# if readwrite == "Y":
#     
#     
#     
# 
#     
# 
# elif readwrite == "N":
#     try:
#         WebsiteOut = input("From which website do you want to know the Password from?\n")
# 
#         with open("passwords.json", "r") as file:
#             data = json.load(file)
# 
#         passwordOut = cipher.decrypt(data[WebsiteOut]).decode()
# 
#         print(f"Your Password for {WebsiteOut} is {passwordOut}")
#     except KeyError:
#         print("You Do not have that Websites Password stored")

app.mainloop()