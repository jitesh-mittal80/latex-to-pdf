import shutil
from pathlib import Path


def find_output_path(input_path: Path):
    counter = 1

    while True:
        output_path = (
            input_path.parent
            / f"{input_path.stem}({counter}).pdf"
        )

        if not output_path.exists():
            return output_path

        counter += 1


def move_pdf(pdf_path: Path, output_path: Path):
    try:
        shutil.move(str(pdf_path), str(output_path))
        return True

    except OSError as error:
        print("Error: Could not save the generated PDF.")
        print(error)
        return False