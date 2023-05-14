from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, Canvas, filedialog


class ImageToAlphaMapConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Alpha Map Converter")

        self.image_path = ""
        self.output_path = ""

        self.label = Label(
            root, text="Click 'Upload' to select an image, then click 'Preview' to see the alpha map.")
        self.label.pack(padx=10, pady=10)

        self.upload_button = Button(
            root, text="Upload", command=self.upload_image)
        self.upload_button.pack(padx=10, pady=5)

        self.preview_button = Button(
            root, text="Preview", command=self.preview_alpha_map, state="disabled")
        self.preview_button.pack(padx=10, pady=5)

        self.export_button = Button(
            root, text="Export", command=self.export_alpha_map, state="disabled")
        self.export_button.pack(padx=10, pady=5)

        self.canvas = Canvas(root, width=300, height=300)
        self.canvas.pack(padx=10, pady=10)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=(
            ("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")))

        if self.image_path:
            self.preview_button.config(state="normal")

    def preview_alpha_map(self):
        # Open the image
        image = Image.open(self.image_path)

        # Convert the image to grayscale
        grayscale_image = image.convert("L")

        # Create a new image with alpha channel
        alpha_image = Image.new("LA", grayscale_image.size)

        # Set the grayscale values as the alpha channel
        alpha_image.paste(grayscale_image, (0, 0))

        # Resize the alpha map image for preview
        alpha_image.thumbnail((300, 300), Image.LANCZOS)

        # Display the alpha map preview
        self.alpha_map_preview = ImageTk.PhotoImage(alpha_image)
        self.canvas.create_image(
            0, 0, anchor="nw", image=self.alpha_map_preview)

        self.export_button.config(state="normal")

    def export_alpha_map(self):
        self.output_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))

        if self.output_path:
            # Open the image
            image = Image.open(self.image_path)

            # Convert the image to grayscale
            grayscale_image = image.convert("L")

            # Create a new image with alpha channel
            alpha_image = Image.new("LA", grayscale_image.size)

            # Set the grayscale values as the alpha channel
            alpha_image.paste(grayscale_image, (0, 0))

            # Save the alpha map image
            alpha_image.save(self.output_path)

            self.label.config(text="Alpha map exported successfully!")


root = Tk()
app = ImageToAlphaMapConverter(root)
root.mainloop()
