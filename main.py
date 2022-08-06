import json
import random
from tkinter import *
from tkinter import messagebox


APP_NAME = "MyPass"
DATA_FILE_PATH = "data.json"
FONT = {"name": "Times New Roman", "size": 12, "type": "normal"}
INNER_PAD = 4
OUTER_PAD = 2

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

password = ""


def generate_password():
    global password
    password = ""
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
    
    password_list = [random.choice(LETTERS) for char in range(nr_letters)]
    password_list.extend([random.choice(SYMBOLS) for char in range(nr_symbols)])
    password_list.extend([random.choice(NUMBERS) for char in range(nr_numbers)])
    
    random.shuffle(password_list)
    
    password = password.join(password_list)

    password_input.delete(0, END)
    password_input.insert(0, password)
    

#Check all inputs including password (will call 'validate_password' at the last step)
def validate_data():
    #Get inputs
    website = website_input.get()
    email = email_input.get()
    

    #Check for emptyness, than validate URL, email and pass
    if len(website) > 0 and len(email) > 0:
        if '.' in website:
            dot_index = website.index('.')
            
            if len(website) - dot_index > 3:
                if '@' in email:
                    at_index = email.index('@')
                    
                    if '.' in email[at_index:]:
                        dot_index = email.index('.')
                        
                        if dot_index - at_index > 2 and len(email) - dot_index > 3:
                            validate_password()
                            return
                
                messagebox.showwarning(title="Invalid Email", message="Your email seems to be invalid. Check it please!")
                return
        
        messagebox.showwarning(title="Invalid URL", message="The website URL seems to be invalid. Check it please!")
        return
    
    messagebox.showwarning(title="No Data", message="Please, type in a website URL and your email")
        

#Separate function on pass validation
def validate_password():
    global password
    password = password_input.get()
    
    num_of_numbers = sum(number.isdigit() for number in password)
    num_of_letters = sum(letter.isalpha() for letter in password)
    num_of_symbols = sum(symbol in SYMBOLS for symbol in password)
    
    if num_of_letters >= 8 and num_of_letters <= 10:
        if num_of_numbers >= 2 and num_of_numbers <= 4:
            if num_of_symbols >= 2 and num_of_symbols <= 4:
                save()
            else:
                messagebox.showwarning(title="Wrong Password", message="The password should contain  from 2 to 4 special characters ('!', '#', '$', '%', '&', '(', ')', '*', '+')")
        else:
            messagebox.showwarning(title="Wrong Password", message="The password should contain from 2 to 4 NUMBERS.")
    else:
        messagebox.showwarning(title="Wrong Password", message="The password should contain from 8 to 10 characters (lowercase or uppercase).")


#Search for a password in the database
def search():
    website = website_input.get()
    
    #Not calling 'validate_data()' in case a user wants firstly search for a record
    if len(website) > 0:
        try:
            with open(file=DATA_FILE_PATH, mode="r") as data_file:
                passwords = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showerror(title="Missing Data", message="There is not any data saved yet.")
        else:
            for key, value in passwords.items():
                found_email = ""
                found_password = ""
                
                if key == website:
                    found_email = value["email"]
                    found_password = value["password"]
                    messagebox.showinfo(title="Password Searching", message=f"The password for {website} website was found!\nLogin: {found_email}\nPassword:{found_password}")
                    break
                
            messagebox.showinfo(title="Password Searching", message=f"Unfortunately, there is no any password for {website} website...")
    else:
        messagebox.showinfo(title="Password Searching", message="The field is empty!")


#Finally save all data
def save():
    website = website_input.get()
    email = email_input.get()
        
    respond = messagebox.askokcancel(title=website, message=f"These are the details You entered:\nWebsite: {website}\nEmail: {email}\nPassword: {password}\nIs it ok to save?")
    
    if respond:
        #Prepare new data before saving it
        new_password = {
            website: {
                "email": email,
                "password": password,
            }
        }
        
        #Try to open the data-file. If it's not there, we'll create it from scratch
        try:
            with open(DATA_FILE_PATH, "r") as data_file:
                passwords = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open(DATA_FILE_PATH, "w") as data_file:
                json.dump(new_password, data_file, indent=4)
        else:
            passwords.update(new_password)
            
            with open(DATA_FILE_PATH, "w") as data_file:
                json.dump(passwords, data_file, indent=4)
        #Empty inputs after saving data
        finally:
            website_input.delete(0, END)
            email_input.delete(0, END)
            password_input.delete(0, END)
            messagebox.showinfo(title="Job's done ;)", message="Your password has been successfully saved.")
    else:
        messagebox.showinfo(title="Pass Saving", message="Action was declined.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title(APP_NAME)
window.config(padx=40, pady=40, bg="white")
canvas = Canvas(height=200, width=200, bg="white", highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website_label = Label(text="Website: ", bg="white", font=(FONT["name"], FONT["size"], FONT["type"]))
website_label.grid(row=1, column=0, pady=OUTER_PAD)

email_label = Label(text="Email/Username: ", bg="white", font=(FONT["name"], FONT["size"], FONT["type"]))
email_label.grid(row=2, column=0, pady=OUTER_PAD)

password_label = Label(text="Password", bg="white", font=(FONT["name"], FONT["size"], FONT["type"]))
password_label.grid(row=3, column=0, pady=OUTER_PAD)

website_input = Entry(width=24, bg="white")
website_input.grid(row=1, column=1, sticky='wens', ipady=INNER_PAD, padx=OUTER_PAD, pady=OUTER_PAD)
website_input.focus()

email_input = Entry(width=35, bg="white")
email_input.grid(row=2, column=1, columnspan=2, sticky='wens', ipady=INNER_PAD, padx=OUTER_PAD, pady=OUTER_PAD)

password_input = Entry(width=24, bg="white")
password_input.grid(row=3, column=1, sticky='wens', padx=OUTER_PAD, pady=OUTER_PAD)

add_button = Button(text="Add", width=34, bg='white', font=(FONT["name"], FONT["size"], FONT["type"]), command=validate_data)
add_button.grid(row=4, column=1, columnspan=2, sticky='we', padx=OUTER_PAD, pady=OUTER_PAD)

generate_button = Button(text="Generate Password", width=20, bg='white', font=(FONT["name"], FONT["size"], FONT["type"]), command=generate_password)
generate_button.grid(row=3, column=2, sticky='wens', padx=OUTER_PAD, pady=OUTER_PAD)

search_button = Button(text="Search for a Password", width=20, bg='white', font=(FONT["name"], FONT["size"], FONT["type"]), command=search)
search_button.grid(row=1, column=2, sticky='wens', padx=OUTER_PAD, pady=OUTER_PAD)

window.mainloop()