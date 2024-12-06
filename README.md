# Grammar Auto-Corrector

## Overview
The Grammar Auto-Corrector is a web-based application that corrects grammatical errors, spelling mistakes, and punctuation issues in text or PDF files. The tool leverages state-of-the-art machine learning models and NLP techniques to improve text quality while providing insightful analytics about the corrections made.

---

## Features
- **Text Input:** Paste or type text directly into the input box for correction.
- **PDF Input:** Upload a PDF file to extract and correct its content.
- **Spelling Corrections:** Detects and corrects spelling errors.
- **Grammar Fixes:** Identifies and rectifies grammatical issues using `gramformer`.
- **Punctuation Adjustments:** Improves punctuation usage, such as commas and periods.
- **Analytics Dashboard:** Displays a bar chart summarizing the corrections made.
- **Downloadable Reports:** Generates and allows download of a detailed correction report.

---

## Technology Stack
- **Backend:** Flask, Flask-CORS
- **Frontend:** HTML, CSS, JavaScript
- **NLP Tools:**
  - Gramformer
  - SpaCy (en_core_web_sm)
- **Visualization:** Matplotlib
- **Others:** PyPDF2 for PDF handling

---

## Installation

### Prerequisites
- **Python 3.9**
- Virtual Environment (recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate   # For macOS/Linux
   env\Scripts\activate    # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the SpaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application in your browser:
   - Navigate to `http://127.0.0.1:5000/`

---

## Usage
1. Open the application in your browser.
2. Choose one of the following inputs:
   - Paste text in the input box.
   - Upload a PDF file.
3. Click the **Correct Text** button.
4. View the corrected text, analytics, and optionally download the correction report.

---

## Folder Structure
```
project-root/
|-- app.py
|-- requirements.txt
|-- templates/
|   |-- index.html
|-- static/
|   |-- css/
|   |-- js/
|-- generated_reports/
|-- spelling_corrector.py
|-- big.txt
```

---

## Future Improvements
- Integration with advanced language models like GPT-4 for improved accuracy.
- Support for multiple languages.
- Enhanced UI/UX for better user interaction.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or feature requests.

---

## Contact
For questions or suggestions, please contact:
- **Email:** [your-email@example.com]
- **GitHub:** [your-github-profile]

