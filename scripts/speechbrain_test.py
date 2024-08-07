import torchaudio
from speechbrain.pretrained import EncoderClassifier

# Lade das vortrainierte Modell
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# Lade eine Audiodatei
signal, fs = torchaudio.load('tests/samples/ASR/spk1_snt1.wav')

# Erstelle Embeddings
embeddings = classifier.encode_batch(signal)

# Gib die Embeddings aus
print(embeddings)
