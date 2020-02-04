import os
import subprocess
import torch
from collections import defaultdict
import numpy as np
import config as cfg
import assert_src.features.audio as F
from assert_src.model import E2E
from assert_src.data_reader.dataset_v1 import SpoofDatsetFilebase
import assert_src.src.eval_metrics as metr


use_cuda = torch.cuda.is_available()  # use cpu
device = torch.device("cuda" if use_cuda else "cpu")
kwargs = {'num_workers': 2, 'pin_memory': True} if use_cuda else {}

# create model
model = E2E(**cfg.model_params).to(device)
num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print('===> Model total parameter: {}'.format(num_params))

if os.path.isfile(cfg.model_file):
    print("===> loading checkpoint '{}'".format(cfg.model_file))
    checkpoint = torch.load(cfg.model_file, map_location=lambda storage, loc: storage)  # load for cpu
    model.load_state_dict(checkpoint['state_dict'], strict=False)
    print("===> loaded checkpoint '{}' (epoch {})"
          .format(cfg.model_file, checkpoint['epoch']))
else:
    print("===> no checkpoint found at '{}'".format(cfg.model_file))
    exit()


def detect_spoofing(file_name):
    # transform to wav
    fid = os.path.splitext(file_name)[0]
    wav_name = '{}.wav'.format(fid)
    subprocess.call(['/home/vano/ffmpeg-4.2.1-amd64-static/ffmpeg', '-i', file_name, '-ar', '16000', '-ac', '1', wav_name])
    #subprocess.call(['sox',  file_name, '-r', '16000', wav_name])
    print('[INFO] Transformed to wav: %s' % wav_name)

    # extract features
    feat_type = cfg.feat_params['type']
    extractor = F.prepare_extractor(feats=feat_type, params=cfg.feat_params)
    x, fs = F.load_sound_file(wav_name)
    assert (fs == 16000)
    feat = extractor.extract(x, fs)
    feat_file = '{}.npy'.format(fid)
    np.save(feat_file, np.squeeze(feat))
    print('[INFO] Features are extracted: %s' % feat_file)
    # forward network
    res = _forward_pass(feat_file, cfg.model_params)
    scores = res[feat_file]
    return 'bonafide: %.4f\nspoof: %.4f' % (scores[0], scores[1])


def _forward_pass(feat_file, model_params):
    """ forward pass dev and eval data to trained model  """
    # TODO load model
    # use_cuda = torch.cuda.is_available()  # use cpu
    # device = torch.device("cuda" if use_cuda else "cpu")
    # kwargs = {'num_workers': 2, 'pin_memory': True} if use_cuda else {}
    #
    # # create model
    # model = E2E(**model_params).to(device)
    # num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    # print('===> Model total parameter: {}'.format(num_params))
    #
    # if os.path.isfile(cfg.model_file):
    #     print("===> loading checkpoint '{}'".format(cfg.model_file))
    #     checkpoint = torch.load(cfg.model_file, map_location=lambda storage, loc: storage)  # load for cpu
    #     model.load_state_dict(checkpoint['state_dict'], strict=False)
    #     print("===> loaded checkpoint '{}' (epoch {})"
    #           .format(cfg.model_file, checkpoint['epoch']))
    # else:
    #     print("===> no checkpoint found at '{}'".format(cfg.model_file))
    #     exit()
    ###########################################
    # Data loading
    val_data = SpoofDatsetFilebase([feat_file])
    val_loader = torch.utils.data.DataLoader(val_data,
                                             batch_size=cfg.test_batch_size,
                                             shuffle=False, **kwargs)
    # forward pass
    return _prediction(val_loader, model, device)


def _prediction(val_loader, model, device):
    # switch to evaluate mode
    utt2scores = defaultdict(list)
    model.eval()

    with torch.no_grad():
        for i, (utt_id, input) in enumerate(val_loader):
            input = input[0].to(device)
            # compute output
            output = model(input)
            print(output)
            # score = output[:, 0]  # use log-probability of the bonafide class for scoring

            # for index, utt_id in enumerate(utt_id):
            #     utt2scores[utt_id[0]].append(output[index].numpy())
            utt2scores[utt_id[0]] = np.mean(output.cpu().numpy(), axis=0)

        # for index, utt_id in enumerate(val_loader.file_list):
        # score_list = utt2scores[utt_id]
        # avg_score = np.mean(score_list)
        # utt2scores[utt_id] = avg_score

        return utt2scores

if __name__ == '__main__':

    file_names = ['bonafide2020_01_06_13_04_54.wav', 'spoof2020_01_06_13_24_13.wav',
 'bonafide2020_01_06_13_08_37.wav', 'spoof2020_01_06_13_26_08.wav',
 'bonafide2020_01_06_13_10_59.wav',   'spoof2020_01_06_13_27_24.wav',
 'bonafide2020_01_06_13_17_31.wav',   'spoof2020_01_06_13_28_45.wav',
 'bonafide2020_01_06_13_22_11.wav',   'spoof2020_01_06_13_30_18.wav']
    fdir = 'test_audio'
    y_pred = []
    y_true = []
    for fn in file_names:
        fid = os.path.splitext(fn)[0]
        wav_name = fdir + '/' + fn
         # extract features
        feat_type = cfg.feat_params['type']
        extractor = F.prepare_extractor(feats=feat_type, params=cfg.feat_params)
        x, fs = F.load_sound_file(wav_name)
        assert (fs == 16000)
        feat = extractor.extract(x, fs)
        feat_file = '{}.npy'.format(fid)
        np.save(feat_file, np.squeeze(feat))
        print('[INFO] Features are extracted: %s' % feat_file)
        # forward network
        res = _forward_pass(feat_file, cfg.model_params)
        scores = res[feat_file]
        print('bonafide: %.4f\nspoof: %.4f' % (scores[0], scores[1]))
        
        y = 0 if 'bonafide' in fn else 1
        y_true.append(y)
        y_pred.append(scores[1])
    # TODO test: for bonafida scores 40%, for spoof 100%
    print('EER: %.4f' % metr.eer(y_true, y_pred))
