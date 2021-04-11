import csv
import string
import json
import os

from magoosh import get_magoosh_word_list

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
word_dict = {a: [] for a in list(string.ascii_lowercase)}


def sort_dict(_dict):
    for k, v in _dict.items():
        _dict[k] = sorted(v)
    return _dict


def build_word_dict_from_csv(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for word in row:
                if not word:
                    continue
                word_dict[word[0]].append(word)
    for k, v in word_dict.items():
        word_dict[k] = sorted(v)
    return sort_dict(word_dict)


def build_word_dict_from_quizlet(file_name):
    with open(file_name, mode='r') as reader:
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            word = line.strip().split("-")[0].lower()
            word_dict[word[0]].append(word)
            line = reader.readline()

    return word_dict


def merge_two_word_list(_dict1, _dict2):
    merged = {a: [] for a in list(string.ascii_lowercase)}
    for k, v in merged.items():
        merged[k] = _dict1[k] + _dict2[k]

    return sort_dict(merged)


if __name__ == '__main__':
    gregmat = build_word_dict_from_csv(os.path.join(CURRENT_DIR, "gregmat_wordlist.csv"))
    barrons_333 = build_word_dict_from_quizlet(os.path.join(CURRENT_DIR, "barrons_333.txt"))
    magoosh = get_magoosh_word_list()
    magoosh_gregmat_barron333 = merge_two_word_list(merge_two_word_list(gregmat, magoosh), barrons_333)
    print(json.dumps(magoosh_gregmat_barron333))

