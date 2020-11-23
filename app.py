from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request,session, abort
import os



app = Flask(__name__)
# Sumy Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
# Sumy 
def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result
# NLTK
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq  

# Sumy
def nltk_summarizer(raw_text):
	stopWords = set(stopwords.words("english"))
	word_frequencies = {}  
	for word in nltk.word_tokenize(raw_text):  
	    if word not in stopWords:
	        if word not in word_frequencies.keys():
	            word_frequencies[word] = 1
	        else:
	            word_frequencies[word] += 1

	maximum_frequncy = max(word_frequencies.values())

	for word in word_frequencies.keys():  
	    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

	sentence_list = nltk.sent_tokenize(raw_text)
	sentence_scores = {}  
	for sent in sentence_list:  
	    for word in nltk.word_tokenize(sent.lower()):
	        if word in word_frequencies.keys():
	            if len(sent.split(' ')) < 30:
	                if sent not in sentence_scores.keys():
	                    sentence_scores[sent] = word_frequencies[word]
	                else:
	                    sentence_scores[sent] += word_frequencies[word]



	summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

	summary = ' '.join(summary_sentences)  
	return summary



@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

	if request.form['password'] == 'password' and request.form['username'] == 'admin':
		session['logged_in'] = True
	else:
		flash('wrong password!')
		return home()
@app.route('/analyze',methods=['GET','POST'])	
def analyze():
    if request.method == 'POST':
    	rawtext = request.form['rawtext']
        if request.form['algorithm'] == 'Sumy':
        	final_summary = sumy_summary(rawtext)
			return render_template('index.html',ctext=rawtext,final_summary=final_summary)
        else request.form['algorithm'] == 'NLTK':
        	final_summary = nltk_summarizer(rawtext)
			return render_template('index.html',ctext=rawtext,final_summary=final_summary)



if __name__ == '__main__':
	app.run(debug=True)
