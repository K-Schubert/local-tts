# Use model to split PDF by chapter -> get PDF pages (start, end) for each chapter + bibliography
# Split PDF into chapter chunks -> save chunks as PDF
# Parse with formatting instructions -> save to .txt
# Run TTS
# Combine mp3 sections to final file
# Upload to spotify?

import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_by_pages(input_path: str, pages_per_chunk: int, output_dir: str):
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    filename_base = os.path.splitext(os.path.basename(input_path))[0]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(0, total_pages, pages_per_chunk):
        writer = PdfWriter()
        chunk_pages = reader.pages[i:i+pages_per_chunk]
        for page in chunk_pages:
            writer.add_page(page)

        output_path = os.path.join(output_dir, f"{filename_base}_part_{i // pages_per_chunk + 1}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

        # Check if the output file size exceeds 20MB
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        if file_size_mb > 20:
            print(f"WARNING: Chunk {filename_base}_part_{i // pages_per_chunk + 1}.pdf exceeds 20MB (size: {file_size_mb:.2f}MB)")

        print(f"Saved chunk: {output_path} ({file_size_mb:.2f}MB)")

def main():
    parser = argparse.ArgumentParser(description="Split a PDF into smaller chunks of X pages each.")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("pages_per_chunk", type=int, help="Number of pages per chunk")
    parser.add_argument("output_dir", help="Directory to save output PDF chunks")
    args = parser.parse_args()

    split_pdf_by_pages(args.input_pdf, args.pages_per_chunk, args.output_dir)

if __name__ == "__main__":
    main()