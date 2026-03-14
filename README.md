# 📚 Research Article PDF Renamer

A Python application that automatically renames research article PDFs based on their titles. Extracts titles from PDF metadata or first page content and creates clean, readable filenames.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)

## ✨ Features

- 🎯 **Smart Title Extraction** - Reads PDF metadata and falls back to first-page text
- 🖥️ **User-Friendly GUI** - Simple interface for folder selection and file preview
- 👁️ **Preview Mode** - See changes before applying them
- 🛡️ **Safe Operations** - No accidental overwrites with automatic duplicate handling
- 📝 **Detailed Logging** - Track all operations in real-time
- 🔧 **Customizable Options** - Control filename length, space handling, and more
- ⚡ **Multi-threaded** - UI stays responsive during processing
- 🎓 **Research-Optimized** - Better title recognition for academic papers

## 📸 Screenshots

*[Add screenshots of your application here]*

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pdf-renamer.git
   cd pdf-renamer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python pdf_renamer.py
   ```

### Creating Standalone Executable

To create a standalone `.exe` file for Windows:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "PDFRenamer" pdf_renamer.py
```

The executable will be in the `dist` folder.

## 📖 Usage Guide

1. **Launch the application**
2. **Click "Browse"** to select your folder containing PDF files
3. **Click "Scan PDFs"** to analyze files and preview titles
4. **Review the preview** to ensure titles are correct
5. **Adjust options** if needed:
   - Enable/disable preview
   - Replace spaces with underscores
   - Set maximum filename length
6. **Click "Rename Files"** to apply changes

### Tips for Best Results

- **PDFs with metadata** work best (common in downloaded articles)
- **First-page titles** are extracted when metadata is missing
- **Maximum length** prevents extremely long filenames
- **Preview always** recommended before applying changes

## 🛠️ How It Works

1. **Scans folder** for all PDF files
2. **Extracts title** from each PDF:
   - First checks metadata (most reliable)
   - Falls back to first-page text analysis
   - Uses heuristics to identify actual titles
3. **Sanitizes filename** by removing invalid characters
4. **Prevents duplicates** by adding numbers if needed
5. **Renames files** with the new, clean titles

## 📦 Dependencies

- **PyPDF2** - PDF parsing and text extraction
- **tkinter** - GUI framework (built-in)
- **pathlib** - Path handling (built-in)
- **threading** - Background processing (built-in)

## 🔧 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| Preview | Show changes before applying | Enabled |
| Underscores | Replace spaces with underscores | Disabled |
| Max Length | Maximum filename length | 100 chars |

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/pdf-renamer.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [PyPDF2](https://github.com/py-pdf/PyPDF2) for PDF processing
- All contributors and users of this tool

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/pdf-renamer](https://github.com/yourusername/pdf-renamer)

## 🐛 Known Issues

- Some PDFs with complex formatting may not extract titles correctly
- Very long titles are truncated to prevent filename length issues
- OCR-based PDFs (scanned documents) may not have extractable text

## 🚀 Future Enhancements

- [ ] Support for drag-and-drop file addition
- [ ] Batch processing for multiple folders
- [ ] Custom title extraction rules
- [ ] Support for more PDF formats
- [ ] Integration with reference managers
```

## `LICENSE` (MIT License)

```txt
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Quick Setup Commands

```bash
# Initialize git repository
git init

# Create the files
touch .gitignore requirements.txt README.md LICENSE

# Add your python script
# Copy your pdf_renamer.py to the folder

# First commit
git add .
git commit -m "Initial commit: PDF Renamer application"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/pdf-renamer.git
git branch -M main
git push -u origin main
```

This setup provides a professional GitHub repository with all the essential files for documentation, dependencies, and licensing. Users can easily install and use your PDF renamer!
