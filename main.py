import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

df = pd.read_excel('Input.xlsx')

for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        article_title = soup.find('h1').get_text()

        article_text = ""
        for paragraph in soup.find_all('p'):
            article_text += paragraph.get_text() + '\n'

        filename = f"{url_id}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(article_title + '\n\n')
            f.write(article_text)
        print(f"Article saved: {filename}")
    else:
        print(f"Failed to fetch URL: {url}")


import nltk
nltk.download('stopwords')
nltk.download('punkt')


import zipfile
import os

def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

extract_zip('StopWords.zip', 'StopWords')
extract_zip('MasterDictionary.zip', 'MasterDictionary')


import glob

def load_words_from_files(directory):
    words = set()
    for filepath in glob.glob(os.path.join(directory, '*.txt')):
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                words.add(line.strip().lower())
    return words

stop_words = load_words_from_files('StopWords')
positive_words = load_words_from_files('MasterDictionary/positive-words')
negative_words = load_words_from_files('MasterDictionary/negative-words')


import pandas as pd
import zipfile
import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import string

nltk.download('punkt')

def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

extract_zip('StopWords.zip', 'StopWords')
extract_zip('MasterDictionary.zip', 'MasterDictionary')

def load_words_from_files(directory):
    words = set()
    for filepath in glob.glob(os.path.join(directory, '*.txt')):
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                words.add(line.strip().lower())
    return words

stop_words = load_words_from_files('StopWords')
positive_words = load_words_from_files('MasterDictionary/positive-words')
negative_words = load_words_from_files('MasterDictionary/negative-words')

def text_analysis(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]

    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)

    sentences = sent_tokenize(text)
    avg_sentence_length = len(words) / len(sentences)
    complex_words = [word for word in words if len([char for char in word if char in 'aeiou']) > 2]
    percentage_complex_words = len(complex_words) / len(words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    avg_words_per_sentence = len(words) / len(sentences)
    complex_word_count = len(complex_words)
    word_count = len(words)
    syllable_per_word = sum([len([char for char in word if char in 'aeiou']) for word in words]) / len(words)
    personal_pronouns = sum([1 for word in words if word in ['i', 'we', 'my', 'ours', 'us']])
    avg_word_length = sum(len(word) for word in words) / len(words)

    return {
        'positive_score': positive_score,
        'negative_score': negative_score,
        'polarity_score': polarity_score,
        'subjectivity_score': subjectivity_score,
        'avg_sentence_length': avg_sentence_length,
        'percentage_complex_words': percentage_complex_words,
        'fog_index': fog_index,
        'avg_words_per_sentence': avg_words_per_sentence,
        'complex_word_count': complex_word_count,
        'word_count': word_count,
        'syllable_per_word': syllable_per_word,
        'personal_pronouns': personal_pronouns,
        'avg_word_length': avg_word_length
    }

output_df = pd.read_excel('Output Data Structure.xlsx')

results = []
for index, row in output_df.iterrows():
    url_id = row['URL_ID']
    file_path = f"{url_id}.txt"
    if os.path.exists(file_path):
        analysis_results = text_analysis(file_path)
        for key, value in analysis_results.items():
            output_df.at[index, key] = value
    else:
        print(f"File not found: {file_path}")
output_df.to_excel('Output Data Structure.xlsx', index=False)
print('Task Completed')
