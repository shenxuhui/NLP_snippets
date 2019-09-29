#! /usr/bin/env python3

import os
import io
import sys
import unicodedata
import regex

in_file = sys.argv[1]
out_file= sys.argv[2]

word_replace_dict_path = './dics/q2b.dic'
word2id_dict_path = './dics/word.dic'

def is_punctuation_char(char):
    return unicodedata.category(char).startswith('P')

def is_L_or_Num_char(char):
    return (unicodedata.category(char).startswith('N') or unicodedata.category(char).startswith('L'))

def is_Num_char(char):
    return unicodedata.category(char).startswith('N')

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

def norm_number(line):
    if len(line) < 3:
        return ''

    line=regex.sub('(\p{N}+)(年)(-)(\p{N}+)(年)', "一九四九年到一九四九年", line)
    line=regex.sub('(\p{N}+)(月)(-)(\p{N}+)(月)', "十月到十月", line)
    line=regex.sub('(\p{N}+)(日|号)(-)(\p{N}+)(日|号)', "一日到一日", line)

    line=regex.sub('(\p{N}+)(年)', "一九四九年", line)
    line=regex.sub('(\p{N}+)(月)', "十月", line)
    line=regex.sub('(\p{N}+)(日|号)', "一日", line)
    line=regex.sub('(零|一|二|三|四|五|六|七|八|九|十)+(年)', "一九四九年", line)
    line=regex.sub('(零|一|二|三|四|五|六|七|八|九|十)+(月)', "十月", line)
    line=regex.sub('(零|一|二|三|四|五|六|七|八|九|十)+(日|号)', "一日", line)

    line=regex.sub('(\p{N}*)([\.]?)(\p{N}+)([\.]?)(%)(-)(\p{N}*)([\.]?)(\p{N}+)([\.]?)(%)', "百分之六到百分之六", line)
    line=regex.sub('(\p{N}*)([\.]?)(\p{N}+)([\.]?)(-)(\p{N}*)([\.]?)(\p{N}+)([\.]?)',  "六到六", line)
    line=regex.sub('(-)(\p{N}*)([\.]?)(\p{N}+)([\.]?)(%)', "负百分之六", line)
    line=regex.sub('(\p{N}*)([\.]?)(\p{N}+)([\.]?)(%)', "百分之六", line)

    line=regex.sub('(\p{N}+)([\.])(\p{N}+)', "六点六", line)

    line=regex.sub('(\p{N}+)', "六", line)

    return line

def merge_some_punctuation(line):
    if len(line) == 0:
        return ''
    merge_list_0 = ['-'] # keep

    merge_list_1 = ['/', '》', '《', '"', '\'', '\)', '\(', '\]', '\['] # merge to NULL
    merge_list_2 = [':', ';'] # merge to commas

    for char in merge_list_1:
        line = regex.sub(char, '', line)

    for char in merge_list_2:
        line = regex.sub(char, ',', line)

    return line

def clean_text(line):
    # delete line if line have some strange word, such as www, http, etc.
    r=regex.search(r'www|http|jsp|html|font|img|OOV', line)
    if r != None:
        return ''

    # delete line if line have some strange character, such as html and email address, etc.
    need_to_delete_char_set=['﹏', '〃','‐', '︱', '″', '§', '︰', '※', '′', '{', '}', '@', '#', '―', '\\', '‰', '&', '–', '·', '*', '_']
    for word in line:
        if word in need_to_delete_char_set:
            return ''

    # remove senseless character
    # 1. Zl: Separator, line
    # 2. Zp: Separator, paragraph
    # 3. Cc, Cf, Cs, Co, Cn
    # 4. Sm, Sc, Sk, So
    # 5. Mn, Mc, Me
    line = regex.sub(r'[\p{Zl}\p{Zp}\p{C}\p{S}\p{M}]', '', line)

    # norm space to normal
    line = regex.sub(r'\p{Zs}', ' ', line)

    # delete []() inner line
    line = regex.sub(r'[\(\[].*[\)\]]', '', line)

    # delete line if first character is punctuation or num, tail character is not punctuation.
    line = line.strip()
    if (len(line) < 3):
        return ''

    if (line[len(line) - 1] not in ['.', '?', '!']) or (is_punctuation_char(line[0])):
        return ''

    if (regex.match('^(\p{N}+)(年|月|日|号|个)', line) == None) and (is_Num_char(line[0])):
        return ''

    return line

def norm_to_dict(line, word_replace_dict, word2id_dict):
    index = 0
    new_line = ''
    index += 1
    bad_line = False
    for word in line:
        if ord(word) < 0x20:
            word = ' '
        if word in word_replace_dict:
            word = word_replace_dict[word]
        if word not in word2id_dict:
            word = "OOV"
        new_line += word

    return new_line

def main_process(in_filename, out_filename):
    fout = open(out_filename, "w", encoding='utf8')
    word_replace_dict = load_dict(word_replace_dict_path)
    word2id_dict = load_reverse_dict(word2id_dict_path)

    for line in io.open(in_filename, 'r', encoding='utf8'):
        if (len(line) < 3) or (regex.match(r'^[ ]*$', line) != None):
            continue
        line = line.strip("\n")
        new_line = norm_to_dict(line, word_replace_dict, word2id_dict)
        new_line = clean_text(new_line)
        new_line = merge_some_punctuation(new_line)
        new_line = norm_number(new_line)
        if (len(new_line) < 3) or (regex.match(r'^[ ]*$', new_line) != None):
            continue

        fout.write(new_line + '\n')

    fout.close()

if __name__ == "__main__":
    main_process(in_file, out_file)
