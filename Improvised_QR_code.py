from tkinter import *
from tkinter import messagebox #------
from tkinter import ttk #------
import os
import io #------
import csv #------
import pyqrcode
import png #------
import datetime #------
#from datetime import datetime #------
from cryptography.fernet import Fernet #------
from PIL import Image, ImageTk, ImageGrab #------
from tkinter import filedialog #------
import smtplib #------
from email.mime.text import MIMEText #------
from email.mime.multipart import MIMEMultipart #------
from email.mime.image import MIMEImage #------
# SHASHANK KENY, 33, BEITB

#----------------------------------------------------------
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.starttls()
smtp_server.login('your_emailID@gmail.com', 'your_password')
#----------------------------------------------------------
encryption_key = Fernet.generate_key() #------
cipher_suite = Fernet(encryption_key) #------

window = Tk()
window.title("QR Code Generator")

file_name = ""
selected_format = ""

#Set App icon  
window.iconbitmap(r'QR.ico') #------

def send_email(file_name):  
    email_address = email_entry.get()
    if not email_address:
        messagebox.showinfo("Email Address Missing", "Please enter an email address.")
        return

    subject = "QR Code"
    message = "Please find the QR code attached."

    msg = MIMEMultipart()
    msg['From'] = 'your_emailID@gmail.com'
    msg['To'] = email_address
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Attach the QR code image to the email using the passed file_name
    qr_image_path = os.path.join(os.getcwd(), f"{file_name}")
    if os.path.exists(qr_image_path):
        qr_image = open(qr_image_path, 'rb').read()
        image_attachment = MIMEImage(qr_image, name=os.path.basename(qr_image_path))
        msg.attach(image_attachment)

        try:
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login('your_emailID@gmail.com', 'your_password')
            smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
            smtp_server.quit()
            messagebox.showinfo("Email Sent", "QR code email sent successfully.")
        except Exception as e:
            messagebox.showinfo("Email Error", f"An error occurred while sending the email: {str(e)}")
    else:
        messagebox.showinfo("File Not Found", f"File not found at path: {qr_image_path}")

def generate1(): #-----NO ENCRYPTION-----#
    if len(Subject.get())!=0 :
        global qr,photo,selected_format
        qr = pyqrcode.create(Subject.get())
        photo = BitmapImage(data = qr.xbm(scale=8))
        try:
            showcode()
        except:
            pass
        messagebox.showinfo("QR Code Generated", "QR code has been generated successfully.")
        # Save details to CSV
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_to_csv(f"QR of {Subject.get()}", "PNG", os.getcwd(), current_datetime, email_entry.get(), "No")
    else:
        messagebox.showinfo("Please Enter Subject", "Please enter some subject.")

def generate2(): #-----ADDING ENCRYPTION(AES)-----#
    if len(Subject.get()) != 0:
        global qr, photo, selected_format
        if encryption_key is None:
            messagebox.showinfo("Key Missing", "Encryption key is missing.")
            return
        data = Subject.get().encode()  # Convert data to bytes
        encrypted_data = cipher_suite.encrypt(data)  # Encrypt data
        qr = pyqrcode.create(encrypted_data)
        photo = BitmapImage(data=qr.xbm(scale=8))
        print("Encrypted Data:\n", encrypted_data)  # Print the encrypted data
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        print("Decrypted Data:\n\t", decrypted_data)  # Print the decrypted data
        print()
        try:
            showcode()
        except:
            pass
        messagebox.showinfo("QR Code(AES)Generated", "QR code(AES Encrytped)has been generated successfully.")
        # Save details to CSV
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_to_csv(f"QR of {Subject.get()}",selected_format, os.getcwd(), current_datetime, email_entry.get(), "Yes")
    else:
        messagebox.showinfo("Please Enter Subject", "Please enter some subject.") #------
# SHASHANK KENY, 33, BEITB

def showcode():
    imageLabel.config(image=photo)
    subLabel.config(text="QR of " + Subject.get())
    imageLabel.bind("<Button-3>", show_context_menu)

def clear_fields():
    SubEntry.delete(0, 'end')
    email_entry.delete(0, 'end')
    imageLabel.config(image=None)
    subLabel.config(text="")
    file_name = ""
    global photo
    photo = None
# SHASHANK KENY, 33, BEITB

def show_context_menu(event):
    print("Right-click event triggered")
    context_menu = Menu(window, tearoff=0)
    context_menu.add_command(label="Copy QR Code", command=copy_to_clipboard)
    context_menu.add_separator()
    context_menu.add_command(label="Save QR Code", command=save)
    context_menu.post(event.x_root, event.y_root) #------


def copy_to_clipboard(event=None): #------
    qr_image = pyqrcode.create(Subject.get())
    qr_image_path = os.path.join(os.getcwd(), "temp_qr_image.png")
    qr_image.png(qr_image_path, scale=8)
    pil_image = Image.open(qr_image_path)
    photo_image = ImageTk.PhotoImage(pil_image)
    window.clipboard_clear()
    window.clipboard_append(photo_image)
    os.remove(qr_image_path)  # Remove the temporary image file
    messagebox.showinfo("Copied", "QR code image copied to clipboard.") #------

def save():
    global file_name
    global selected_format

    dir = os.getcwd()
    if not os.path.exists(dir):
        os.makedirs(dir)

    selected_format = format_var.get()

    try:
        if len(Subject.get()) != 0:
            #if not file_name:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"QR of {Subject.get()}_{current_datetime}.{selected_format}"

            file_path = filedialog.asksaveasfilename(
                initialdir=dir,
                initialfile=file_name,
                defaultextension="." + selected_format,
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpeg"),
                    ("BMP files", "*.bmp"),
                    ("All files", "*.*"),
                ],
            )
            if file_path:
                if selected_format == "png":
                    qr.png(file_path, scale=8)
                elif selected_format == "jpeg":
                    qr.png(file_path, scale=8)
                elif selected_format == "bmp":
                    qr.png(file_path, scale=8)
                else:
                    messagebox.showinfo(
                        "Unsupported Format", "Selected image format is not supported."
                    )
                # Update the file_name variable and then send the email
                file_name = os.path.basename(file_path)
                #send_email(file_name)
        else:
            messagebox.showinfo("Warning", "Please enter a File Name")
    except Exception as e:
        messagebox.showinfo("Save Error", f"An error occurred while saving the QR code: {str(e)}")
# SHASHANK KENY, 33, BEITB

def save_to_csv(file_name, image_format, location_path, timestamp, email_address, encrypted):
    with open('QRcode_Database.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([file_name, image_format, location_path, timestamp, email_address, encrypted])

Sub = Label(window, text="Enter subject")
Sub.grid(row=0, column=0, sticky=N+S+W+E, padx=10, pady=10)

#FName = Label(window, text="Enter FileName")
#FName.grid(row=1, column=0, sticky=N+S+W+E, padx=10, pady=10)

Subject = StringVar()
SubEntry = Entry(window,textvariable = Subject)
SubEntry.grid(row =0,column =1,sticky=N+S+W+E, padx=10, pady=10)

#nameEntry = Entry(window,textvariable = name)
#nameEntry.grid(row =1,column =1,sticky=N+S+W+E, padx=10, pady=10)

button1 = Button(window,text = "Generate",width=15,command = generate1)
button1.grid(row =0,column =2,sticky=N+S+W+E, padx=10, pady=10)

button2 = Button(window,text = "Generate(AES)",width=15,command = generate2)
button2.grid(row =0,column =3,sticky=N+S+W+E, padx=10, pady=10)

saveB = Button(window,text="Save",width=15,command = save)
saveB.grid(row =1,column =2,sticky=N+S+W+E, padx=10, pady=10)

format_var = StringVar()
format_var.set("png")  # Set the default format to PNG

email_label = Label(window, text="Enter Email Address")
email_label.grid(row=1, column=0, sticky=N+S+W+E, padx=10, pady=10)

email_entry = Entry(window)
email_entry.grid(row=1, column=1, sticky=N+S+W+E, padx=10, pady=10)

email_button = Button(window, text="Send Email", width=15, command=lambda: send_email(file_name))
email_button.grid(row=1, column=2, sticky=N+S+W+E, padx=10, pady=10)


clear_button = Button(window, text="Clear", width=15, command=clear_fields)
clear_button.grid(row=5, column=1, sticky=N+S+W+E, padx=10, pady=10)

# Adjust the position of the QR code and labels
imageLabel = Label(window)
subLabel = Label(window,text="")
imageLabel.grid(row=3, columnspan=4, sticky=N+S+W+E)
subLabel.grid(row=4, columnspan=4, sticky=N+S+W+E)
saveB.grid(row=1, column=3, sticky=N+S+W+E)

#making this resposnsive
Rows = 3
Columns = 3

for row in range(Rows+1):
    window.grid_rowconfigure(row,weight=1)

for col in range(Columns+1):
    window.grid_columnconfigure(col,weight=1)

window.mainloop()
# SHASHANK KENY, 33, BEITB
