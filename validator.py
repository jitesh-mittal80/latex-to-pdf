from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET


SUPPORTED_EXTENSIONS = {".txt", ".latex", ".tex", ".docx"}


def validate_input_file(input_path: Path):
    if not input_path.exists():
        print(f"Error: Input file does not exist:\n{input_path}")
        return False

    if not input_path.is_file():
        print(f"Error: The specified path is not a file:\n{input_path}")
        return False

    if input_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print(
            "Error: Unsupported file type.\n"
            "Supported extensions: .txt, .latex, .tex, .docx"
        )
        return False

    return True


def read_latex_source(input_path: Path):
    try:
        if input_path.suffix.lower() == ".docx":
            with zipfile.ZipFile(input_path, "r") as docx:
                document_xml = docx.read("word/document.xml")

            root = ET.fromstring(document_xml)

            namespace = {
                "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            }

            paragraphs = []

            for paragraph in root.findall(".//w:p", namespace):
                text = "".join(
                    node.text or ""
                    for node in paragraph.findall(".//w:t", namespace)
                )

                paragraphs.append(text)

            return "\n".join(paragraphs)

        return input_path.read_text(encoding="utf-8")

    except (OSError, zipfile.BadZipFile, ET.ParseError) as error:
        print("Error: Could not read the input file.")
        print(error)
        return None