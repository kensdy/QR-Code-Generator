import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import webbrowser

class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")

        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TButton', font=('Helvetica', 12))

        # Add a notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Start Page
        self.start_page = tk.Frame(self.notebook)
        self.notebook.add(self.start_page, text="Start")

        # Label to instruct the user
        instruction_label = tk.Label(self.start_page, text="Enter the content for the QR code", font=('Helvetica', 14))
        instruction_label.pack(fill=tk.X, pady=5)

        # Frame for the link input field
        link_frame = tk.Frame(self.start_page)
        link_frame.pack(fill=tk.X, pady=5)

        # Variable to store the link entered by the user
        self.link_var = tk.StringVar()

        # Entry field for the link
        self.link_entry = tk.Entry(link_frame, textvariable=self.link_var, width=30)
        self.link_entry.pack(fill=tk.X, ipadx=10, ipady=5, pady=5)

        # Button to generate QR code
        generate_qr_button = tk.Button(self.start_page, text="Generate QR Code", command=self.create_qr_code, bg='#4CAF50', fg='white')
        generate_qr_button.pack(fill=tk.X, ipadx=10, ipady=5, pady=5)

        # Button to choose file location and name
        save_button = tk.Button(self.start_page, text="Save As", command=self.save_as, bg='#008CBA', fg='white')
        save_button.pack(fill=tk.X, ipadx=10, ipady=5, pady=5)

        # Guide Page
        self.guide_page = tk.Frame(self.notebook)
        self.notebook.add(self.guide_page, text="Guide")

        # Formatted content using text widget and scrollbar
        guide_text = """
        QR Code Guide

        QR Code is a modern type of barcode that stores information, notable for its ability to contain more data. Scanned by smartphone cameras, QR codes make it easy to access links, contact information, events, Wi-Fi networks, and more. This guide illustrates how and for what QR codes can be generated, highlighting their versatility in different contexts, from sharing contact data to simplifying Wi-Fi network connection.

        - Link/URL: `https://www.example.com`
        - Plain Text: `Simple text for the QR code.`
        - Wi-Fi Credentials: `WIFI:T:WPA;S:MyWiFiNetwork;P:MyPassword123;;`
        - Geolocation (GPS coordinates): `geo:37.7749,-122.4194`
        - Text Message (SMS): `SMSTO:+123456789:Message text`
        - Emails: `mailto:example@email.com`
        - Phone Numbers: `tel:+123456789`
        - Bitcoin Address: `bitcoin:1DvF8f1hNvECX3HJ5ovC7eAeDXYFZPz8qp`
        - Text Notes: `NOTE:Text of the note`
        - Connect to a Bluetooth Network: `bluetooth:Device_MAC_Address`
        """

        guide_text_widget = tk.Text(self.guide_page, wrap=tk.WORD, width=80, height=25)
        guide_text_widget.insert(tk.END, guide_text)
        guide_text_widget.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(self.guide_page, command=guide_text_widget.yview)
        guide_text_widget.config(yscrollcommand=scrollbar.set)

        guide_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Information Page
        self.info_page = tk.Frame(self.notebook)
        self.notebook.add(self.info_page, text="Information")

        # Add an image, name, and link
        image_url = "img.png"  # Replace with the actual path of your image
        self.add_information(image_url, "Program Created by Kensdy", "Check the project repository here https://github.com/kensdy/QR-Code-Generator")

    def add_information(self, image_url, name, text):
        image = Image.open(image_url)
        image.thumbnail((100, 100))
        image_tk = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.info_page, image=image_tk)
        image_label.image = image_tk
        image_label.pack(pady=10)

        name_label = tk.Label(self.info_page, text=name, font=("Helvetica", 16, "bold"))
        name_label.pack(pady=5)

        # Text label with clickable link
        text_label = tk.Label(self.info_page, text=text, wraplength=400, justify="left", foreground="blue", cursor="hand2", font=('Helvetica', 10))
        text_label.pack(pady=10)
        text_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/kensdy/QR-Code-Generator"))

    def create_qr_code(self):
        link = self.link_var.get()

        if not link:
            messagebox.showwarning("Warning", "Please enter content for the QR code.")
            return

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        self.qr_image = img

        messagebox.showinfo("Success", "QR code created successfully. Click 'Save As' to choose the file location.")

    def save_as(self):
        if hasattr(self, 'qr_image'):
            file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")], title="Save As")

            if file_name:
                self.qr_image.save(file_name)
                messagebox.showinfo("Success", f"QR code saved as {file_name}")
        else:
            messagebox.showwarning("Warning", "Please generate the QR code first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
