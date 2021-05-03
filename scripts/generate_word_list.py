import csv
import itertools
import json
import os
import string

from magoosh import get_magoosh_word_list

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def sort_dict(_dict):
    for k, v in _dict.items():
        _dict[k] = sorted(v)
    return _dict


def build_word_dict_from_csv(file_name):
    word_dict = {a: [] for a in list(string.ascii_lowercase)}
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            for word in row:
                if not word:
                    continue
                word_dict[word[0]].append(word.strip())
    for k, v in word_dict.items():
        word_dict[k] = sorted(v)
    return sort_dict(word_dict)


def build_word_dict_from_quizlet(file_name):
    word_dict = {a: [] for a in list(string.ascii_lowercase)}
    with open(file_name, mode="r") as reader:
        line = reader.readline()
        while line != "":  # The EOF char is an empty string
            word = line.split(":")[0].strip().lower()
            try:
                word_dict[word[0]].append(word)
            except KeyError:
                pass
            line = reader.readline()

    return word_dict


def combine_word_lists(*args):
    word_dict = {a: [] for a in list(string.ascii_lowercase)}

    for k, v in word_dict.items():
        combined_list = itertools.chain.from_iterable(list(a[k] for a in args))
        word_dict[k] = list(set(combined_list))

    return sort_dict(word_dict)


if __name__ == "__main__":
    """
    magoosh = 1006
    barrons = 333
    gregmat = 839
    magoosh + barrons = 1197
    gregmat + barrons = 1004
    magoosh + gregmat = 1504
    magoosh + gregmat + barrons = 1634
    """
    gregmat = build_word_dict_from_csv(
        os.path.join(CURRENT_DIR, "gregmat_wordlist.csv")
    )
    barron_333 = build_word_dict_from_quizlet(
        os.path.join(CURRENT_DIR, "barrons_333.txt")
    )
    barron_800 = build_word_dict_from_quizlet(
        os.path.join(CURRENT_DIR, "barron_800.txt")
    )
    barron_1100 = build_word_dict_from_quizlet(
        os.path.join(CURRENT_DIR, "barron_1100.txt")
    )
    word_smart = build_word_dict_from_quizlet(
        os.path.join(CURRENT_DIR, "word_smart.txt")
    )
    magoosh = get_magoosh_word_list()

    combined_word_list = combine_word_lists(
        magoosh, word_smart, barron_1100, barron_800, barron_333, gregmat
    )
    combined_total_word = sum(len(v) for k, v in combined_word_list.items())

    print("combined_total_word", combined_total_word)
    print(json.dumps(combined_word_list))
