#!/bin/bash

# set -x
# trap read debug

echo $0 "$@"

data_dir=$1
out_dir=$2

mkdir -p $out_dir || exit 1;

# check that sox is installed 
which sox  &>/dev/null
if [[ $? != 0 ]]; then 
 echo "sox is not installed"
 exit 1 
fi

(
for w in `find $data_dir -name *.flac` ; do 
  base=`basename $w .flac`
  fullpath=`utils/make_absolute.sh $w`
  echo "$base sox $fullpath -r 16000 -t wav - |"
done
)  | sort -u > $out_dir/wav.scp

echo "[INFO] data prep audio succeded: `wc -l $out_dir/wav.scp`"
#exit 0