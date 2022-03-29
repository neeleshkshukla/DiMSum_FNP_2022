def get_relevant_sections_with_scores_in_file(file_id, df):
    return df[(df.file_id == file_id) & (df.pred == 1)][['toc_section', 'True']].to_dict('list')

def get_relevant_sections_with_scores(df):
    file_ids = df.file_id.unique()
    for file_id in file_ids:
        relevant_section = get_relevant_sections_with_scores_in_file(file_id, df)
        print('file_id: ', file_id , '.txt')
        print(relevant_section['toc_section'])
        print(relevant_section['True'])
        print('\n')