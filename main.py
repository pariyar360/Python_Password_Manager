import json
from tkinter import *
from tkinter import messagebox

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    # generating random characters based on how many we need with minimum and maximum value
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for letter in range(nr_letters)]
    password_symbols = [random.choice(symbols) for letter in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for letter in range(nr_numbers)]
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    generated_password = "".join(password_list)
    password_input.delete(0, END)
    password_input.insert(END, generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_info():
    website = website_input.get().capitalize()
    user_id = id_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": user_id,
            "password": password,
        }
    }
    if website == "" or password == "" or user_id == "":
        messagebox.showwarning(title="Empty boxes", message="Please do not leave any fields empty. :)")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Details Entered: \n"
                                                              f"User ID     : {user_id}\n"
                                                              f"Password : {password}\n"
                                                              f"Are these correct and ready to save?")

        if is_ok:
            try:
                with open("data.json", mode="r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    # Saving data
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data
                data.update(new_data)
                with open("data.json", mode="w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                # Deleting inputs in canvas
                website_input.delete(0, END)
                password_input.delete(0, END)


# -----------------------------Search Setup-------------------------------


def search_data():
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
            website = website_input.get().capitalize()
    except FileNotFoundError:
        messagebox.showerror(title="File Error", message="File not Found!")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showerror(title="Data Error", message=f"Details for {website} not Found!")


# ---------------------------- UI SETUP ------------------------------- #
windows = Tk()
windows.title("Password Manager")
windows.config(pady=50, padx=50)

canvas = Canvas()
canvas.config(width=200, height=200)

# Photo setup
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# Labels and inputs
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_input = Entry()
website_input.grid(column=1, row=1, sticky="ew")
# when the program runs, it is automatically focused to enter the website details
website_input.focus()

id_label = Label(text="Email/Username:")
id_label.grid(column=0, row=2)
id_input = Entry()
id_input.grid(column=1, row=2, columnspan=2, sticky="ew")
# Autofill the email id
id_input.insert(END, "pariyar360@gmail.com")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_input = Entry()
password_input.grid(column=1, row=3, sticky="ew")

# generate button
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, sticky="ew")

# Add button
add_button = Button(text="Add", command=save_info)
add_button.grid(column=1, row=4, columnspan=2, sticky="ew")

# Search button
search_button = Button(text="Search", command=search_data)
search_button.grid(column=2, row=1, sticky="ew")

windows.mainloop()
