# Order to run PDF preprocessing scripts

1. python split_pdf.py input_pdf/rlhfbook.pdf 20 output_pdf_chunks
2. python get_toc.py
3. python create_chapters.py

# Parse PDF sections
1. python3 generate.py # generate first audio section
2. python3 stich_pdf.py # generate second audio section with voice cloning from previous section
