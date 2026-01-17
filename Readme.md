WhatsApp Chat Analyzer
A powerful tool to analyze WhatsApp chat exports, visualize activity, and perform sentiment analysis with a beautiful, modern UI.

Features
Upload and preprocess WhatsApp chat exports
Visualize message statistics (total messages, words, media, links)
Monthly and weekly activity timelines
Most active users and word clouds
Emoji analysis and most common words

# WhatsApp Chat Analyzer

A powerful tool to analyze WhatsApp chat exports, visualize activity, and perform sentiment analysis with a beautiful, modern UI.

---

## 🚀 Features

- Upload and preprocess WhatsApp chat exports
- Visualize message statistics (total messages, words, media, links)
- Monthly and weekly activity timelines
- Most active users and word clouds
- Emoji analysis and most common words
- Sentiment analysis of messages
- Search and filter messages
- Modern, customizable UI

---

##  Installation Guide

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Setup Steps

1. **Clone the repository:**
	```sh
	git clone https://github.com/yourusername/whatsapp_chat_analyser.git
	cd whatsapp_chat_analyser
	```
2. **Install required libraries:**
	```sh
	pip install -r requirements.txt
	```
	If `requirements.txt` is missing, install manually:
	```sh
	pip install streamlit matplotlib seaborn nltk pandas
	```
3. **Download NLTK data (first run only):**
	```python
	import nltk
	nltk.download('vader_lexicon')
	```
4. **Run the app:**
	```sh
	streamlit run app.py
	```

---

## Usage

### Command Line
1. Open a terminal in the project directory.
2. Run:
	```sh
	streamlit run app.py
	```
3. Open the provided local URL in your browser.

### GitHub Desktop
1. Open GitHub Desktop and clone the repository.
2. Open the project in your code editor.
3. Follow the installation steps above.

---

## Libraries Used

- [Streamlit](https://streamlit.io/) - Web app framework
- [NLTK](https://www.nltk.org/) - Natural Language Toolkit (sentiment analysis)
- [Matplotlib](https://matplotlib.org/) - Plotting library
- [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization
- [Pandas](https://pandas.pydata.org/) - Data analysis

---

## Screenshots / Demo

