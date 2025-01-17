import customtkinter
import os
from tkinter import filedialog, messagebox
import fitz
import sys
import tkinter as tk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ICON_PATH = resource_path("assets/app_icon.ico")

def select_pdf():
    file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=(("PDF Files", "*.pdf"),))
    if file_path:
        pdf_path.set(file_path)
        update_page_count()

def select_output_folder():
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    if folder_path:
        output_path.set(folder_path)

def update_page_count():
    try:
        if pdf_path.get():
            doc = fitz.open(pdf_path.get())
            page_count_label.configure(text=f"Total Pages: {doc.page_count}")
            doc.close()
        else:
            page_count_label.configure(text="Total Pages: ")
    except Exception as e:
        messagebox.showerror("Error", f"Error getting page count: {e}")

def convert_pdf_to_png():
    try:
        if not pdf_path.get() or not output_path.get():
            messagebox.showerror("Error", "Select PDF and output folder.")
            return

        dpi = int(dpi_entry.get()) if dpi_entry.get() else 300
        from_page = int(from_page_entry.get()) if from_page_entry.get() else None
        to_page = int(to_page_entry.get()) if to_page_entry.get() else None

        if from_page and to_page and from_page > to_page:
            messagebox.showerror("Error", "Invalid page range.")
            return

        doc = fitz.open(pdf_path.get())
        start_page = max(0, from_page - 1) if from_page else 0
        end_page = min(doc.page_count, to_page) if to_page else doc.page_count

        for page_num in range(start_page, end_page):
            page = doc[page_num]
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat)
            output_filename = os.path.join(output_path.get(), f"page_{page_num + 1}.png")
            pix.save(output_filename)

        doc.close()
        messagebox.showinfo("Success", f"{end_page - start_page} page(s) converted.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def toggle_fullscreen():
    fullscreen = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not fullscreen)
    root.geometry("600x450" if fullscreen else "{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

def minimize_window():
    root.iconify()

root = customtkinter.CTk()
root.title("PDF to PNG Converter")
root.geometry("600x450")
root.resizable(True, True)

try:
    root.iconbitmap(ICON_PATH)
except:
    pass

pdf_path = customtkinter.StringVar()
output_path = customtkinter.StringVar()

input_frame = customtkinter.CTkFrame(root)
input_frame.pack(pady=10, padx=20, fill="x")

output_frame = customtkinter.CTkFrame(root)
output_frame.pack(pady=10, padx=20, fill="x")

options_frame = customtkinter.CTkFrame(root)
options_frame.pack(pady=10, padx=20, fill="x")

convert_button_frame = customtkinter.CTkFrame(root)
convert_button_frame.pack(pady=(20, 10), padx=20)

#PDF file selection
pdf_label = customtkinter.CTkLabel(input_frame, text="PDF File:", anchor="w")
pdf_label.grid(row=0, column=0, padx=5, sticky="w")
pdf_entry = customtkinter.CTkEntry(input_frame, textvariable=pdf_path, width=300)
pdf_entry.grid(row=0, column=1, padx=5)
pdf_button = customtkinter.CTkButton(input_frame, text="Browse", command=select_pdf)
pdf_button.grid(row=0, column=2, padx=5)

#output folder selection
output_label = customtkinter.CTkLabel(input_frame, text="Output Folder:", anchor="w")
output_label.grid(row=1, column=0, padx=5, pady=(10, 0), sticky="w")
output_entry = customtkinter.CTkEntry(input_frame, textvariable=output_path, width=300)
output_entry.grid(row=1, column=1, padx=5, pady=(10, 0))
output_button = customtkinter.CTkButton(input_frame, text="Browse", command=select_output_folder)
output_button.grid(row=1, column=2, padx=5, pady=(10, 0))
page_count_label = customtkinter.CTkLabel(input_frame, text="Total Pages: ")
page_count_label.grid(row=2, column=0, columnspan=3, pady=(5, 0))

#DPI and Page range selection
dpi_label = customtkinter.CTkLabel(options_frame, text="DPI:")
dpi_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
dpi_entry = customtkinter.CTkEntry(options_frame, width=50)
dpi_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
dpi_entry.insert(0, "300")

from_page_label = customtkinter.CTkLabel(options_frame, text="From Page:")
from_page_label.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="w")
from_page_entry = customtkinter.CTkEntry(options_frame, width=50)
from_page_entry.grid(row=1, column=1, padx=5, pady=(5, 0))

to_page_label = customtkinter.CTkLabel(options_frame, text="To Page:")
to_page_label.grid(row=1, column=2, padx=5, pady=(5, 0), sticky="w")
to_page_entry = customtkinter.CTkEntry(options_frame, width=50)
to_page_entry.grid(row=1, column=3, padx=5, pady=(5, 0))

#button for full screen minimize and convert
fullscreen_button = customtkinter.CTkButton(convert_button_frame, text="Fullscreen", command=toggle_fullscreen)
fullscreen_button.pack(pady=5, padx=20, side=tk.LEFT)

minimize_button = customtkinter.CTkButton(convert_button_frame, text="Minimize", command=minimize_window)
minimize_button.pack(pady=5, padx=20, side=tk.LEFT)

convert_button = customtkinter.CTkButton(convert_button_frame, text="Convert to PNG", command=convert_pdf_to_png)
convert_button.pack(pady=10, padx=20, side="left")

root.mainloop()