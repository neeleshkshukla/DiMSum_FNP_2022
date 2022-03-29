import os
import pickle


def extract_section_body(file_id, section_name, dir_path, reports_dir, toc_loc_pickle_file_path):
    with open(toc_loc_pickle_file_path, "rb") as input_toc_pkl_file:
        file_toc = pickle.load(input_toc_pkl_file)
    try:
        (file_id_pages, file_id_sections) = file_toc[str(file_id)]
    except Exception as e:
        print('File id: ', file_id, ' not found!')
        return None

    num_sections = len(file_id_sections)
    try:
        section_index = file_id_sections.index(section_name)
    except Exception as e:
        print('Section: ', section_name, ' in file id: ', file_id, ' not found!')
        return None

    tmp_file = []
    with open(os.path.join(dir_path, reports_dir, str(file_id) + '.txt'), "r", encoding='utf-8') as report_file:
        for line in report_file:
            line = line.replace("\n", "").replace("\t", " ").replace("\xa0", " ")
            tmp_file.append(line)

    start_page = file_id_pages[section_index]

    # last section
    if section_index == num_sections - 1:
        body = " ".join(tmp_file[start_page:])
    else:
        end_page = file_id_pages[section_index + 1]
        body = " ".join(tmp_file[start_page:end_page])
    return body