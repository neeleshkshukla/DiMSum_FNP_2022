from nltk.tokenize import word_tokenize as nltk_word_tokenize
from heapq import nlargest

def get_summary_training_keywords(freq_summary_keywords, clean_sentences, raw_sentences, num_sents=3, num_neighbour=3):
    index_strength = {}
    for idx, sent in enumerate(clean_sentences):
        words = nltk_word_tokenize(sent)
        for word in words:
            if word in freq_summary_keywords.keys():
                if idx in index_strength.keys():
                    index_strength[idx] += freq_summary_keywords[word]
                else:
                    index_strength[idx] = freq_summary_keywords[word]

    summarized_indexes = nlargest(num_sents, index_strength, key=index_strength.get)
    final_sentences = []
    for idx in summarized_indexes:
        start_idx = idx - num_neighbour
        end_idx = idx + num_neighbour
        if end_idx > len(raw_sentences):
            end_idx = len(raw_sentences)
        if start_idx < 0:
            start_idx = 0
        final_sentences.extend(raw_sentences[start_idx: end_idx + 1])
    #final_sentences = [raw_sentences[idx] for idx in summarized_indexes]
    summary = ' '.join(final_sentences)
    return summary


def get_summary_section_keywords(keywords_weights, clean_sentences, raw_sentences, num_sents=3, num_neighbour=3):
    sent_strength = {}
    index_strength = {}
    for idx, sent in enumerate(clean_sentences):
        words = nltk_word_tokenize(sent)
        for word in words:
            if word in keywords_weights.keys():
                if idx in index_strength.keys():
                    index_strength[idx] += keywords_weights[word]
                else:
                    index_strength[idx] = keywords_weights[word]

    summarized_indexes = nlargest(num_sents, index_strength, key=index_strength.get)
    final_sentences = []
    for idx in summarized_indexes:
        start_idx = idx - num_neighbour
        end_idx = idx + num_neighbour
        if end_idx > len(raw_sentences):
            end_idx = len(raw_sentences)
        if start_idx < 0:
            start_idx = 0
        final_sentences.extend(raw_sentences[start_idx: end_idx+1])
    # final_sentences = [ raw_sentences[idx] for idx in summarized_indexes ]
    summary = ' '.join(final_sentences)
    return summary