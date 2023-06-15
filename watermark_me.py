from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def select_image():
    global image_path, image_label, watermarked_image

    # Prompt the user to select an image file
    filetypes = (("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*"))
    image_path = filedialog.askopenfilename(title = "Select Image", filetypes = filetypes)

    # Open and display the selected image
    image = Image.open(image_path)
    image = image.resize((500, 500))  # Resize the image for display
    image_tk = ImageTk.PhotoImage(image)
    image_label.configure(image = image_tk)
    image_label.image = image_tk

    # Apply watermark
    watermarked_image = apply_watermark(image)

    # Activate the "Save" button
    save_button.config(state = tk.NORMAL)


def apply_watermark(image):
    # Create a watermark on the image
    watermark_text = "Watermark"
    font = ImageFont.truetype("arial.ttf", 20)  # Change the font and size as needed
    padding = 10  # Adjust the padding value as desired

    # Create a transparent image for the watermark
    watermark = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    # Calculate the watermark position in the right corner with padding
    watermark_width, watermark_height = draw.textsize(watermark_text, font)
    x = image.width - watermark_width - padding
    y = padding

    # Draw the watermark text on the transparent image
    draw.text((x, y), watermark_text, font = font, fill = (255, 255, 255, 128))

    # Composite the watermark onto the image
    watermarked_image = Image.alpha_composite(image.convert("RGBA"), watermark)

    return watermarked_image


def save_image():
    global watermarked_image, image_path

    if watermarked_image:
        # Get the original file name and directory path
        original_file_path, original_file_name = os.path.split(image_path)

        # Append "_w" at the end of the file name
        watermarked_file_name = original_file_name[:-4] + "_w" + ".png"

        # Create the watermarked file path in the same directory
        watermarked_file_path = os.path.join(original_file_path, watermarked_file_name)

        # Save the watermarked image
        watermarked_image.save(watermarked_file_path)

        # Show success message
        messagebox.showinfo("Success", "Image saved successfully.")

        # Open the folder with the saved file
        os.startfile(original_file_path)


# Variables
image_path = None
watermarked_image = None

# Create the main window
root = tk.Tk()
root.title("Watermark me")
root.geometry("800x800")

# Create a frame to contain the elements
frame = tk.Frame(root)
frame.pack(expand = True, pady = 10, anchor = tk.CENTER)

# Create a label for the image
image_label = tk.Label(frame)
image_label.grid(row = 0, column = 0, columnspan = 2, pady = 5)

# Create a label for the title
title_label = tk.Label(frame, text = "Choose an image to add watermark.")
title_label.grid(row = 1, column = 0, columnspan = 2, pady = 10)

# Create the "Upload" button
upload_button = tk.Button(frame, text = "Upload", command = select_image)
upload_button.grid(row = 2, column = 0, columnspan = 2, pady = (0, 10))

# Create the "Save" button
save_button = tk.Button(frame, text = "Save", command = save_image, state = tk.DISABLED)
save_button.grid(row = 3, column = 0)

# Create the "Close" button
close_button = tk.Button(frame, text = "Close", command = root.destroy)
close_button.grid(row = 3, column = 1)

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 800
window_height = 800
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Start the main event loop
root.mainloop()
