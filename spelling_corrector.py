import re
from collections import Counter

# Load the words from 'big.txt' for spell correction
try:
    with open('big.txt', 'r', encoding='utf-8') as f:
        WORDS = Counter(re.findall(r'\w+', f.read().lower()))
except FileNotFoundError:
    raise FileNotFoundError("The 'big.txt' file was not found. Please ensure it exists in the project directory.")

# Function to calculate the probability of a word
def P(word, N=sum(WORDS.values())):
    return WORDS[word] / N

# Function to generate correction candidates
def correction(word):
    return max(candidates(word), key=P)

# Function to generate possible spelling corrections for a word
def candidates(word):
    return known([word]) or known(edits1(word)) or [word]

# Function to return the subset of words that are actually in the dictionary
def known(words_set):
    return set(w for w in words_set if w in WORDS)

# Function to generate edits that are one edit away from the input word
def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces   = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts    = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

# Function to generate edits that are two edits away from the input word
def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# Export the correct_spelling function for use in app.py
def correct_spelling(text):
    # Tokenize the text while preserving punctuation
    tokens = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)
    corrected_tokens = []
    
    for token in tokens:
        # Check if the token is a word
        if re.match(r'\w+', token):
            corrected_word = correction(token.lower())
            # Preserve the original casing
            if token.istitle():
                corrected_word = corrected_word.capitalize()
            elif token.isupper():
                corrected_word = corrected_word.upper()
            corrected_tokens.append(corrected_word)
        else:
            # If it's punctuation, keep it as is
            corrected_tokens.append(token)
    
    # Join tokens and fix spacing around punctuation
    corrected_text = ' '.join(corrected_tokens)
    corrected_text = re.sub(r'\s([?.!,"](?:\s|$))', r'\1', corrected_text)  # Fix spaces before punctuation
    
    return corrected_text
