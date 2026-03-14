import os
import re
import sys
import PyPDF2
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import threading


class PDFRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Research Article PDF Renamer")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Set icon (optional - you can add an icon file later)
        # self.root.iconbitmap('icon.ico')

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Folder selection
        ttk.Label(main_frame, text="Folder Path:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.folder_path_var = tk.StringVar()
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_path_var, width=50)
        folder_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_folder)
        browse_btn.grid(row=0, column=2, pady=5, padx=5)

        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)

        # Preview option
        self.preview_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preview changes before renaming",
                        variable=self.preview_var).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        # Replace spaces with underscores
        self.underscore_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Replace spaces with underscores",
                        variable=self.underscore_var).grid(row=1, column=0, columnspan=2, sticky=tk.W)

        # Max filename length
        ttk.Label(options_frame, text="Max filename length:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.max_length_var = tk.StringVar(value="100")
        ttk.Spinbox(options_frame, from_=30, to=255, textvariable=self.max_length_var,
                    width=10).grid(row=2, column=1, sticky=tk.W, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.scan_btn = ttk.Button(button_frame, text="Scan PDFs", command=self.scan_pdfs)
        self.scan_btn.pack(side=tk.LEFT, padx=5)

        self.rename_btn = ttk.Button(button_frame, text="Rename Files", command=self.rename_files,
                                     state=tk.DISABLED)
        self.rename_btn.pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Log area
        ttk.Label(main_frame, text="Progress Log:").grid(row=4, column=0, sticky=tk.W, pady=5)

        self.log_area = scrolledtext.ScrolledText(main_frame, width=80, height=20, wrap=tk.WORD)
        self.log_area.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Configure text tags for colors
        self.log_area.tag_config('error', foreground='red')
        self.log_area.tag_config('success', foreground='green')
        self.log_area.tag_config('info', foreground='blue')

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Store scanned files info
        self.pdf_files_info = []

    def log(self, message, tag=None):
        """Add message to log area"""
        self.log_area.insert(tk.END, message + "\n", tag)
        self.log_area.see(tk.END)
        self.root.update()

    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path_var.set(folder)

    def sanitize_filename(self, filename):
        """Remove or replace invalid characters from filename"""
        # Replace invalid characters with underscore
        invalid_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(invalid_chars, '_', filename)

        # Replace spaces if option selected
        if self.underscore_var.get():
            sanitized = sanitized.replace(' ', '_')

        # Remove any trailing periods or spaces
        sanitized = sanitized.strip('. ')

        # Replace multiple underscores with single underscore
        sanitized = re.sub(r'_+', '_', sanitized)

        # Limit length
        max_length = int(self.max_length_var.get())
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length].rsplit(' ', 1)[0] if ' ' in sanitized[:max_length] else sanitized[
                :max_length]

        return sanitized if sanitized else "untitled"

    def extract_title_from_pdf(self, pdf_path):
        """Extract title from PDF metadata or first page"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Try metadata first
                if pdf_reader.metadata and pdf_reader.metadata.title:
                    title = pdf_reader.metadata.title.strip()
                    if title and not all(c in '0123456789- ' for c in title):  # Avoid pure numbers/dashes
                        return title

                # Try first page text
                if len(pdf_reader.pages) > 0:
                    first_page = pdf_reader.pages[0]
                    text = first_page.extract_text()
                    if text:
                        # Common patterns for research article titles
                        lines = text.split('\n')
                        for line in lines[:5]:  # Check first 5 lines
                            line = line.strip()
                            # Heuristic: title usually has 5-20 words and not all caps
                            if line and 5 < len(line.split()) < 25 and not line.isupper():
                                # Avoid common headers
                                if not any(word in line.lower() for word in
                                           ['abstract', 'introduction', 'page', 'journal']):
                                    return line

                        # Fallback: first non-empty line
                        for line in lines:
                            if line.strip():
                                return line.strip()

                return None

        except Exception as e:
            self.log(f"Error reading {pdf_path.name}: {str(e)}", 'error')
            return None

    def scan_pdfs(self):
        """Scan folder for PDFs and extract titles"""
        folder_path = self.folder_path_var.get().strip()

        if not folder_path:
            messagebox.showerror("Error", "Please select a folder first!")
            return

        folder = Path(folder_path)
        if not folder.exists():
            messagebox.showerror("Error", f"Folder '{folder_path}' does not exist!")
            return

        # Clear previous data
        self.pdf_files_info = []
        self.log_area.delete(1.0, tk.END)
        self.rename_btn.config(state=tk.DISABLED)

        # Start scanning in separate thread
        self.scan_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_var.set("Scanning PDFs...")

        def scan():
            try:
                pdf_files = list(folder.glob("*.pdf")) + list(folder.glob("*.PDF"))

                if not pdf_files:
                    self.log("No PDF files found in the specified folder.", 'error')
                else:
                    self.log(f"Found {len(pdf_files)} PDF file(s)")
                    self.log("-" * 60)

                    for pdf_path in pdf_files:
                        self.status_var.set(f"Processing: {pdf_path.name}")
                        title = self.extract_title_from_pdf(pdf_path)

                        if title:
                            new_name = self.sanitize_filename(title) + '.pdf'
                            self.pdf_files_info.append({
                                'old_path': pdf_path,
                                'old_name': pdf_path.name,
                                'new_name': new_name,
                                'title': title
                            })
                            self.log(f"📄 {pdf_path.name[:50]}...", 'info')
                            self.log(f"   → {new_name[:50]}...", 'success')
                        else:
                            self.pdf_files_info.append({
                                'old_path': pdf_path,
                                'old_name': pdf_path.name,
                                'new_name': None,
                                'title': None
                            })
                            self.log(f"⚠️ Could not extract title from: {pdf_path.name}", 'error')

                        self.log("")

                    self.log("-" * 60)
                    self.log(
                        f"Scan complete. Found titles for {sum(1 for f in self.pdf_files_info if f['title'])} out of {len(self.pdf_files_info)} files.")

                    if any(f['title'] for f in self.pdf_files_info):
                        self.rename_btn.config(state=tk.NORMAL)

            except Exception as e:
                self.log(f"Error during scan: {str(e)}", 'error')
            finally:
                self.progress.stop()
                self.scan_btn.config(state=tk.NORMAL)
                self.status_var.set("Scan complete")

        threading.Thread(target=scan, daemon=True).start()

    def rename_files(self):
        """Rename files based on scanned information"""
        if not self.pdf_files_info:
            return

        # Count files to rename
        files_to_rename = [f for f in self.pdf_files_info if f['title']]

        if not files_to_rename:
            messagebox.showinfo("Info", "No files to rename!")
            return

        # Preview if enabled
        if self.preview_var.get():
            preview_text = "The following files will be renamed:\n\n"
            for f in files_to_rename:
                preview_text += f"Old: {f['old_name']}\n"
                preview_text += f"New: {f['new_name']}\n\n"

            if not messagebox.askyesno("Confirm Rename", preview_text + "\nProceed with rename?"):
                return

        # Start renaming
        self.rename_btn.config(state=tk.DISABLED)
        self.scan_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_var.set("Renaming files...")

        def rename():
            renamed = 0
            errors = 0

            try:
                for file_info in self.pdf_files_info:
                    if not file_info['title']:
                        continue

                    old_path = file_info['old_path']
                    new_name = file_info['new_name']
                    new_path = old_path.parent / new_name

                    # Handle duplicate names
                    counter = 1
                    original_new_path = new_path
                    while new_path.exists() and new_path != old_path:
                        name_without_ext = new_name[:-4]
                        new_name = f"{name_without_ext}_{counter}.pdf"
                        new_path = old_path.parent / new_name
                        counter += 1

                    try:
                        old_path.rename(new_path)
                        self.log(f"✅ Renamed: {old_path.name} -> {new_name}", 'success')
                        renamed += 1
                    except Exception as e:
                        self.log(f"❌ Error renaming {old_path.name}: {str(e)}", 'error')
                        errors += 1

                    self.status_var.set(f"Renamed {renamed} files...")

                self.log("-" * 60)
                self.log(f"Complete: {renamed} file(s) renamed, {errors} error(s)", 'info')

            except Exception as e:
                self.log(f"Error during rename: {str(e)}", 'error')
            finally:
                self.progress.stop()
                self.scan_btn.config(state=tk.NORMAL)
                self.status_var.set("Rename complete")
                messagebox.showinfo("Complete", f"Renamed {renamed} files successfully!")

        threading.Thread(target=rename, daemon=True).start()


def main():
    root = tk.Tk()
    app = PDFRenamerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()