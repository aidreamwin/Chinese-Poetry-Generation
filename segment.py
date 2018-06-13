#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from common import *
import jieba

_raw_sxhy_path = os.path.join(raw_dir, 'shixuehanying.txt')

_sxhy_path = os.path.join(data_dir, 'sxhy_dict.txt')

def _gen_sxhy_dict():
    print("Parsing shixuehanying dictionary ...")
    words = set()
    with open(_raw_sxhy_path, 'r') as fin:
        for line in fin.readlines():
            if line[0] == '<':
                continue
            for phrase in line.strip().split()[1:]:
                if not is_cn_sentence(phrase):
                    continue
                idx = 0
                while idx + 4 <= len(phrase):
                    # Cut 2 chars each time.
                    words.add(phrase[idx : idx + 2])
                    idx += 2
                # Use jieba to cut the last 3 chars.
                if idx < len(phrase):
                    for word in jieba.lcut(phrase[idx:]):
                        words.add(word)
    with open(_sxhy_path, 'w') as fout:
        fout.write(' '.join(words))


class Segmenter(object):

    def __init__(self):
        if not os.path.exists(_sxhy_path):
            _gen_sxhy_dict()
        with open(_sxhy_path, 'r') as fin:
            self.sxhy_dict = set(fin.read().split())

    def segment(self, sentence):
        toks = []
        idx = 0
        while idx + 4 <= len(sentence):
            # Cut 2 chars each time.
            if sentence[idx : idx + 2] in self.sxhy_dict:
                toks.append(sentence[idx : idx + 2])
            else:
                for tok in jieba.lcut(sentence[idx : idx + 2]):
                    toks.append(tok)
            idx += 2
        # Cut last 3 chars.
        if idx < len(sentence):
            if sentence[idx : ] in self.sxhy_dict:
                toks.append(sentence[idx : ])
            else:
                for tok in jieba.lcut(sentence[idx : ]):
                    toks.append(tok)
        return toks


# For testing purpose.
if __name__ == '__main__':
    segmenter = Segmenter()
    with open(os.path.join(raw_dir, 'qts_tab.txt'), 'r') as fin:
        for line in fin.readlines()[1 : ]:
            for sentence in split_sentences(line.strip().split()[3]):
                print(' '.join(segmenter.segment(sentence)))
