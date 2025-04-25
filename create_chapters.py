import json
import os
import PyPDF2
import ast
import glob
import re

def create_chapters():
    # Load the TOC data from JSON file
    with open('toc.json', 'r') as f:
        toc_data = json.load(f)

    # Parse the sections data (it's stored as a string in the JSON)
    sections = ast.literal_eval(toc_data['sections'])

    # Get a list of all PDF files in the current directory
    pdf_files = glob.glob('output_pdf_chunks/*.pdf')

    # Sort PDF files by the part number in their filename
    def get_part_number(filename):
        match = re.search(r'part_(\d+)\.pdf$', filename)
        return int(match.group(1)) if match else 0

    pdf_files.sort(key=get_part_number)

    print(f"Found {len(pdf_files)} PDF files")
    print(f"Sorted PDF files: {pdf_files}")

    # Create output directory if it doesn't exist
    output_dir = 'chapters'
    os.makedirs(output_dir, exist_ok=True)

    # Process each section
    for section_name, page_range in sections.items():
        start_page, end_page = page_range

        # Handle the "NA" case for end_page (e.g., Bibliography section)
        if end_page == "NA":
            # Calculate the total number of pages across all PDF files
            total_pages = 0
            for pdf_file in pdf_files:
                with open(pdf_file, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    total_pages += len(reader.pages)

            # Use the total page count as the end page
            end_page = total_pages
            print(f"Setting end page for {section_name} to total page count: {end_page}")

        # Convert page numbers to integers
        start_page = int(start_page)
        end_page = int(end_page)

        print(f"Processing section: {section_name} (pages {start_page}-{end_page})")

        # Create a new PDF writer for this section
        pdf_writer = PyPDF2.PdfWriter()

        # Get the pages from the appropriate PDF files
        current_page = 1
        for pdf_file in pdf_files:
            with open(pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)

                # Check if this PDF contains pages we need
                for page_num in range(num_pages):
                    if start_page <= current_page <= end_page:
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                    current_page += 1

                    if current_page > end_page:
                        break

            if current_page > end_page:
                break

        # Create a valid filename from the section name
        safe_section_name = section_name.replace('/', '-').replace(':', '-')
        output_filename = os.path.join(output_dir, f"{safe_section_name}.pdf")

        # Write the output file
        with open(output_filename, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

        print(f"Created: {output_filename}")

    for file_to_remove in glob.glob("output_pdf_chunks/*.pdf"):
        os.remove(file_to_remove)
    print("Removed all PDF files in output_pdf_chunks directory")

if __name__ == "__main__":
    create_chapters()
