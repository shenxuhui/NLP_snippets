#! /usr/bin/env python3

import os
import io
import sys
import unicodedata
import regex

in_file = sys.argv[1]
out_file= sys.argv[2]

def is_punctuation_char(char):
    return unicodedata.category(char).startswith('P')

def is_L_or_Num_char(char):
    return (unicodedata.category(char).startswith('N') or unicodedata.category(char).startswith('L'))

def is_chinese(char):
    return unicodedata.name(char).startswith('CJK')

def load_dict(dict_path):
    """
    Load a dict. The first column is the key and the second column is the value.
    """
    result_dict = {}
    for line in io.open(dict_path, "r", encoding='utf8'):
        terms = line.strip("\n").split("\t")
        if len(terms) != 2:
            continue
        result_dict[terms[0]] = terms[1]
    return result_dict

def load_reverse_dict(dict_path):
    """
    Load a dict. The first column is the value and the second column is the key.
    """
    result_dict = {}
    for line in io.open(dict_path, "r", encoding='utf8'):
        terms = line.strip("\n").split("\t")
        if len(terms) != 2:
            continue
        result_dict[terms[1]] = terms[0]
    return result_dict

def clean_text(text):
    # remove senseless character
    # 1. Zl: Separator, line
    # 2. Zp: Separator, paragraph
    # 3. Cc, Cf, Cs, Co, Cn
    # 4. Sm, Sc, Sk, So
    # 5. Mn, Mc, Me
    text = regex.sub(r'[\p{Zl}\p{Zp}\p{C}\p{S}\p{M}]', '', text)

    # norm space to normal
    text = regex.sub(r'\p{Zs}', ' ', text)

    return text + '\n'

def norm_to_dict(line, word_replace_dict, word2id_dict):
    index = 0
    new_line = ''
    index += 1
    bad_line = False
    line = line.strip("\n")
    for word in line:
        if ord(word) < 0x20:
            word = ' '
        if word in word_replace_dict:
            word = word_replace_dict[word]
        if word not in word2id_dict:
            word = "OOV"
        new_line += word

    return new_line + '\n'

dict={}
def main_process(in_filename, out_filename):
    fout = open(out_filename, "w", encoding='utf8')

    for line in io.open(in_filename, 'r', encoding='utf8'):
        line = line.strip("\n")
        if len(line) == 0:
            continue
        for word in line:
            if is_punctuation_char(word):
                if word not in dict:
                    dict[word] = 1
                else:
                    dict[word] = dict[word] + 1
    for _punc in dict:
        fout.write(_punc + ' ' + str(dict[_punc]) + ' ' + str(unicodedata.category(_punc)) + ' ' + str(ord(_punc)) + '\n')
    fout.close()

if __name__ == "__main__":
    main_process(in_file, out_file)
