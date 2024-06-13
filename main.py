import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

class PDFPageDeleter:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Page Deleter")
        
        # Setting the font
        self.font_large = ("Helvetica", 16)
        self.font_medium = ("Helvetica", 14)
        
        self.file_label = tk.Label(root, text="No file selected", font=self.font_medium)
        self.file_label.pack(pady=10)
        
        self.select_button = tk.Button(root, text="Select PDF", command=self.select_file, font=self.font_medium, bg='#4CAF50', fg='white', padx=10, pady=5)
        self.select_button.pack(pady=10)
        
        self.page_label = tk.Label(root, text="Pages to Delete (comma separated):", font=self.font_medium)
        self.page_label.pack(pady=5)
        
        self.page_entry = tk.Entry(root, font=self.font_medium)
        self.page_entry.pack(pady=5)
        
        self.delete_button = tk.Button(root, text="Delete Pages",width=20, command=self.delete_pages, font=self.font_medium, bg='#f44336', fg='white', padx=10, pady=5)
        self.delete_button.pack(pady=10)
        
        self.credit_label = tk.Label(root, text="Connect With Me", font=self.font_medium, fg='black')
        self.credit_label.pack(padx=5, pady=20)

        self.github_button = tk.Button(root, text="GitHub", width=20, command=lambda: webbrowser.open("https://github.com/jeturgavli"), font=self.font_medium, bg='#333333', fg='white', padx=10, pady=5)
        self.github_button.pack(padx=5, pady=5)
        
        self.linkedin_button = tk.Button(root, text="LinkedIn", width=20, command=lambda: webbrowser.open("https://www.linkedin.com/in/jeturgavli"), font=self.font_medium, bg='#0077B5', fg='white', padx=10, pady=5)
        self.linkedin_button.pack(padx=5, pady=5)
        
        self.instagram_button = tk.Button(root, text="Instagram", width=20, command=lambda: webbrowser.open("https://www.instagram.com/jetur_gavli_302"), font=self.font_medium, bg='#E4405F', fg='white', padx=10, pady=5)
        self.instagram_button.pack(padx=5, pady=5)

        self.credit_label = tk.Label(root, text="Program by Jetur Gavli", font=self.font_medium, fg='grey')
        self.credit_label.pack(pady=10)
        
        self.file_path = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file_path:
            self.file_label.config(text=self.file_path)
        else:
            self.file_label.config(text="No file selected")
    
    def delete_pages(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return
        
        try:
            pages_to_delete = list(map(int, self.page_entry.get().split(',')))
            # Convert to 0-indexed
            pages_to_delete = [p - 1 for p in pages_to_delete]  
            if any(p < 0 for p in pages_to_delete):
                raise ValueError("Page numbers must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid page numbers!")
            return
        
        try:
            reader = PdfReader(self.file_path)
            num_pages = len(reader.pages)
            
            if any(p >= num_pages for p in pages_to_delete):
                messagebox.showerror("Error", "One or more page numbers are out of range!")
                return
            
            writer = PdfWriter()
            for i in range(num_pages):
                if i not in pages_to_delete:
                    writer.add_page(reader.pages[i])
            
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if output_path:
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)
                
                messagebox.showinfo("Success", f"Pages {', '.join(map(str, [p + 1 for p in pages_to_delete]))} deleted successfully Dude!")
            else:
                messagebox.showwarning("Warning", "Save operation cancelled!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFPageDeleter(root)
    root.mainloop()
