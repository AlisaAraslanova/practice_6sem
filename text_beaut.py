import nltk
from nltk.tokenize import sent_tokenize
import re

nltk.download('punkt')

def detect_language(sentence):
    """
    Простейшая эвристика: определение языка по алфавиту.
    """
    if re.search(r'[а-яА-ЯёЁ]', sentence):
        return 'russian'
    elif re.search(r'[a-zA-Z]', sentence):
        return 'english'
    elif re.search(r'[áéíóúñüÁÉÍÓÚÑÜ]', sentence):  # Испанские символы
        return 'spanish'
    else:
        return 'english'  # По умолчанию

def multilingual_sent_tokenize(text):
    # Грубая разбивка по знакам окончания предложений
    rough_sentences = re.split(r'(?<=[.!?])\s+(?=\S)', text)

    final_sentences = []
    for chunk in rough_sentences:
        lang = detect_language(chunk)
        try:
            sentences = sent_tokenize(chunk, language=lang)
        except LookupError:
            sentences = [chunk.strip()]
        final_sentences.extend(sentences)

    return [s.strip() for s in final_sentences if s.strip()]

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()

    sentences = multilingual_sent_tokenize(text)

    with open(output_path, 'w', encoding='utf-8') as file:
        for sentence in sentences:
            file.write(sentence + '\n')

# Пример использования
process_file('texts.txt', 'new_texts.txt')
