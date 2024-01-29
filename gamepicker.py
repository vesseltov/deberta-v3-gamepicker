from transformers import pipeline
from urllib.request import urlopen
import json
import re

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

# function by c24b on StackOverflow
# https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

# https://huggingface.co/facebook/bart-large-cnn
summary_model = pipeline("summarization", model="facebook/bart-large-cnn")
# https://huggingface.co/timpal0l/mdeberta-v3-base-squad2
qa_model = pipeline("question-answering", "timpal0l/mdeberta-v3-base-squad2")

# get json data from game 1 and 2
with urlopen("https://store.steampowered.com/api/appdetails?appids=220") as url:
    game1_data = json.load(url)['220']['data']

with urlopen("https://store.steampowered.com/api/appdetails?appids=1091500") as url:
    game2_data = json.load(url)['1091500']['data']

# get summaries
game1_summary = summary_model(cleanhtml(game1_data['detailed_description']), max_length=300, min_length=50, do_sample=False)[0]['summary_text']
game2_summary = summary_model(cleanhtml(game2_data['detailed_description']), max_length=300, min_length=50, do_sample=False)[0]['summary_text']
print("Summaries complete. Analyzing answer...")

# ask question
print(qa_model(question = "What game sounds more interesting, {0} or {1}?".format(game1_data['name'],game2_data['name']),
               context = "The description for {0} reads: '{1}' The description for {2} reads '{3}'".format(game1_data['name'],game1_summary,game2_data['name'],game2_summary)
               )['answer']
)