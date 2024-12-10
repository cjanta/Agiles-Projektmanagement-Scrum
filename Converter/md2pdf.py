#pip install markdown-pdf
from markdown_pdf import Section, MarkdownPdf

path_filename = "Dokumentation_0_0_1.md"

# Read content from the Markdown file
with open(path_filename, "r", encoding="utf-8") as file:
    markdown_content = file.read()

pdf = MarkdownPdf()

# Add the entire content as a single section
pdf.add_section(Section(markdown_content))

# Save the PDF
pdf.save("Dokumentation.pdf")

print("PDF has been created: Dokumentation.pdf")
