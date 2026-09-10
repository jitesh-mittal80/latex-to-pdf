import sys
import tempfile
from pathlib import Path

from compiler import (
    compile_latex,
    create_temporary_tex,
    get_generated_pdf,
)

from output import (
    find_output_path,
    move_pdf,
)

from validator import (
    read_latex_source,
    validate_input_file,
)


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        return

    input_path = Path(sys.argv[1])

    if not validate_input_file(input_path):
        return

    latex_source = read_latex_source(input_path)

    if latex_source is None:
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        tex_path = create_temporary_tex(
            temp_path,
            input_path,
            latex_source,
        )

        if tex_path is None:
            return

        if not compile_latex(tex_path):
            return

        pdf_path = get_generated_pdf(tex_path)

        if pdf_path is None:
            return

        output_path = find_output_path(input_path)

        if not move_pdf(pdf_path, output_path):
            return

        print(f"PDF created successfully:\n{output_path}")


if __name__ == "__main__":
    main()