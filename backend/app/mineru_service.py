import subprocess
import os


def run_mineru_extraction(pdf_path: str) -> str:
    """
    Runs MinerU on the given PDF file using the CPU pipeline backend,
    and returns the extracted Markdown content as a string.
    """
    filename_without_ext = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = "mineru_output"

    result = subprocess.run(
        ["mineru", "-p", pdf_path, "-o", output_dir, "-b", "pipeline"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"MinerU failed: {result.stderr}")

    md_file_path = os.path.join(output_dir, filename_without_ext, "auto", f"{filename_without_ext}.md")

    if not os.path.exists(md_file_path):
        raise FileNotFoundError(f"Expected MinerU output not found at {md_file_path}")

    with open(md_file_path, "r", encoding="utf-8") as file:
        extracted_text = file.read()

    return extracted_text