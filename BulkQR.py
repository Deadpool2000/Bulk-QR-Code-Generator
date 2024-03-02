import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
import zipfile
import os
import shutil
from PIL import Image

class ShowFileDialog(tk.Toplevel):
    def __init__(self, master, file_path):
        super().__init__(master)
        self.title("Show File in Explorer")
        self.geometry("300x100")
        self.file_path = file_path

        label = tk.Label(self, text="Do you want to show the file in Explorer?")
        label.pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack()

        yes_button = tk.Button(button_frame, text="Yes", command=self.show_in_explorer)
        yes_button.pack(side=tk.LEFT, padx=10)

        no_button = tk.Button(button_frame, text="No", command=self.destroy)
        no_button.pack(side=tk.LEFT)

    def show_in_explorer(self):
        folder_path = os.path.dirname(self.file_path)
        if os.path.exists(folder_path):
            os.startfile(folder_path)
            self.destroy()
        else:
            messagebox.showerror("Error", "Folder not found.")
            self.destroy()

class QRCodeGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Free Bulk QR Code Generator 1.0 - By @Deadpool2000")

        self.file_label = tk.Label(master, text="List for QR (txt):")
        self.file_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.file_entry = tk.Entry(master, width=50)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_file_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_file_button.grid(row=0, column=2, padx=5, pady=5)

        self.textfile2_label = tk.Label(master, text="Name File (txt):")
        self.textfile2_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.textfile2_entry = tk.Entry(master, width=50)
        self.textfile2_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_textfile2_button = tk.Button(master, text="Browse", command=self.browse_textfile2)
        self.browse_textfile2_button.grid(row=1, column=2, padx=5, pady=5)

        self.resolution_label = tk.Label(master, text="QR Resolution (pixels):")
        self.resolution_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.resolution_entry = tk.Entry(master, width=50)
        self.resolution_entry.grid(row=2, column=1, padx=5, pady=5)

        self.generate_button = tk.Button(master, text="Generate QR Codes", command=self.generate_qr_codes)
        self.generate_button.grid(row=3, column=1, padx=5, pady=10)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=4, column=1, padx=5, pady=5)

        # Disable maximize button and set window size
        master.resizable(False, False)
        master.geometry("520x150")

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, filename)

    def browse_textfile2(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.textfile2_entry.delete(0, tk.END)
        self.textfile2_entry.insert(0, filename)

    def generate_qr_codes(self):
        file_path = self.file_entry.get()
        textfile2_path = self.textfile2_entry.get()
        resolution = self.resolution_entry.get()

        if not os.path.exists(file_path):
            self.result_label.config(text="File list for QR not found.")
            return
        if not os.path.exists(textfile2_path):
            textfile2_path = file_path
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        filename_set = set()
        with open(file_path, 'r') as file, open(textfile2_path, 'r') as textfile2:
            for record, filename in zip(file, textfile2):
                record = record.strip()
                filename = filename.strip()
                file_index = 1
                new_filename = f"{filename}.png"
                while new_filename in filename_set:
                    new_filename = f"{filename}_{file_index}.png"
                    file_index += 1
                qr = qrcode.QRCode(version=None, box_size=10, border=4)
                qr.add_data(record)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white").resize((int(resolution), int(resolution)),
                                                                                     Image.BILINEAR)
                filename_set.add(new_filename)
                filename = f"{temp_dir}/{new_filename}"
                img.save(filename, format='PNG')

        zip_filename = f"{os.path.splitext(textfile2_path)[0]}.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            for filename in os.listdir(temp_dir):
                zip_file.write(f"{temp_dir}/{filename}", arcname=filename)
        shutil.rmtree(f'{temp_dir}')
        self.show_success_message(zip_filename)

    def show_success_message(self, zip_filename):
        message = "QR Codes generated successfully. Do you want to show the file in Explorer?"
        if messagebox.askyesno("Success", message):
            ShowFileDialog(self.master, zip_filename)


def main():
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
