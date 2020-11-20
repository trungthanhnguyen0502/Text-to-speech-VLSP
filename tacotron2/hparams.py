import os
from text import vn_symbols, en_symbols

"""Create model hyperparameters. Parse nondefault from given string."""
project_dir = os.getcwd()
# project_dir = '/'.join(project_dir.split('/')[:-1])

class hparams:
    is_cuda = False
    symbols=vn_symbols
    epochs=500
    iters_per_checkpoint=200
    seed=1234
    dynamic_loss_scaling=True
    fp16_run=False
    distributed_run=False
    dist_backend="nccl"
    dist_url="tcp://localhost:54321"
    cudnn_enabled=True
    cudnn_benchmark=False
    ignore_layers=['']
    load_mel_from_disk=False
    text_cleaners=['basic_cleaners']

    max_wav_value=1.0
    sampling_rate=22050
    filter_length=1024
    hop_length=256
    win_length=1024
    n_mel_channels=80
    mel_fmin=0.0
    mel_fmax=8000.0
    combine_ratio=0.8
    n_symbols=len(vn_symbols)
    symbols_embedding_dim=512

    # Encoder parameters
    encoder_kernel_size=5
    encoder_n_convolutions=3
    encoder_embedding_dim=512

    # Decoder parameters
    n_frames_per_step=1
    decoder_rnn_dim=1024
    prenet_dim=256
    max_decoder_steps=1000
    gate_threshold=0.5
    p_attention_dropout=0.1
    p_decoder_dropout=0.1

    # Attention parameters
    attention_rnn_dim=1024
    attention_dim=128

    # Location Layer parameters
    attention_location_n_filters=32
    attention_location_kernel_size=31

    # Mel-post processing network parameters
    postnet_embedding_dim=512
    postnet_kernel_size=5
    postnet_n_convolutions=5

    use_saved_learning_rate=False
    learning_rate=1e-4
    weight_decay=1e-6
    grad_clip_thresh=1.0
    batch_size=32
    mask_padding=True # set model's padded outputs to padded values
    tacotron_path="{}/pretrained/checkpoint_6600_0,638".format(project_dir)
    waveglow_path="{}/pretrained/waveglow_256channels.pt".format(project_dir)
    audio_outdir="static/audio".format(project_dir)
