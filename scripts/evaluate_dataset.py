import torch
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2Processor
import soundfile as sf
import numpy as np
import os
import argparse
from scipy.io import wavfile

model_name = "microsoft/wavlm-base-plus-dns"
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)
processor = Wav2Vec2Processor.from_pretrained(model_name)

# Function to evaluate the quality of a single file
def evaluate_audio_quality(file_path):
    audio_input, sample_rate = sf.read(file_path) # Get input array and sample rate from the audio file
    if len(audio_input.shape) > 1: # If Stereo (2-dimensional array)
        audio_input = np.mean(audio_input, axis = 1) # Convert to Mono by taking the mean of each value
    # Pre-process the file using the Wav2Vec2Processor, generating a tensor
    inputs = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt")

    # Evaluate quality
    with torch.no_grad(): # Deactivate gradient computation to save space and time
        outputs = model(**inputs) # Apply the model to the tensor
    quality_score = outputs.logits.squeeze().item() # Retrieve the quality score from the output

    return quality_score

# Run the above method for each .wav file in the dataset
def process_dataset(dataset_path, output_file):
    results = []
    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file) # Get the file path
                score = ecaluate_audio_quality(file_path) # Evaluate the file's quality
                results.append((file_path, score)) # Save the quality score in results
                print(f"Processed {file_path}: Quality Score = {score}")

    # Save results
    with open(output_file, 'w') as f:
        for file_path, score in results:
            f.write(f"{file_path}, {score}\n") # Write the score of each sample in the output file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "")

    dataset_path = "C:/Dev/Example Files" # TODO: Add path to dataset here
    output_file = "audio_quality_scores.csv"
    process_dataset(dataset_path, output_file)
