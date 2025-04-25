
from kokoro import KPipeline
import soundfile as sf

# 'a' => American English
# 'b' => British English
# 'e' => Spanish es
# 'f' => French fr-fr
# 'h' => Hindi hi
# 'i' => Italian it
# 'j' => Japanese: pip install misaki[ja]
# 'p' => Brazilian Portuguese pt-br
# 'z' => Mandarin Chinese: pip install misaki[zh]

pipeline = KPipeline(lang_code='b', device='mps') # <= make sure lang_code matches voice, reference above.

with open('parsed_text/8 Regularization.txt', 'r') as f:
    text = f.read().strip()

# Generate, display, and save audio files in a loop.
generator = pipeline(
    text, voice='af_heart', # <= change voice here
    speed=1, split_pattern=r'\n+'
)

# Alternatively, load voice tensor directly:
# voice_tensor = torch.load('path/to/voice.pt', weights_only=True)
# generator = pipeline(
#     text, voice=voice_tensor,
#     speed=1, split_pattern=r'\n+'
# )

for i, (gs, ps, audio) in enumerate(generator):
    print(i)  # i => index
    print(gs) # gs => graphemes/text
    print(ps) # ps => phonemes
    #display(Audio(data=audio, rate=24000, autoplay=i==0))
    sf.write(f'output_audio/{i}.wav', audio, 24000) # save each audio file
