import os
import ast
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pathlib
from pydantic import BaseModel
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

filepath = pathlib.Path('./output_pdf_chunks/rlhfbook_part_1.pdf')

with open("prompts/parse_toc.txt", "r") as f:
    prompt = f.read()

print(prompt)

class TableOfContents(BaseModel):
    sections: str

response = client.models.generate_content(
  model="gemini-2.5-pro-exp-03-25",
  contents=[
      types.Part.from_bytes(
        data=filepath.read_bytes(),
        mime_type='application/pdf',
      ),
      prompt],
  config={
        'response_mime_type': 'application/json',
        'response_schema': TableOfContents,
    }
  )

print(response.text)

json_dict = ast.literal_eval(response.text)
print(json_dict)

try:
    with open("toc.json", "w") as outfile:
        json.dump(json_dict, outfile, indent=4, sort_keys=False)
except SyntaxError as e:
    print(f"Error writing to file: {e}")
    print("Response text:", response.text)
