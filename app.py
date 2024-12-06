from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import PyPDF2
from gramformer import Gramformer
import torch
import spacy
from spelling_corrector import correct_spelling
import re
import matplotlib.pyplot as plt
import os
import time

app = Flask(__name__)
CORS(app)

# Initialize models
gf = Gramformer(models=1, use_gpu=torch.cuda.is_available())
nlp = spacy.load("en_core_web_sm")

# Directory for generated files
GENERATED_FILES_DIR = "generated_reports"
os.makedirs(GENERATED_FILES_DIR, exist_ok=True)

def cleanup_generated_files():
    """Remove old files from the generated files directory."""
    for file in os.listdir(GENERATED_FILES_DIR):
        file_path = os.path.join(GENERATED_FILES_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def fix_contractions(text):
    contractions = {
        "dont": "don't",
        "its": "it's",
        "im": "I'm",
        # Add more as needed
    }
    pattern = re.compile(r'\b(' + '|'.join(contractions.keys()) + r')\b')
    return pattern.sub(lambda x: contractions[x.group()], text)

def correct_grammar(sentence):
    corrected_result = gf.correct(sentence)
    if corrected_result:
        return list(corrected_result)[0]
    return sentence

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/correct_text', methods=['POST'])
def correct_text():
    cleanup_generated_files()

    text = request.form.get('text', '')
    pdf = request.files.get('pdf')
    grammar_count, spelling_count, punctuation_count = 0, 0, 0
    replaced_words = {"spelling": [], "grammar": []}

    if pdf:
        try:
            reader = PyPDF2.PdfReader(pdf)
            text = ' '.join(page.extract_text() for page in reader.pages)
        except Exception as e:
            return jsonify({'corrected_text': f'PDF error: {e}'}), 400

    if not text.strip():
        return jsonify({'corrected_text': 'No text found to correct'}), 400

    # Correct spelling
    original_text = text
    spelling_corrected_text = correct_spelling(text)
    for original_word, corrected_word in zip(original_text.split(), spelling_corrected_text.split()):
        if original_word.lower() != corrected_word.lower():
            replaced_words["spelling"].append((original_word, corrected_word))

    spelling_count = len(replaced_words["spelling"])

    # Grammar correction
    sentences = re.split(r'(?<=[.!?])\s+', spelling_corrected_text)
    corrected_sentences = []
    for sentence in sentences:
        original_sentence = sentence
        corrected_sentence = correct_grammar(sentence)
        if corrected_sentence != original_sentence:
            for o, c in zip(original_sentence.split(), corrected_sentence.split()):
                if o != c and (o, c) not in replaced_words["spelling"]:
                    replaced_words["grammar"].append((o, c))
        corrected_sentences.append(corrected_sentence)

    corrected_text = ' '.join(corrected_sentences)
    grammar_count = len(replaced_words["grammar"])

    # Add punctuation
    punctuation_count = corrected_text.count('.') - original_text.count('.')

    # Generate analytics chart
    timestamp = int(time.time())
    chart_path = os.path.join(GENERATED_FILES_DIR, f'analytics_chart_{timestamp}.png')
    generate_chart(grammar_count, spelling_count, punctuation_count, chart_path)

    # Save report
    report_path = os.path.join(GENERATED_FILES_DIR, f'correction_report_{timestamp}.txt')
    with open(report_path, 'w') as report_file:
        report_file.write("Correction Report\n")
        report_file.write("=================\n\n")
        report_file.write("Spelling Corrections:\n")
        for original, corrected in replaced_words["spelling"]:
            report_file.write(f"- {original} -> {corrected}\n")
        report_file.write("\nGrammar Corrections:\n")
        for original, corrected in replaced_words["grammar"]:
            report_file.write(f"- {original} -> {corrected}\n")

    return jsonify({
        'corrected_text': corrected_text,
        'stats': {
            'grammar': grammar_count,
            'spelling': spelling_count,
            'punctuation': punctuation_count
        },
        'chart': chart_path,
        'report': report_path
    })

def generate_chart(grammar_count, spelling_count, punctuation_count, file_path):
    labels = ['Grammar', 'Spelling', 'Punctuation']
    values = [grammar_count, spelling_count, punctuation_count]
    plt.figure(figsize=(6, 6))
    plt.bar(labels, values, color=['blue', 'green', 'orange'])
    plt.title('Text Correction Analytics')
    plt.xlabel('Correction Type')
    plt.ylabel('Count')
    plt.savefig(file_path)
    plt.close()

@app.route('/download_report', methods=['GET'])
def download_report():
    report_name = request.args.get('report')
    report_path = os.path.join(GENERATED_FILES_DIR, report_name)
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True)
    return jsonify({'error': 'Report not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
