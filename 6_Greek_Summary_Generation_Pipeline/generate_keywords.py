import os
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from collections import Counter

import pickle
import pandas as pd

from process_text import cleanup_sentences

def get_training_keywords(train_dir, gold_summary_dir):
    summary_keywords = []
    num_file = 0
    for file in os.listdir(os.path.join(train_dir, gold_summary_dir)):
        try:
            if ".DS_Store" in file:
                continue
            if num_file % 10 == 0:
                print("Processing File Number: ", num_file)
            num_file = num_file + 1
            file_id = file.split('.')[0]

            with open(os.path.join(train_dir, gold_summary_dir, str(file_id) + '.txt'), "r",
                      encoding='utf-8') as summary_file:
                tmp_file = []
                for line in summary_file:
                    line = line.replace("\n", "").replace("\t", " ").replace("\xa0", " ")
                    tmp_file.append(line)
                text = ' '.join(tmp_file)
                raw_sentences, clean_sentences = cleanup_sentences(text, 'es')
                for sent in clean_sentences:
                    words = nltk_word_tokenize(sent)
                    for word in words:
                        summary_keywords.append(word)
        except Exception as e:
            print(file, e)

    freq_summary_keywords = Counter(summary_keywords)
    print(freq_summary_keywords.most_common(5))

    max_freq = Counter(summary_keywords).most_common(1)[0][1]
    for word in freq_summary_keywords.keys():
        freq_summary_keywords[word] = (freq_summary_keywords[word] / max_freq)
    print(freq_summary_keywords.most_common(5))
    return freq_summary_keywords


def get_section_keywords(multi_lingual_cleaned_toc_sections_pickle_file, col_name):
    toc_section_df = pickle.load(open(multi_lingual_cleaned_toc_sections_pickle_file, 'rb'))
    keywords_weights = {}
    for index, row in toc_section_df.iterrows():
        words = nltk_word_tokenize(row[col_name])
        for word in words:
            try:
                keywords_weights[word] = keywords_weights[word] + row['score']
            except:
                keywords_weights[word] = row['score']
    keywords_weights = {k: v for k, v in sorted(keywords_weights.items(), key=lambda item: item[1], reverse=True)}
    return keywords_weights