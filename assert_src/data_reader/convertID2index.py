# create multi-labels for model training


def convert_la(scp_file, systemID_file, out_index_file, out_ID_file):
    ''' multi-class classification for LA: SS_1, SS_2, SS_4, US_1, VC_1, VC_4 --> 7 classes
        (bonafide: 0), (SS_1: 1), (SS_2: 2), (SS_4: 3), (US_1: 4), (VC_1: 5), (VC_4: 6)
    '''
    with open(scp_file) as f:
        temp = f.readlines()
    key_list = [x.strip().split()[0] for x in temp]

    with open(systemID_file) as f:
        temp = f.readlines()
    utt2ID = {x.strip().split()[1]: x.strip().split()[3] for x in temp}

    with open(out_index_file, 'w') as f:
        with open(out_ID_file, 'w') as fID:
            for i, key in enumerate(key_list):
                if key in utt2ID:
                    label = utt2ID[key]
                else:
                    print('[WARN] Utterance is absent: %d: %s' % (i, key))
                    continue

                if label == '-':
                    fID.write('%s %s\n' % (key, 'bonafide'))
                else:
                    fID.write('%s %s\n' % (key, label))

                if label == '-':  # bonafide
                    f.write('%s %d\n' % (key, 0))
                elif label == 'A01':
                    f.write('%s %d\n' % (key, 1))
                elif label == 'A02':
                    f.write('%s %d\n' % (key, 2))
                elif label == 'A03':
                    f.write('%s %d\n' % (key, 3))
                elif label == 'A04':
                    f.write('%s %d\n' % (key, 4))
                elif label == 'A05':
                    f.write('%s %d\n' % (key, 5))
                elif label == 'A06':
                    f.write('%s %d\n' % (key, 6))
                else:
                    print('[INFO] new label: %s' % label)
                    f.write('%s %d\n' % (key, int(label[1:])))


def convert_pa(scp_file, systemID_file, out_index_file, out_ID_file):
    ''' multi-class classification for PA: AA, AB, AC, BA, BB, BC, CA, CB, CC --> 10 classes
        (bonafide: 0), (AA: 1), (AB: 2), (AC: 3), (BA: 4), (BB: 5), (BC: 6),
        (CA: 7), (CB: 8), (CC: 9)
    '''
    with open(scp_file) as f:
        temp = f.readlines()
    key_list = [x.strip().split()[0] for x in temp]
    print(len(key_list))

    with open(systemID_file) as f:
        temp = f.readlines()
    utt2ID = {x.strip().split()[1]: x.strip().split()[3] for x in temp}

    with open(out_index_file, 'w') as f:
        with open(out_ID_file, 'w') as f2:
            for i, key in enumerate(key_list):
                if key in utt2ID:
                    label = utt2ID[key]
                else:
                    print('[WARN] Utterance is absent: %d: %s' % (i, key))
                    continue

                if label == '-':
                    f2.write('%s %s\n' % (key, 'bonafide'))
                else:
                    f2.write('%s %s\n' % (key, label))

                if label == '-': # 'bonafide'
                    f.write('%s %d\n' % (key, 0))
                elif label == 'AA':
                    f.write('%s %d\n' % (key, 1))
                elif label == 'AB':
                    f.write('%s %d\n' % (key, 2))
                elif label == 'AC':
                    f.write('%s %d\n' % (key, 3))
                elif label == 'BA':
                    f.write('%s %d\n' % (key, 4))
                elif label == 'BB':
                    f.write('%s %d\n' % (key, 5))
                elif label == 'BC':
                    f.write('%s %d\n' % (key, 6))
                elif label == 'CA':
                    f.write('%s %d\n' % (key, 7))
                elif label == 'CB':
                    f.write('%s %d\n' % (key, 8))
                elif label == 'CC':
                    f.write('%s %d\n' % (key, 9))


def convert_pa_leave_one_out(scp_file, systemID_file, out_file):
    ''' multi-class classification for PA: AA, AB, AC, BA, BB, BC, CA, CB, CC --> 10 classes
        (bonafide: 0), (AB: 1), (AC: 2), (BA: 3), (BB: 4), (BC: 5),
        (CA: 6), (CB: 7), (CC: 8), (AA: 9)
    '''
    with open(scp_file) as f:
        temp = f.readlines()
    key_list = [x.strip().split()[0] for x in temp]

    with open(systemID_file) as f:
        temp = f.readlines()
    utt2ID = {x.strip().split()[0]: x.strip().split()[1] for x in temp}

    with open(out_file, 'w') as f:
        for key in key_list:
            curr_utt = ''.join(key.split('-')[0] + '-' + key.split('-')[1])
            label = utt2ID[curr_utt]
            if label == 'bonafide':
                f.write('%s %d\n' % (key, 0))
            elif label == 'AA':
                f.write('%s %d\n' % (key, 9))
            elif label == 'AB':
                f.write('%s %d\n' % (key, 1))
            elif label == 'AC':
                f.write('%s %d\n' % (key, 2))
            elif label == 'BA':
                f.write('%s %d\n' % (key, 3))
            elif label == 'BB':
                f.write('%s %d\n' % (key, 4))
            elif label == 'BC':
                f.write('%s %d\n' % (key, 5))
            elif label == 'CA':
                f.write('%s %d\n' % (key, 6))
            elif label == 'CB':
                f.write('%s %d\n' % (key, 7))
            elif label == 'CC':
                f.write('%s %d\n' % (key, 8))


if __name__ == '__main__':
    curr_wd = 'utt2systemID/'

    data_root = '/home/vano/wrkdir/datasets/asvspoof2019/'
    feat_dir = '/home/vano/wrkdir/projects/antispoofing_speech/kaldi_feats/data/'

    systemID_files = [data_root + 'LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.dev.trl.txt',
                      data_root + 'LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt',
                      data_root + 'LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.eval.trl.txt',
                      data_root + 'PA/ASVspoof2019_PA_cm_protocols/ASVspoof2019.PA.cm.dev.trl.txt',
                      data_root + 'PA/ASVspoof2019_PA_cm_protocols/ASVspoof2019.PA.cm.train.trn.txt',
                      data_root + 'PA/ASVspoof2019_PA_cm_protocols/ASVspoof2019.PA.cm.eval.trl.txt']
    out_files = ['la_dev_utt2index_8',
                 'la_train_utt2index_8',
                 'la_eval_utt2index_8',
                 'pa_dev_utt2index_8',
                 'pa_train_utt2index_8',
                 'pa_eval_utt2index_8']
    out_ID_files = ['la_dev_utt2systemID',
                    'la_train_utt2systemID',
                    'la_eval_utt2systemID',
                    'pa_dev_utt2systemID',
                    'pa_train_utt2systemID',
                    'pa_eval_utt2systemID']

    scp_files = [feat_dir + 'ASVspoof2019_LA_dev_spec/feats.scp',
                 feat_dir + 'ASVspoof2019_LA_train_spec/feats.scp',
                 feat_dir + 'ASVspoof2019_LA_eval_spec/feats.scp',
                 feat_dir + 'ASVspoof2019_PA_dev_spec/feats.scp',
                 feat_dir + 'ASVspoof2019_PA_train_spec/feats.scp',
                 feat_dir + 'ASVspoof2019_PA_eval_spec/feats.scp',]

    for i in range(2, 3):
        convert_la(scp_files[i], systemID_files[i],
                   curr_wd + out_files[i], curr_wd + out_ID_files[i])
    
    #for i in range(5, 6):        
    #    convert_pa(scp_files[i], systemID_files[i],
    #               curr_wd + out_files[i], curr_wd + out_ID_files[i])

    """ 
    la  |  spec with cm  |  la_{train,dev}_spec_cm_tensor.scp   |  (257 by 400)  |  la_{train,dev}_utt2index    |  regular 
    pa  |  spec with cm  |  pa_{train,dev}_spec_cm_tensor.scp   |  (257 by 500)  |  pa_{train,dev}_utt2index    |  regular 
    pa  |  spec          |  pa_{train,dev}_spec_tensor3.scp     |  (257 by 400)  |  pa_{train,dev}_utt2index_2  |  regular
    pa  |  spec with cm  |  pa_{train,dev}_spec_cm_tensor2.scp  |  (257 by 400)  |  pa_{train,dev}_utt2index_2  |  regular
    la  |  cqcc with cm  |  la_{train,dev}_cqcc_cm_tensor.scp   |  (30  by 400)  |  la_{train,dev}_utt2index_3  |  regular
    pa  |  cqcc with cm  |  pa_{train,dev}_cqcc_cm_tensor2.scp  |  (30  by 400)  |  pa_{train,dev}_utt2index_4  |  regular
    la  |  cqcc          |  la_{train,dev}_cqcc_tensor.scp      |  (30  by 400)  |  la_{train,dev}_utt2index_3  |  regular
    pa  |  cqcc          |  pa_{train,dev}_cqcc_tensor2.scp     |  (30  by 400)  |  pa_{train,dev}_utt2index_4  |  regular
    pa  |  cpc_1         |  pa_{train,dev}_cpc_1_tensor_400.scp |  (256 by 400)  |  pa_{train,dev}_utt2index_5  |  regular
    pa  |  spec          |  pa_{train,dev}_spec_tensor3.scp     |  (257 by 400)  |  pa_{train,dev}_utt2index_6  |  leave out AA
    la  |  spec          |  la_{train,dev}_spec_tensor.scp      |  (257 by 400)  |  la_{train,dev}_utt2index    |  regular 
    la  |  cpc_2         |  la_{train,dev}_cpc_2_tensor_400.scp |  (257 by 400)  |  la_{train,dev}_utt2index_7  |  regular
    pa  |  cpc_2         |  pa_{train,dev}_cpc_2_tensor_400.scp |  (257 by 400)  |  pa_{train,dev}_utt2index_7  |  regular
    la  |  spec (slide)  |  la_{train,dev}_spec_tensor4.scp     |  (257 by 400)  |  la_{train,dev}_utt2index_8  |  regular
    pa  |  spec (slide)  |  pa_{train,dev}_spec_tensor4.scp     |  (257 by 400)  |  pa_{train,dev}_utt2index_8  |  regular
    """
