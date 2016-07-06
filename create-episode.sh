#!/bin/bash

input_dir=$1
base=`basename $input_dir`
file_list="$base.txt"
episode="$base.mp3"

ls $input_dir/*.mp3 | sort -V > $file_list
sed -i 's/^/file /' $file_list
#ffmpeg -f concat -i 2.txt absolute-beginner-s2-copy.mp3
ffmpeg -f concat -i $file_list -c copy $episode
python feed.py > feed.xml
