import os
import pickle
import pandas as pd

bad_file = ["7796.txt","14018.txt","23372.txt","4842.txt","11692.txt","2633.txt","132.txt","18103.txt","9588.txt","11736.txt","6586.txt"]

def check_in_summary(tmp_file, toc):
    is_in_summary = False
    for line in tmp_file:
        if line=="":
            continue
        if toc in line:
            return True
    return is_in_summary


def annotate_toc_against_sumamry(dir_path, summary_dir, out_dir_path, out_toc_pos_file_name, out_toc_len_file_name):
    summary_path = os.path.join(dir_path, summary_dir)
    with open(os.path.join(out_dir_path, out_toc_pos_file_name), "rb") as input_file:
        file_toc_pos = pickle.load(input_file)

    print(out_toc_pos_file_name, ' loaded')

    with open(os.path.join(out_dir_path, out_toc_len_file_name), "rb") as input_file1:
        file_toc_len = pickle.load(input_file1)

    print(out_toc_len_file_name, ' loaded')

    sections_to_be_processed = 0
    for key in file_toc_pos.keys():
        (pages, tocs) = file_toc_pos[key]
        sections_to_be_processed = sections_to_be_processed + len(pages)

    print('Total sections to be processed: ', sections_to_be_processed)
    print('Building dataframe')

    file_num = 0
    toc_annotated_df = pd.DataFrame(
        columns=['file_id', 'toc_section', 'toc_section_pos', 'toc_section_len', 'is_section_in_summary'])
    for key in file_toc_pos.keys():
        file_id = key
        if file_num % 300 == 0:
            print('processing file num ', file_num)

        tmp_file = []
        for file in os.listdir(summary_path):

            if file in bad_file:
                print('bad_file')
                continue
            if ".DS_Store" in file:
                print('bad_file')
                continue
            if os.path.isfile(os.path.join(summary_path, file)) and file_id == file.split("_")[0]:
                # print('file found', file)
                with open(os.path.join(summary_path, file), "r", encoding='utf-8') as f:
                    for line in f:
                        line = line.replace("\n", "").replace("\t", " ").replace("\xa0", " ")
                        tmp_file.append(line)

        (pages, tocs) = file_toc_pos[key]
        (lens, tocs) = file_toc_len[key]
        for i in range(len(pages)):
            toc = tocs[i]
            is_in_summary = check_in_summary(tmp_file, toc)
            toc_annotated_df.loc[len(toc_annotated_df.index)] = [file_id, tocs[i], pages[i], lens[i], is_in_summary]

        file_num = file_num + 1

    print('Annotated dataset shape', toc_annotated_df.shape)

    return toc_annotated_df