from dia.model import Dia

model = Dia.from_pretrained("nari-labs/Dia-1.6B", device="mps")

with open("parsed_text/chapter_1.txt", "r") as f:
	text = f.read()

text = "[S1] " + text
output = model.generate(text, use_torch_compile=False, verbose=True, max_tokens=2048)

model.save_audio("output_audio/chapter_1.mp3", output)