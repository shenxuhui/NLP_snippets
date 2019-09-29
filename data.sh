#! /usr/bin/env bash
set -u
set -e
set -o pipefail
base_dir=$(readlink -f $(dirname ${BASH_SOURCE[0]}))
cd $base_dir

dist_flag=first

function pre_process() {
    # dos2unix -f -n ./source-data/THUCNews/ONE-FILE/onefile.txt ./source-data/onefile.txt.dos2unix
    # ssh apple "cd $base_dir/;opencc -c zht2zhs.ini -i ./source-data/onefile.txt.dos2unix -o ./source-data/onefile.txt.dos2unix.opencc"
    # echo "opencc complete ..."

    ./py/norm_data.py ./source-data/onefile.txt.dos2unix.opencc ./source-data/onefile.txt.dos2unix.opencc.norm

    mv ./source-data/onefile.txt.dos2unix.opencc.norm ./source-data/onefile.txt.dos2unix.opencc.norm.out
    echo "pre_process complete"
}

function post_process()
{
    awk -F "" 'NF > 20 {print $0}' ./source-data/onefile.txt.dos2unix.opencc.norm.out > ./source-data/onefile.txt.dos2unix.opencc.norm.post_process
    # delete corpos have space such as "新浪体育讯 "
    grep -v " " ./source-data/onefile.txt.dos2unix.opencc.norm.post_process > ./source-data/onefile.txt.dos2unix.opencc.norm.post_process.nospace

    mv ./source-data/onefile.txt.dos2unix.opencc.norm.post_process.nospace ./source-data/onefile.txt.post_process.out
    echo "post_process complete"
}

function qdreamseg()
{
    echo "qdreamer seg ..."
    /restools/tools/segword/maxmatch/segmax -d ./dics/qdream_seg.dict -i ./source-data/onefile.txt.post_process.out > ./source-data/onefile.txt.post_process.qdreamseg
    echo "qdreamer seg complete"
}

function gen_train_and_test()
{
    # one word
    awk 'BEGIN{srand(1949)}{if (rand() > 0.05) print $0}' ./source-data/onefile.txt.post_process.out > ./source-data/onefile.txt.one_word.train
    awk 'BEGIN{srand(1949)}{if (rand() <= 0.05) print $0}' ./source-data/onefile.txt.post_process.out > ./source-data/onefile.txt.one_word.test

    # words
    awk 'BEGIN{srand(1949)}{if (rand() > 0.05) print $0}' ./source-data/onefile.txt.post_process.qdreamseg > ./source-data/onefile.txt.words.train
    awk 'BEGIN{srand(1949)}{if (rand() <= 0.05) print $0}' ./source-data/onefile.txt.post_process.qdreamseg > ./source-data/onefile.txt.words.test
    echo "gen_train_and_test complete"
}

function tag()
{
    # one word
    ./py/tag.py one_word ./source-data/onefile.txt.one_word.train ./source-data/onefile.txt.one_word.train.tag
    ./py/tag.py one_word ./source-data/onefile.txt.one_word.test ./source-data/onefile.txt.one_word.test.tag

    # words
    ./py/tag.py words ./source-data/onefile.txt.words.train ./source-data/onefile.txt.words.train.tag
    ./py/tag.py words ./source-data/onefile.txt.words.test ./source-data/onefile.txt.words.test.tag
    echo "tag complete"
}

pre_process
post_process
qdreamseg
gen_train_and_test
tag
