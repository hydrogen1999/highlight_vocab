from flask import Flask, request, render_template, jsonify
from googletrans import Translator
import nltk
from nltk.corpus import wordnet
import re

# Khởi tạo Flask
app = Flask(__name__)
translator = Translator()

# Tải dữ liệu NLTK
nltk.download('wordnet')
nltk.download('omw-1.4')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/highlight', methods=['POST'])
def highlight():
    data = request.json
    text = data.get('text', '')
    highlighted_words = data.get('highlighted_words', [])
    show_synonyms = data.get('show_synonyms', False)

    translations = {}
    synonyms = {}

    for word in highlighted_words:
        # Dịch nghĩa
        translations[word] = translator.translate(word, src='en', dest='vi').text

        # Tìm từ đồng nghĩa nếu checkbox "Hiển thị từ đồng nghĩa" được bật
        if show_synonyms and wordnet.synsets(word):
            synonyms[word] = find_synonyms(word)
        else:
            synonyms[word] = []

    return jsonify({
        'highlighted_words': highlighted_words,
        'translations': translations,
        'synonyms': synonyms
    })

def find_synonyms(word):
    """Tìm từ đồng nghĩa cho một từ."""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

if __name__ == '__main__':
    app.run(debug=True)
