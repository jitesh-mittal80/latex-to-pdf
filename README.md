# LaTeX to PDF Converter

> **A lightweight command-line utility for converting files containing
> LaTeX source code into PDF.**

The **LaTeX to PDF Converter** is a small local Windows utility built
with Python. It accepts LaTeX source stored in `.txt`, `.latex`, `.tex`,
or `.docx` files, extracts the source when necessary, and uses
`pdflatex` to generate the final PDF.

The project is deliberately kept minimal: no GUI, database, cloud
service, API, or complicated configuration is required.

------------------------------------------------------------------------

## ✨ Features

-   📄 **Multiple input formats** --- `.txt`, `.latex`, `.tex`, and
    `.docx`
-   🧩 **DOCX text extraction** --- LaTeX source can be stored inside a
    Word document
-   ⚙️ **Real LaTeX compilation** --- uses `pdflatex`
-   📁 **Same-directory output** --- the PDF is saved beside the input
    file
-   🔢 **Automatic numbering** --- finds the first available output
    number
-   🧹 **Temporary-file isolation** --- compilation files stay inside a
    temporary directory
-   🛡️ **Original-file protection** --- input files are never modified
-   🪟 **Windows-friendly CLI** --- supports normal and full file paths,
    including paths with spaces
-   🐍 **Standard-library Python** --- no third-party Python package is
    required

------------------------------------------------------------------------

## 📌 Supported Input

   Extension  Handling
  ----------- -----------------------------------------
    `.txt`    Read directly as LaTeX source
   `.latex`   Read directly as LaTeX source
    `.tex`    Read directly as LaTeX source
    `.docx`   Extract text and use it as LaTeX source

### DOCX files

A `.docx` file is supported as **a container for LaTeX source**, not as
a Word-to-LaTeX converter.

For example, a Word document may contain:

``` latex
\documentclass{article}

\begin{document}

\section{Introduction}

Hello World!

\end{document}
```

The converter extracts the document's text and passes that text through
the same LaTeX compilation pipeline.

> **Note:** Word formatting, Word-specific equations, styles, and other
> document features are not converted into LaTeX.

------------------------------------------------------------------------

## 🔄 Conversion Pipeline

The converter follows the same basic pipeline for every supported
format:

``` text
             Input File
                 │
                 ▼
          Validate Input
                 │
                 ▼
      Read / Extract LaTeX Source
                 │
                 ▼
       Create Temporary .tex
                 │
                 ▼
             pdflatex
                 │
                 ▼
          Generated PDF
                 │
                 ▼
      Select Output Filename
                 │
                 ▼
          Final PDF File
```

The `.docx` format only changes the **source-reading step**. After the
LaTeX source has been extracted, the rest of the architecture remains
the same.

------------------------------------------------------------------------

## 🗂️ Project Structure

``` text
latex-to-pdf/
│
├── main.py              # Application entry point
├── compiler.py          # LaTeX compilation
├── output.py            # Output naming and PDF handling
├── validator.py         # Validation and source extraction
├── latex2pdf.bat        # Windows command launcher
└── README.md            # Project documentation
```

### Module responsibilities

**`main.py`**\
Coordinates the complete conversion workflow.

**`validator.py`**\
Validates the input file and reads or extracts its LaTeX source.

**`compiler.py`**\
Creates the temporary `.tex` file and invokes `pdflatex`.

**`output.py`**\
Determines the first available output filename and moves the generated
PDF.

**`latex2pdf.bat`**\
Provides a convenient Windows command so the converter can be launched
from a terminal.

------------------------------------------------------------------------

## 🛠️ Requirements

### Python

Python 3 is required.

The project uses Python's standard library for its own functionality,
including DOCX text extraction.

### LaTeX

A LaTeX distribution providing `pdflatex` must be installed and
available in `PATH`.

For example, with MiKTeX:

``` powershell
pdflatex --version
```

If the command returns the installed version, the converter can use
`pdflatex`.

------------------------------------------------------------------------

## 🚀 Usage

### Run directly with Python

From the project directory:

``` powershell
python main.py paper.txt
```

The same command works with the other supported formats:

``` powershell
python main.py paper.tex
python main.py paper.latex
python main.py paper.docx
```

### Using the Windows command

The project includes:

``` text
latex2pdf.bat
```

After adding the project directory to your user's `PATH`, the converter
can be launched from any terminal:

``` powershell
latex2pdf paper.txt
```

A full path can also be supplied:

``` powershell
latex2pdf "C:\Users\Example\Documents\paper.docx"
```

Paths containing spaces are supported.

------------------------------------------------------------------------

## 📤 Output Naming

The generated PDF is always saved in the **same directory as the input
file**.

For example:

``` text
Documents/
├── paper.tex
├── paper(1).pdf
├── paper(2).pdf
└── paper(5).pdf
```

Running the converter again produces:

``` text
paper(3).pdf
```

The converter searches from `1` upward and selects the **first available
number** rather than simply using the largest existing number plus one.

------------------------------------------------------------------------

## 🧹 Temporary Compilation Files

LaTeX compilation generates auxiliary files such as:

``` text
.aux
.log
.pdf
```

These files are created inside a temporary directory rather than beside
the original input.

Conceptually:

``` text
Input Directory
│
├── paper.tex
├── paper(1).pdf
└── ...

Temporary Directory
│
├── paper.tex
├── paper.aux
├── paper.log
└── paper.pdf
```

Once processing is complete, the temporary directory is automatically
removed.

This keeps the user's working directory clean.

------------------------------------------------------------------------

## 🔒 File Safety

The converter does **not** modify the original input file.

Instead:

``` text
Original File
      │
      ├── Read / Extract
      │
      ▼
Temporary .tex
      │
      ▼
   pdflatex
      │
      ▼
Temporary PDF
      │
      ▼
Final PDF
```

The original `.txt`, `.latex`, `.tex`, or `.docx` remains unchanged.

------------------------------------------------------------------------

## ⚠️ Error Handling

The converter handles common failure cases, including:

-   Input file does not exist
-   Input path is not a file
-   Unsupported file extension
-   Input file cannot be read
-   Invalid or corrupted `.docx` file
-   `pdflatex` is not available
-   LaTeX compilation failure
-   PDF not generated after compilation
-   Generated PDF cannot be moved to its destination

Errors are reported directly in the terminal.

------------------------------------------------------------------------

## 🧱 Design Philosophy

This project is intentionally small and focused.

### Included

-   Python CLI
-   `pathlib` for file paths
-   `subprocess` for `pdflatex`
-   Temporary directories for compilation
-   Standard-library DOCX text extraction

### Not included

-   ❌ GUI
-   ❌ Web interface
-   ❌ Database
-   ❌ Cloud services
-   ❌ API
-   ❌ User accounts
-   ❌ Configuration system
-   ❌ Custom LaTeX parser
-   ❌ Custom PDF generation engine
-   ❌ Third-party Python dependencies

The core idea is straightforward:

> **Provide a file containing LaTeX source → receive a PDF.**

------------------------------------------------------------------------

## 🔮 Possible Future Improvements

The current implementation intentionally stays minimal. If the project
grows, possible additions could include:

-   More precise LaTeX error extraction
-   Additional input formats
-   Optional command-line flags
-   Improved terminal output
-   Optional preservation of compilation logs
-   More advanced source extraction for document formats

These are deliberately outside the scope of the current implementation.

------------------------------------------------------------------------

## 📄 License

This project is intended as a small personal utility.
