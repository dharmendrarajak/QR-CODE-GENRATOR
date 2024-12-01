from tkinter import *
import requests
from PIL import Image, ImageTk
import io
import os

root = Tk()
root.geometry("400x400")
root.title("QR Code Generator")

keywordVar = StringVar()
fileNameVar = StringVar()

def generateQR():
    # Get the keyword and file name from input
    keyword = keywordVar.get()
    file_name = fileNameVar.get()

    # Validate input
    if not keyword or not file_name:
        Label(root, text="Keyword and File Name are required", fg="red").pack()
        return

    # Generate the QR code API URL
    api = f"https://api.qrserver.com/v1/create-qr-code/?data={keyword}&size=150x150"  # Adjusted size to 150x150

    # Fetch the QR code image from the API
    try:
        response = requests.get(api)
        response.raise_for_status()  # Raise an error if the request fails
        image = response.content

        # Save the image to a file
        save_path = os.path.join(os.getcwd(), f"{file_name}.png")  # Save in current directory
        with open(save_path, "wb") as file:
            file.write(image)

        Label(root, text=f"QR Code saved as {file_name}.png", fg="green").pack()

        # Load the image using PIL
        image = Image.open(io.BytesIO(image))
        image = ImageTk.PhotoImage(image)

        # Create a label to display the image
        imageLabel = Label(root, image=image)
        imageLabel.image = image  # Keep a reference to avoid garbage collection
        imageLabel.pack()

    except requests.exceptions.RequestException as e:
        Label(root, text=f"Error: {e}", fg="red").pack()

keywordLabel = Label(root, text="Enter Keyword")
keywordLabel.pack()

keywordEntry = Entry(root, textvariable=keywordVar)
keywordEntry.pack()

fileNameLabel = Label(root, text="Enter File Name")
fileNameLabel.pack()

fileNameEntry = Entry(root, textvariable=fileNameVar)
fileNameEntry.pack()

generateButton = Button(root, text="Generate QR Code", command=generateQR)
generateButton.pack()

root.mainloop()
