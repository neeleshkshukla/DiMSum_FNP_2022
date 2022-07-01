# DiMSum FNS2022
DiMSum at FNS 2022 Task Repo

This repo has been created to work on the task FNS 2022 http://wp.lancs.ac.uk/cfie/fns2022/ for the paper:

DiMSum: Distributed and Multilingual Summarization of Financial Narratives; Neelesh K Shukla, Amit Vaid, Raghu C Katikeri, Sangeeth Keeriyadath, Msp Raja; Proceedings of the The 4th Financial Narrative Processing Workshop @LREC2022 pp 65-72 [Paper] http://www.lrec-conf.org/proceedings/lrec2022/workshops/FNP/pdf/2022.fnp-1.9.pdf

Please cite us:

@InProceedings{shukla-EtAl:2022:FNP,
  author    = {Shukla, Neelesh  and  Vaid, Amit  and  Katikeri, Raghu  and  Keeriyadath, Sangeeth  and  Raja, Msp},
  title     = {DiMSum: Distributed and Multilingual Summarization of Financial Narratives},
  booktitle      = {Proceedings of the The 4th Financial Narrative Processing Workshop @LREC2022},
  month          = {June},
  year           = {2022},
  address        = {Marseille, France},
  publisher      = {European Language Resources Association},
  pages     = {65--72},
  abstract  = {This paper was submitted for Financial Narrative Summarization (FNS) task in FNP-2022 workshop. The objective of the task was to generate not more than 1000 words summaries for the annual financial reports written in English, Spanish and Greek languages. The central idea of this paper is to demonstrate automatic ways of identifying key narrative sections and their contributions towards generating summaries of financial reports. We have observed a few limitations in the previous works: First, the complete report was being considered for summary generation instead of key narrative sections. Second, many of the works followed manual or heuristic-based techniques to identify narrative sections. Third, sentences from key narrative sections were abruptly dropped to limit the summary to the desired length. To overcome these shortcomings, we introduced a novel approach to automatically learn key narrative sections and their weighted contributions to the reports. Since the summaries may come from various parts of the reports, the summary generation process was distributed amongst the key narrative sections based on the weights identified, later combined to have an overall summary. We also showcased that our approach is adaptive to various report formats and languages.},
  url       = {https://aclanthology.org/2022.fnp-1.9}
}

## Task Introduction

The volume of available financial information is increasing sharply and therefore the study of NLP methods that automatically summarise content has grown rapidly into a major research area.

The Financial Narrative Summarisation (FNS 2022) aims to demonstrate the value and challenges of applying automatic text summarisation to financial text written in English, Spanish and Greek, usually referred to as financial narrative disclosures. The task dataset has been extracted from UK annual reports published in PDF file format.

The participants are asked to provide structured single summaries, based on real-world, publicly available financial annual reports of UK firms by extracting information from different key sections. Participants will be asked to generate summaries that reflects the analysis and assessment of the financial trend of the business over the past year, as provided by annual reports.

## Summaries Evaluation

For the evaluation we aim to use the Rouge Java package.

ROUGE 2 will be the main metric for teams and submission comparisons (Ranking). Teams will be ranked according to the highest F1-Score on the Test set.


