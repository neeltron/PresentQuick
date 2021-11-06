from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import nltk
from flask import Flask, render_template, request

nltk.download('stopwords')
def read_full_text(text):
  td = text.splitlines()
  full_text = td[0].split(".")
  txt_arr = []
  for txt in full_text:
    # print(txt)
    txt_arr.append(txt.replace("[^a-zA-Z]", " ").split(" "))
  txt_arr.pop()
  return txt_arr

def txt_similarity(sent1, sent2, stopwords=None):
  if stopwords is None:
    stopwords = []
 
  sent1 = [w.lower() for w in sent1]
  sent2 = [w.lower() for w in sent2]
  all_words = list(set(sent1 + sent2))
  vector1 = [0] * len(all_words)
  vector2 = [0] * len(all_words)
  for w in sent1:
    if w in stopwords:
      continue
    vector1[all_words.index(w)] += 1

  for w in sent2:
    if w in stopwords:
      continue
    vector2[all_words.index(w)] += 1
  return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(txt_arr, stop_words):
  similarity_matrix = np.zeros((len(txt_arr), len(txt_arr)))
  for idx1 in range(len(txt_arr)):
    for idx2 in range(len(txt_arr)):
      if idx1 == idx2:
        continue 
      similarity_matrix[idx1][idx2] = txt_similarity(txt_arr[idx1], txt_arr[idx2], stop_words)

  return similarity_matrix


def generate_summary(text, top_n=5):
  stop_words = stopwords.words('english')
  summarize_text = []
  txt_arr =  read_full_text(text)
  txt_similarity_martix = build_similarity_matrix(txt_arr, stop_words)
  txt_similarity_graph = nx.from_numpy_array(txt_similarity_martix)
  scores = nx.pagerank(txt_similarity_graph, max_iter = 1000000)
  ranked_txt = sorted(((scores[i],s) for i,s in enumerate(txt_arr)), reverse=True)   
  for i in range(top_n):
    summarize_text.append(" ".join(ranked_txt[i][1]))
  summ =  ". ".join(summarize_text)
  return summ

app = Flask('app', template_folder = "templates", static_folder = "static")

@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/try')
def longText():
  return render_template('tryitout.html')

@app.route('/try', methods = ['POST'])
def process():
  title = request.form['title']
  presenter = request.form['presenter']
  back = request.form['back']
  intro = request.form['intro']
  literature = request.form['literature']
  method = request.form['method']
  result = request.form['result']
  conc = request.form['conc']
  ack = request.form['ack']
  cite = request.form['cite']
  end = request.form['end']
  return render_template('tryitout.html')

app.run(host='0.0.0.0', port=8080)
