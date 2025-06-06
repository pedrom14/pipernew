
import argparse
import json
import numpy as np
import torch
import soundfile as sf
from TTS.tts.models.vits import Vits
from TTS.utils.audio import AudioProcessor
from TTS.utils.io import load_config
from TTS.utils.manage import ModelManager

def load_model(model_path, config_path):
    config = load_config(config_path)
    model = Vits.init_from_config(config)
    cp = torch.load(model_path, map_location=torch.device("cpu"))
    model.load_state_dict(cp["model"])
    model.eval()
    ap = AudioProcessor(**config.audio)
    return model, ap

def synthesize(model, ap, text):
    tokens = model.tokenizer.text_to_ids(text)
    tokens = torch.LongTensor(tokens).unsqueeze(0)
    with torch.no_grad():
        wav = model.inference(tokens)[0]
    wav = ap.inv_preemphasis(wav)
    wav = wav.cpu().numpy()
    return wav

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Path to the .onnx model")
    parser.add_argument("--config", required=True, help="Path to the config .json")
    parser.add_argument("--output_file", required=True, help="Output WAV file path")
    args = parser.parse_args()

    model, ap = load_model(args.model, args.config)
    print("Digite o texto e pressione Enter:")
    text = input().strip()
    wav = synthesize(model, ap, text)
    sf.write(args.output_file, wav, ap.sample_rate)

if __name__ == "__main__":
    main()
