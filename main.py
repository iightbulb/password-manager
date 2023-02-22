from asyncio.base_subprocess import WriteSubprocessPipeProto
import tkinter
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = "Arial"
BLUE = "#4649ff"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    password_entry.delete(0, tkinter.END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

    
# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    global website
    website = website_entry.get()
    email = username_entry.get()
    passw = password_entry.get()
    global new_data
    new_data = {
        website.lower(): {
             "email": email,
             "password": passw,
        }
    }

    if len(website) == 0 or len(passw) == 0:
        messagebox.showinfo(title="Error", message="Please don't leave any fields blank.")
    else:
        try:   
            with open("data.json", "r") as file:
            #read old data
                data = json.load(file)
            #updating old data with new data
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as file:
            #saving updated data
                json.dump(new_data, file, indent=4)
        else:
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, tkinter.END)
            password_entry.delete(0, tkinter.END)
        messagebox.showinfo(title="Saved", message="Your information has been saved.")

#---------------------------- FIND PASSWORD ------------------------------------#

def search():
    website = website_entry.get()
    try:
        with open("data.json") as file:
            data = json.load(file)
            if website.lower() in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website.title(), message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message=f"There are no details for {website.title()}.")
    except FileNotFoundError:
        messagebox.showinfo(title="No data", message="No data file found.")
    finally:
        website_entry.delete(0, tkinter.END)
        password_entry.delete(0, tkinter.END)


# ---------------------------- UI SETUP ------------------------------- #

window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


#canvas
canvas = tkinter.Canvas(width=200, height=200)
logo_img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)


#labels
website_label = tkinter.Label(text="Website:", font=(FONT_NAME, 10))
website_label.grid(column=0, row=1)

username_label = tkinter.Label(text="Email/Username:", font=(FONT_NAME, 10))
username_label.grid(column=0, row=2)

password_label = tkinter.Label(text="Password:", font=(FONT_NAME, 10))
password_label.grid(column=0, row=3)


#Entries
website_entry = tkinter.Entry(width=30)
website_entry.focus()
website_entry.grid(column=1, row=1)

username_entry = tkinter.Entry(width=30)
username_entry.insert(0, string="tjfillis@gmail.com")
username_entry.grid(column=1, row=2)

password_entry = tkinter.Entry(width=30)
password_entry.grid(column=1, row=3)


#Buttons
generate_password_button = tkinter.Button(text="Generate Pass", command=generate_password, font=(FONT_NAME, 8))
generate_password_button.grid(column=2, row=3)

add_button = tkinter.Button(text="Add", command=save_data, width=16, font=(FONT_NAME, 8))
add_button.grid(column=1, row=4)

search_button = tkinter.Button(text="Search", command=search, width=12, font=(FONT_NAME, 8))
search_button.grid(column=2, row=1)



window.mainloop()