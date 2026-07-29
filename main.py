from cryptography.fernet import Fernet
import customtkinter as ctk
import json
import os
import pyperclip

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

key = None

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
    LoadPage.pack()

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



WebsiteEntry = ctk.CTkEntry(SavePage, placeholder_text="e.g Google, Yahoo, ...", font=("Arial", 26), width=700, height=50)
WebsiteEntry.pack(pady=(250, 0))

PasswordEntry = ctk.CTkEntry(SavePage, placeholder_text="Enter Your password", font=("Arial", 26), width=700, height=50)
PasswordEntry.pack(pady=(130, 0))

ContinueButton = ctk.CTkButton(SavePage, text="Continue", font=("Arial", 30, "bold"), command=saveToJson)
ContinueButton.pack(pady=(100, 0), anchor="center")

ValidationFrame = ctk.CTkFrame(app)
ValidationLabel = ctk.CTkLabel(ValidationFrame, text="", font=("Arial", 20))

####################################################################################################

WebsiteLabel = ctk.CTkLabel(LoadPage, text="Enter the Website you want to store the Password from", font=("Arial", 30, "bold"))
WebsiteLabel.pack()

def LoadPassword():
    global WebsiteOut
    global passwordOut

    PasswordFrame.pack(pady=30)
    PasswordLabel.pack(pady=10, padx=100, side="left", anchor="center")
    PasswordCopyButton.pack(side = "right", padx=(0,5))
    WebsiteOut = Selection.get()
    passwordOut = cipher.decrypt(data[WebsiteOut]).decode()
    PasswordLabel.configure(text=passwordOut)

def copyPassword():
    pyperclip.copy(passwordOut)
    ValidationLabel.configure(text="Copied Password")
    ValidationFrame.pack(pady=(30, 0))
    ValidationLabel.pack(padx=30)
    glow_effect(ValidationFrame, steps=50, start_rgb=(0, 255, 0,), delay=10)

with open("passwords.json", "r") as file:
    data = json.load(file)


websites = list(data.keys())

Selection = ctk.CTkComboBox(LoadPage, values=websites, state="normal")
Selection.pack(pady=(150, 0))



if Selection.get() != "normal":
    GetPasswordButton = ctk.CTkButton(LoadPage, text="Get Password", command=LoadPassword)
    GetPasswordButton.pack(pady=(90, 0))



PasswordFrame = ctk.CTkFrame(LoadPage, width=400)

PasswordLabel = ctk.CTkLabel(PasswordFrame, font=("Arial", 20, "bold"))

PasswordCopyButton = ctk.CTkButton(PasswordFrame, text="⧉ Copy", command=copyPassword)



LeaveButton = ctk.CTkButton(app, text="Leave", command=app.destroy)
LeaveButton.pack(pady=10, padx=10, anchor="se")

key = None

app.mainloop()