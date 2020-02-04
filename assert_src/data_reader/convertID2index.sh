#!/bin/bash

wavscp=/home/vano/wrkdir/projects/antispoofing_speech/kaldi_feats/data/tasks/wav.scp
out_lab=utt2systemID/tasks_utt2systemID
out_labid=utt2systemID/tasks_utt2index_8
ext=".wav"

echo "Remove old version: $out_lab, $out_labid"
rm -rf $out_lab $out_labid

while IFS= read -r line; do
  fid=$(cut -d" " -f1 <<< $line)
  fpath=$(cut -d" " -f3 <<< $line)
  fn=$(basename $fpath $ext)
  label=$(cut -d"_" -f1 <<< $fn)
  echo "$fid $label" >> $out_lab

  if [[ "$label" == "bonafide" ]]; then 
    echo "$fid 0" >> $out_labid
  elif [[ "$label" == "spoof" ]]; then
    echo "$fid 1" >> $out_labid
  fi
done < "$wavscp"

echo "[INFO] labels prep succeded: $out_lab `wc -l $out_lab`"
echo "[INFO] labels prep succeded: $out_labid `wc -l $out_labid`"
