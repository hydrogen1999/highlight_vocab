from flask import Flask, request, render_template
import re
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

def extract_and_translate(text):
    # Tách từ và loại bỏ dấu câu
    words = re.findall(r'\b\w+\b', text)
    unique_words = sorted(set(words))

    # Dịch từ sang tiếng Việt
    translations = {word: translator.translate(word, src='en', dest='vi').text for word in unique_words}
    return translations

@app.route('/', methods=['GET', 'POST'])
def index():
    highlighted_text = ""
    translations = {}

    if request.method == 'POST':
        text = request.form['text']
        translations = extract_and_translate(text)

        # Highlight từ trong đoạn văn
        highlighted_text = text
        for word in translations.keys():
            highlighted_text = re.sub(rf'\b{word}\b', f'<span class="highlight">{word}</span>', highlighted_text)

    return render_template('index.html', highlighted_text=highlighted_text, translations=translations)

if __name__ == '__main__':
    app.run(debug=True)