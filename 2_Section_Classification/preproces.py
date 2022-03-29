import re
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stopwords = stopwords.words("english")

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


def text_clean(x):
    x = str(x)
    x = x.encode('ascii', 'ignore').decode()  # remove unicode characters
    x = re.sub(r'https*\S+', ' ', x)  # remove  https links
    x = re.sub(r'http*\S+', ' ', x)  # remove http links
    # cleaning up text
    x = re.sub(r'\'\w+', '', x)  # remove ticks apostrophes and next character like Ankit's -> Ankit
    x = re.sub(r'\w*\d+\w*', '', x)  # remove alphanumeric
    x = re.sub(r'\s{2,}', ' ', x)  # more than 2 whitespaces
    x = re.sub(r'\s[^\w\s]\s', '', x)

    # x = re.sub(r'@\S', '', x) # remove mentions -> Not required here
    # x = re.sub(r'#\S+', ' ', x) # remove hashtags -> not required here
    x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x)  # remove punctuations
    x = re.sub(r'\s[a-z]\s|\s[0-9]\s', ' ', x)  # remove single letters and numbers surrounded by space

    # Lower case
    x = x.lower()  # lowercase everything

    # remove stop words
    x = ' '.join([word for word in word_tokenize(x) if word not in stopwords])

    # Lemmatization
    x = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(x)])

    # Stemming
    x = ' '.join([stemmer.stem(word) for word in word_tokenize(x)])

    return x