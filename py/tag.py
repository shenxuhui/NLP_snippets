#! /usr/bin/env python
import sys

mode = sys.argv[1]
in_file = sys.argv[2]
out_file = sys.argv[3]

def tag_one_word(in_file, out_file):
    fout = open(out_file, 'w', encoding='utf8')
    for line in open(in_file, 'r', encoding='utf8'):
        if len(line) < 3:
            continue
        idx = 0
        for word in line:
            idx = idx + 1
            if len(line) - 1 == idx:
                break
            if word in [',', '.', '、', '?', '!']:
                continue
            if line[idx] == ",":
                fout.write(word + ' ' + 'C' + '\n')
            elif line[idx] == ".":
                fout.write(word + ' ' + 'P' + '\n')
            elif line[idx] == "、":
                fout.write(word + ' ' + 'T' + '\n')
            elif line[idx] == "?":
                fout.write(word + ' ' + 'Q' + '\n')
            elif line[idx] == "!":
                fout.write(word + ' ' + 'E' + '\n')
            else:
                fout.write(word + ' ' + 'O' + '\n')
        fout.write('\n')
    fout.close()

def tag_words(in_file, out_file):
    fout = open(out_file, 'w', encoding='utf8')
    for line in open(in_file, 'r', encoding='utf8'):
        if len(line) < 3:
            continue
        idx = 0
        line = line.strip('\n') # pay attention to the tail of sentence.
        line = line.split(' ')
        for word in line:
            idx = idx + 1
            if len(line) == idx:
                break
            if word in [',', '.', '、', '?', '!']:
                continue
            if line[idx] == ",":
                fout.write(word + ' ' + 'C' + '\n')
            elif line[idx] == ".":
                fout.write(word + ' ' + 'P' + '\n')
            elif line[idx] == "、":
                fout.write(word + ' ' + 'T' + '\n')
            elif line[idx] == "?":
                fout.write(word + ' ' + 'Q' + '\n')
            elif line[idx] == "!":
                fout.write(word + ' ' + 'E' + '\n')
            else:
                fout.write(word + ' ' + 'O' + '\n')
        fout.write('\n')
    fout.close()

if __name__ == "__main__":
    if mode == 'one_word':
        tag_one_word(in_file, out_file)
    elif mode == 'words':
        tag_words(in_file, out_file)
    else:
        print("Must choose one mode between one_word and words.")
        exit(-1)

