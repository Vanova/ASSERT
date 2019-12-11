#!/bin/bash
# extract fbank, mfcc, logspec, ivector features for:
# ASVspoof2019 LA train, LA dev, LA eval, PA train, PA dev, PA eval

# set -x
# trap read debug

. ./cmd.sh
. ./path.sh
set -e
mfccdir=`pwd`/mfcc
fbankdir=`pwd`/fbank
specdir=`pwd`/logspec
vadir=`pwd`/mfcc
data_root=/home/vano/wrkdir/datasets/asvspoof2019

stage=2

if [ $stage -eq 1 ]; then
	# first create spk2utt 
	for name in ASVspoof2019_PA_train; do # ASVspoof2019_PA_dev
		local/prep_wav.sh $data_root/PA/$name data/$name
		cut -d" " -f1 data/$name/wav.scp > data/$name/tmp
		pr -mts' ' data/$name/tmp data/$name/tmp > data/$name/utt2spk
		rm -rf data/$name/tmp
		utils/utt2spk_to_spk2utt.pl data/${name}/utt2spk > data/${name}/spk2utt
		utils/fix_data_dir.sh data/${name}
	done

	for name in ASVspoof2019_LA_train; do #  ASVspoof2019_LA_dev
		local/prep_wav.sh $data_root/LA/$name data/$name
		cut -d" " -f1 data/$name/wav.scp > data/$name/tmp
		pr -mts' ' data/$name/tmp data/$name/tmp > data/$name/utt2spk
		rm -rf data/$name/tmp
		utils/utt2spk_to_spk2utt.pl data/${name}/utt2spk > data/${name}/spk2utt
		utils/fix_data_dir.sh data/${name}
	done
fi

if [ $stage -eq 2 ]; then
	for name in ASVspoof2019_PA_train ASVspoof2019_LA_train; do # ASVspoof2019_PA_dev ASVspoof2019_LA_dev
		# logspec		
		utils/copy_data_dir.sh data/${name} data/${name}_spec
		local/make_spectrogram.sh --fbank-config conf/spec.conf --nj 40 --cmd "$train_cmd" \
		  data/${name}_spec exp/make_spec $specdir
		utils/fix_data_dir.sh  data/${name}_spec

		# # fbank
		# utils/copy_data_dir.sh data/${name} data/${name}_fbank
		# steps/make_fbank.sh --fbank-config conf/fbank.conf --nj 40 --cmd "$train_cmd" \
		# 	data/${name}_fbank exp/make_fbank $fbankdir     	
		# utils/fix_data_dir.sh  data/${name}_fbank

		# apply cm for the extracted features 
		# cm is 3-second sliding window
		
		# # fbank
		# utils/copy_data_dir.sh data/${name}_fbank data/${name}_fbank_cm
		# feats="ark:apply-cmvn-sliding --norm-vars=false --center=true --cmn-window=300 scp:`pwd`/data/${name}_fbank/feats.scp ark:- |"
		# copy-feats "$feats" ark,scp:`pwd`/data/${name}_fbank_cm/feats.ark,`pwd`/data/${name}_fbank_cm/feats.scp
		# utils/fix_data_dir.sh  data/${name}_fbank_cm
	
		# # logspec
		# utils/copy_data_dir.sh data/${name}_spec data/${name}_spec_cm
		# feats="ark:apply-cmvn-sliding --norm-vars=false --center=true --cmn-window=300 scp:`pwd`/data/${name}_spec/feats.scp ark:- |"
		# copy-feats "$feats" ark,scp:`pwd`/data/${name}_spec_cm/feats.ark,`pwd`/data/${name}_spec_cm/feats.scp
		# utils/fix_data_dir.sh  data/${name}_spec_cm
	done
fi
