import subprocess
from pathlib import Path


def create_temporary_tex(
    temp_dir: Path,
    input_path: Path,
    latex_source: str
):
    tex_filename = input_path.stem + ".tex"
    tex_path = temp_dir / tex_filename

    try:
        tex_path.write_text(latex_source, encoding="utf-8")
        return tex_path
    except OSError as error:
        print("Error: Could not create the temporary LaTeX file.")
        print(error)
        return None


def extract_latex_error(output: str):
    lines = output.splitlines()

    for index, line in enumerate(lines):
        if line.startswith("!"):
            error_lines = [line]

            # Include the source line information, e.g.:
            # l.12 \wrongcommand
            for next_line in lines[index + 1:index + 4]:
                stripped = next_line.strip()

                if stripped.startswith("l."):
                    error_lines.append(stripped)
                    break

            return "\n".join(error_lines)

    return "Unknown LaTeX compilation error."


def compile_latex(tex_path: Path):
    try:
        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                tex_path.name,
            ],
            cwd=tex_path.parent,
            capture_output=True,
            text=True,
        )

    except FileNotFoundError:
        print(
            "Error: pdflatex could not be found.\n"
            "Make sure a LaTeX distribution is installed "
            "and pdflatex is available in PATH."
        )
        return False

    if result.returncode != 0:
        latex_error = extract_latex_error(result.stdout)

        print("LaTeX syntax error:")
        print(latex_error)

        return False

    return True


def get_generated_pdf(tex_path: Path):
    pdf_path = tex_path.with_suffix(".pdf")

    if not pdf_path.exists():
        print("Error: No PDF was generated.")
        return None

    return pdf_path