
import sys
sys.path.append("tacotron2")
sys.path.append("tacotron2/waveglow")


import os
import librosa
import numpy as np
import re
import io
from layers import *
import torch

from hparams import hparams
from denoiser import Denoiser
from unicodedata import normalize
from model import Tacotron2
from text import text_to_sequence, normalize_text


def load_tacotron():
    global hparams
    hparams = hparams
    if hparams.is_cuda == True:
        device = "cuda"
    else:
        device = "cpu"
    # load tacotron model
    tacotron = Tacotron2(hparams)
    tacotron.load_state_dict(
        torch.load(hparams.tacotron_path, map_location=torch.device(device))[
            'state_dict']
    )

    if hparams.is_cuda:
        tacotron.cuda().eval().half()
    else:
        tacotron.eval()
    return hparams, tacotron


def load_waveglow(hparams):
    # load waveglow model
    if hparams.is_cuda == True:
        device = "cuda"
    else:
        device = "cpu"

    waveglow = torch.load(hparams.waveglow_path,
                          map_location=torch.device(device))['model']
    for m in waveglow.modules():
        if "Conv" in str(type(m)):
            setattr(m, "padding_mode", "zeros")

    if hparams.is_cuda:
        waveglow.cuda().eval().half()
    else:
        waveglow.eval()
    for k in waveglow.convinv:
        k.float()

    denoiser = Denoiser(waveglow, is_cuda=hparams.is_cuda)
    return waveglow, denoiser


def to_speech(text, tacotron, waveglow, denoiser, hparams):
    padding = np.zeros(int(0.5*hparams.sampling_rate),)
    concated_audio = []
    sequences = normalize_text(text).strip()
    sequences = sequences.split('.')
    print(sequences)
    for sequence in sequences:
        if not sequence:
            continue
        print(sequence)
        sequence = np.array(text_to_sequence(
            sequence, ["basic_cleaners"]))[None, :]

        sequence = torch.autograd.Variable(torch.from_numpy(sequence))
        if hparams.is_cuda:
            sequence = sequence.cuda().long()
        else:
            sequence = sequence.cpu().long()

        _, mel_post, _, _ = tacotron.inference(sequence)
        with torch.no_grad():
            audio = waveglow.infer(
                mel_post, is_cuda=hparams.is_cuda, sigma=0.666)
        audio_denoised = denoiser(audio, strength=0.01)[:, 0]
        audio_denoised = audio_denoised.cpu().numpy()
        # audio_denoised, index = librosa.effects.trim(audio_denoised, top_db=20)
        audio_denoised = np.squeeze(audio_denoised)

        concated_audio.append(audio_denoised)
        concated_audio.append(padding)
    concated_audio = np.hstack(concated_audio)
    concated_audio, index = librosa.effects.trim(concated_audio, top_db=20)
    return concated_audio
