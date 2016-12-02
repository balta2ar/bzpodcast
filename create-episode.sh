#!/bin/bash

input_dir=$1
base=`basename $input_dir`
file_list="$base.txt"
episode="$base.mp3"

shift 1

ls $input_dir/**/*.mp3 | sort -V > $file_list
sed -i 's/^/file /' $file_list
#ffmpeg -f concat -i 2.txt absolute-beginner-s2-copy.mp3
#ffmpeg -f concat -i $file_list -c copy $episode
#ffmpeg -f concat -i $file_list -c libmp3lame $episode
ffmpeg -f concat $* -i $file_list -f mp3 -c libmp3lame -ar 44100 -ac 2 -b:a 128k $episode
python feed.py > feed.xml
