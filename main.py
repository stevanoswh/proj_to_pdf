import os
import sys
import argparse
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black, grey

def convert_project_to_pdf(project_path, output_pdf):
    # Get all files in the project directory
    file_paths = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    # Create the PDF document
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom style for code
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=black,
        backColor=grey,
    )

    # Add each file's content to the PDF
    for file_path in file_paths:
        # Add file name as a header
        story.append(Paragraph(file_path, styles['Heading2']))
        story.append(Spacer(1, 12))

        # Read and add file content
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                story.append(Paragraph(content, code_style))
        except Exception as e:
            story.append(Paragraph(f"Error reading file: {str(e)}", styles['Normal']))

        story.append(Spacer(1, 24))

    # Build the PDF
    doc.build(story)

def main():
    parser = argparse.ArgumentParser(description="Convert a project directory to PDF")
    parser.add_argument("project_path", help="Path to the project directory")
    args = parser.parse_args()

    # Use the provided project path
    project_path = args.project_path

    # Set output path to home directory
    home_dir = str(Path.home())
    output_pdf = os.path.join(home_dir, 'project_contents.pdf')

    convert_project_to_pdf(project_path, output_pdf)
    print(f"PDF has been generated and saved to: {output_pdf}")

if __name__ == "__main__":
    main()
