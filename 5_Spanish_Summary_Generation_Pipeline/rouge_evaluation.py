from rouge_score import rouge_scorer
import os


def get_rouge_scores(system_summary_dir, gold_summary_dir):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2'])
    rouge_scores = {}
    rouge_scores['rouge-1'] = {}
    rouge_scores['rouge-2'] = {}

    rouge_scores['rouge-1']['p'] = 0
    rouge_scores['rouge-1']['r'] = 0
    rouge_scores['rouge-1']['f'] = 0
    rouge_scores['rouge-2']['p'] = 0
    rouge_scores['rouge-2']['r'] = 0
    rouge_scores['rouge-2']['f'] = 0
    num_file = 0

    for file in os.listdir(system_summary_dir):
        try:
            if num_file % 50 == 0:
                print("Processing File Number: ", num_file)
            file_id = file.split('_')[0]
            if ".DS_Store" in file:
                continue

            with open(os.path.join(system_summary_dir, file), "r", encoding='utf-8') as f:
                system_summary_txt = f.read()

            sum_rouge_scores = {}
            sum_rouge_scores['rouge-1'] = {}
            sum_rouge_scores['rouge-2'] = {}

            sum_rouge_scores['rouge-1']['p'] = 0
            sum_rouge_scores['rouge-1']['r'] = 0
            sum_rouge_scores['rouge-1']['f'] = 0
            sum_rouge_scores['rouge-2']['p'] = 0
            sum_rouge_scores['rouge-2']['r'] = 0
            sum_rouge_scores['rouge-2']['f'] = 0
            num_sum_file = 0
            for sum_file in os.listdir(gold_summary_dir):
                if ".DS_Store" in file:
                    continue
                if os.path.isfile(os.path.join(gold_summary_dir, sum_file)) and file_id == sum_file.split("_")[0]:
                    with open(os.path.join(gold_summary_dir, sum_file), "r", encoding='utf-8') as f:
                        gold_sum_txt = f.read()
                        sum_scores = scorer.score(gold_sum_txt, system_summary_txt)
                        sum_rouge_scores['rouge-1']['p'] = sum_rouge_scores['rouge-1']['p'] + sum_scores['rouge1'][0]
                        sum_rouge_scores['rouge-1']['r'] = sum_rouge_scores['rouge-1']['r'] + sum_scores['rouge1'][1]
                        sum_rouge_scores['rouge-1']['f'] = sum_rouge_scores['rouge-1']['f'] + sum_scores['rouge1'][2]
                        sum_rouge_scores['rouge-2']['p'] = sum_rouge_scores['rouge-2']['p'] + sum_scores['rouge2'][0]
                        sum_rouge_scores['rouge-2']['r'] = sum_rouge_scores['rouge-2']['r'] + sum_scores['rouge2'][1]
                        sum_rouge_scores['rouge-2']['f'] = sum_rouge_scores['rouge-2']['f'] + sum_scores['rouge2'][2]
                        num_sum_file = num_sum_file + 1

            if num_sum_file > 0:
                sum_rouge_scores['rouge-1']['p'] = sum_rouge_scores['rouge-1']['p'] / (num_sum_file)
                sum_rouge_scores['rouge-1']['r'] = sum_rouge_scores['rouge-1']['r'] / (num_sum_file)
                sum_rouge_scores['rouge-1']['f'] = sum_rouge_scores['rouge-1']['f'] / (num_sum_file)
                sum_rouge_scores['rouge-2']['p'] = sum_rouge_scores['rouge-2']['p'] / (num_sum_file)
                sum_rouge_scores['rouge-2']['r'] = sum_rouge_scores['rouge-2']['r'] / (num_sum_file)
                sum_rouge_scores['rouge-2']['f'] = sum_rouge_scores['rouge-2']['f'] / (num_sum_file)

            rouge_scores['rouge-1']['p'] = rouge_scores['rouge-1']['p'] + sum_rouge_scores['rouge-1']['p']
            rouge_scores['rouge-1']['r'] = rouge_scores['rouge-1']['r'] + sum_rouge_scores['rouge-1']['r']
            rouge_scores['rouge-1']['f'] = rouge_scores['rouge-1']['f'] + sum_rouge_scores['rouge-1']['f']
            rouge_scores['rouge-2']['p'] = rouge_scores['rouge-2']['p'] + sum_rouge_scores['rouge-2']['p']
            rouge_scores['rouge-2']['r'] = rouge_scores['rouge-2']['r'] + sum_rouge_scores['rouge-2']['r']
            rouge_scores['rouge-2']['f'] = rouge_scores['rouge-2']['f'] + sum_rouge_scores['rouge-2']['f']

            num_file = num_file + 1


        except Exception as e:
            print(e)
            pass

    print('Number of files processed: ', num_file)
    rouge_scores['rouge-1']['p'] = rouge_scores['rouge-1']['p'] / (num_file)
    rouge_scores['rouge-1']['r'] = rouge_scores['rouge-1']['r'] / (num_file)
    rouge_scores['rouge-1']['f'] = rouge_scores['rouge-1']['f'] / (num_file)
    rouge_scores['rouge-2']['p'] = rouge_scores['rouge-2']['p'] / (num_file)
    rouge_scores['rouge-2']['r'] = rouge_scores['rouge-2']['r'] / (num_file)
    rouge_scores['rouge-2']['f'] = rouge_scores['rouge-2']['f'] / (num_file)

    return rouge_scores