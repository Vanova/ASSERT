TOKEN = '998051465:AAG39shJV-XheO4BMdnRMBMMYv0a7cI-_CE'
BOT_NAME = 'AntiSpoof'

feat_params = {
    'type': 'stft',
    'win_length_seconds': 0.025,
    'hop_length_seconds': 0.01,
    'fmin': 20,  # Minimum frequency when constructing MEL bands
    'fmax': 7800,  # for 16KHz, Maximum frequency when constructing MEL band
    'include_delta': False,
    'include_acceleration': False,
    'delta': {'width': 15},
    'acceleration': {'width': 15},
    'n_fft': 512,
    'mono': True,
    'window': 'hamming_asymmetric'  # [hann_asymmetric, hamming_asymmetric]
}

model_params = {
    'MODEL_SELECT': 6,  # which model
    'NUM_SPOOF_CLASS': 2,  # LA: 7 or PA: 10 x-class classification
    'FOCAL_GAMMA': None,  # gamma parameter for focal loss; if obj is not focal loss, set this to None
    'NUM_RESNET_BLOCK': 5,  # number of resnet blocks in ResNet
    'AFN_UPSAMPLE': 'Bilinear',  # upsampling method in AFNet: Conv or Bilinear
    'AFN_ACTIVATION': 'sigmoid',  # activation function in AFNet: sigmoid, softmaxF, softmaxT
    'NUM_HEADS': 3,  # number of heads for multi-head att in SAFNet
    'SAFN_HIDDEN': 10,  # hidden dim for SAFNet
    'SAFN_DIM': 'T',  # SAFNet attention dim: T or F
    'RNN_HIDDEN': 128,  # hidden dim for RNN
    'RNN_LAYERS': 4,  # number of hidden layers for RNN
    'RNN_BI': True,  # bidirecitonal/unidirectional for RNN
    'DROPOUT_R': 0.0,  # dropout rate
}
data_files = {  # training
    'train_scp': '/home/vano/wrkdir/projects_data/antispoofing_speech/logspec/raw_fbank_ASVspoof2019_PA_train_spec.1.scp',
    'train_utt2index': 'data_reader/utt2systemID/pa_train_utt2index_8',
    'dev_scp': '/home/vano/wrkdir/projects_data/antispoofing_speech/logspec/raw_fbank_ASVspoof2019_PA_dev_spec.1.scp',
    'dev_utt2index': 'data_reader/utt2systemID/pa_dev_utt2index_8',
    'dev_utt2systemID': 'data_reader/utt2systemID/pa_dev_utt2systemID',
    'eval_utt2systemID': 'data_reader/utt2systemID/pa_eval_utt2systemID',
    'scoring_dir': 'scoring/pa_cm_scores/',
}


batch_size = 3  # 64
test_batch_size = 1  # 64 TODO fix pytorch collate function!!!
model_file = '../pretrained/pa/senet34'
