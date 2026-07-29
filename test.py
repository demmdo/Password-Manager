import customtkinter as ctk
import json


app = ctk.CTk()

with open("passwords.json", "r") as file:
    data = json.load(file)

websites = list(data.keys())

combo = ctk.CTkComboBox(
    app,
    values=websites
)

combo.pack(pady=20)

app.mainloop()