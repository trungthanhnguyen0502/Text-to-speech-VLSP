import numpy as np
from scipy.io.wavfile import read
import torch
import librosa
import os

def get_mask_from_lengths(lengths):
    max_len = torch.max(lengths).item()
    ids = torch.arange(0, max_len, out=torch.cuda.LongTensor(max_len))
    mask = (ids < lengths.unsqueeze(1)).byte()
    return mask


def load_wav_to_torch(full_path):
    data, sampling_rate = librosa.core.load(full_path)
    return torch.FloatTensor(data.astype(np.float32)), sampling_rate


def load_filepaths_and_text(filename, split="|"):
    filepaths_and_text = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            try:
                file_path, text = line.strip().split(split)

                if os.path.isfile(file_path):
                    filepaths_and_text.append([file_path, text])
            except:
                print(line)
    return filepaths_and_text


def to_gpu(x):
    x = x.contiguous()

    if torch.cuda.is_available():
        x = x.cuda(non_blocking=True)
    return torch.autograd.Variable(x)
