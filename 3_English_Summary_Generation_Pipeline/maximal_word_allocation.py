import numpy as np

def get_number_of_words(section_scores, section_body_len, total_num_require_words, prev_num_required_words):
    extract_section_words = np.zeros(len(section_scores))
    # Terminating condition 1
    if total_num_require_words == 0:
        return prev_num_required_words + extract_section_words

    if sum(section_scores) == 0:
        return prev_num_required_words + extract_section_words

    num_required_words = np.floor(total_num_require_words * section_scores / sum(section_scores))

    # Terminating condition 2
    all_required_words_less_than_body_words = True
    for i in range(len(section_scores)):
        if num_required_words[i] <= section_body_len[i]:
            continue
        else:
            all_required_words_less_than_body_words = False
    if all_required_words_less_than_body_words == True:
        return prev_num_required_words + num_required_words

    # Terminating condition 3
    all_required_words_greater_than_body_words = True
    for i in range(len(section_scores)):
        if num_required_words[i] >= section_body_len[i]:
            continue
        else:
            all_required_words_greater_than_body_words = False
    if all_required_words_greater_than_body_words == True:
        return prev_num_required_words + section_body_len

    remaining_required_words = 0
    for i in range(len(section_scores)):
        if num_required_words[i] > section_body_len[i]:
            remaining_required_words = remaining_required_words + (num_required_words[i] - section_body_len[i])
            num_required_words[i] = prev_num_required_words[i] + section_body_len[i]
            section_body_len[i] = 0
            section_scores[i] = 0
        elif num_required_words[i] < section_body_len[i]:
            section_body_len[i] = section_body_len[i] - num_required_words[i]
            num_required_words[i] = prev_num_required_words[i] + num_required_words[i]
        else:
            num_required_words[i] = prev_num_required_words[i] + num_required_words[i]
            section_body_len[i] = 0
            section_scores[i] = 0

    return get_number_of_words(section_scores, section_body_len, remaining_required_words, num_required_words)