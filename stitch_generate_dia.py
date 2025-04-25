from dia.model import Dia

model = Dia.from_pretrained("nari-labs/Dia-1.6B", device="mps")

# Clone from text and audio
with open("./sample.txt", "r") as f:
    clone_from_text = f.read()

clone_from_text = "[S1] " + clone_from_text
clone_from_audio = "sample.mp3"

# Text to generate
text_to_generate = "[S1] Open Questions Fundamental problems and discussions for the long-term evolution of how RLHF is used. 17. Over-optimization: Qualitative observations of why RLHF goes wrong and why over-optimization is inevitable with a soft optimization target in reward models."

# It will only return the audio from the text_to_generate
output = model.generate(
    clone_from_text + text_to_generate, audio_prompt=clone_from_audio, use_torch_compile=False, verbose=True
)

model.save_audio("voice_clone.mp3", output)