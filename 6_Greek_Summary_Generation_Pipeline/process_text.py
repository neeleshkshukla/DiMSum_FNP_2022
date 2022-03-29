import re
import string
from nltk.tokenize import sent_tokenize as nltk_sent_tokenize
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from nltk.corpus import stopwords


def sent_tokenize(text):
    sents = nltk_sent_tokenize(text)
    sents_filtered = []
    for sent in sents:
        sents_filtered.append(sent)
    return sents_filtered


def clean_text(text):
    clean = text.replace('\n' ,' ')
    clean = re.sub('\\s+', ' ', text)
    clean = re.sub(r'[^\w]', ' ', clean)
    clean = clean.replace("\t" ," ").replace("\xa0" ," ")
    return clean


def clean_number(text):
    ans = ""
    for i in text:
        if not i.isdigit():
            ans += i
    return ans


def cleanup_sentences(text, lang='en'):
    if lang == 'en':
        stop_words = set(stopwords.words('english'))
    if lang == 'es':
        stop_words = set(stopwords.words('spanish'))
    if lang == 'el':
        stop_words = set(stopwords.words('greek'))
    sentences = sent_tokenize(text)
    raw_sentences = []
    sentences_cleaned = []
    for sent in sentences:
        #print(sent, '================>')
        #print('\n')
        clean = clean_number(sent)
        clean = clean_text(clean)
        words = nltk_word_tokenize(clean)
        words = [w for w in words if w not in string.punctuation]
        words = [w for w in words if not w.lower() in stop_words]
        words = [w.lower() for w in words]
        cleaned_sent = " ".join(words)
        sentences_cleaned.append(" ".join(words))
        raw_sentences.append(sent)
            #print(cleaned_sent, '================>')
            #print('\n\n')
    return raw_sentences, sentences_cleaned


def cleanup_sentence(sentence, lang='en'):
    if lang == 'en':
        stop_words = set(stopwords.words('english'))
    if lang == 'es':
        stop_words = set(stopwords.words('spanish'))
    if lang == 'el':
        stop_words = set(stopwords.words('greek'))

    sent = clean_number(sentence)
    sent = clean_text(sent)
    words = nltk_word_tokenize(sent)
    words = [w for w in words if w not in string.punctuation]
    words = [w for w in words if not w.lower() in stop_words]
    words = [w.lower() for w in words]
    cleaned_sent = " ".join(words)
    return cleaned_sent