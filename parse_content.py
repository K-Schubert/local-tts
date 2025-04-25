import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pathlib
from pydantic import BaseModel

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

with open("prompts/parse_pdf_to_text.txt", "r") as f:
    prompt = f.read()

class ParsedDocument(BaseModel):
    content: str
    summary: str

# Get all PDF files excluding Bibliography
pdf_files = [f for f in os.listdir("chapters") if f.endswith(".pdf") and f != "Bibliography.pdf"]

# Sort files by number at beginning of filename
def extract_number(filename):
    match = re.search(r'^(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

pdf_files.sort(key=extract_number)

bibliography = pathlib.Path('./chapters/Bibliography.pdf').read_bytes()

for fp in pdf_files[12:]:
    print(f"Processing: {fp}")
    chapter_path = os.path.join("chapters", fp)
    chapter = pathlib.Path(chapter_path).read_bytes()

    # Create output filename using the same name as the PDF but with .txt extension
    output_file = os.path.splitext(fp)[0] + ".txt"

    response = client.models.generate_content(
      model="gemini-2.5-pro-exp-03-25",
      contents=[
          types.Part.from_bytes(
            data=chapter,
            mime_type='application/pdf',
          ),
          types.Part.from_bytes(
            data=bibliography,
            mime_type='application/pdf',
          ),
          prompt],
      config={
            'response_mime_type': 'application/json',
            'response_schema': ParsedDocument,
        }
      )

    chapter_with_summary = response.parsed.summary + response.parsed.content

    try:
        os.makedirs("parsed_text", exist_ok=True)  # Ensure directory exists
        with open(f"parsed_text/{output_file}", "w") as f:
            f.write(chapter_with_summary.strip())
        print(f"Successfully wrote {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        print("Response text:", response.text)
