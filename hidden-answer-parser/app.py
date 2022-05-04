import json
import os
import re
import nltk
import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from nltk import FreqDist
from collections import Counter

from src.models.question import Question
from src.schemas.question import QuestionSchema

RESULTS_PATH = './no-script/'
if not RESULTS_PATH.endswith('/'):
    RESULTS_PATH += '/'

INTERESTING_PATH = './interesting/'
if not INTERESTING_PATH.endswith('/'):
    INTERESTING_PATH += '/'

post_tags = os.listdir(RESULTS_PATH)

testContent = []
interesting = []
all_posts = []
maximum = 10000
current = 0
for tag in post_tags:
    tag_path = RESULTS_PATH + tag

    all_posts_path = os.listdir(tag_path)
    for html_file in all_posts_path:
        if current >= maximum:
            break
        html_path = '{}/{}'.format(tag_path, html_file)

        with open(html_path, 'r') as html_file:
            html_lines = html_file.readlines()

        html_content = ''.join(html_lines)

        parsed_html = BeautifulSoup(html_content, 'html.parser')

        print(html_path)
        question = Question(parsed_html)
        schema = QuestionSchema()
        result = schema.dump(question)

        if not ((question.category == 'Hacking') or (question.category == 'Segurança') or (question.category == 'Programação') or (question.category == 'Deepweb') or (question.category == 'Criptomoedas') or (question.category == 'Bitcoin') or (question.category == 'Tor') or (question.category == 'Hack') or (question.category == 'Darknet') or (question.category == 'Darkweb')):
            all_posts.append(result)
            current += 1
            continue
        print('===============================================================')
        print(question.title)
        print('===============================================================')
        pprint(result)
        print('===============================================================')

        testContent.append(question.content)

        print("===============================QUESTION CONTENT===============================")
        print(question.content)

        answersResult = question.answers

        for anws in answersResult:
            resultAws = schema.dump(anws)
            contentResAns = resultAws["content"]
            print("===============================AWS CONTENT===============================")
            print(contentResAns)
            testContent.append(contentResAns)

        commentsResult = question.comments

        for cmts in commentsResult:
            resultCmts = schema.dump(cmts)
            contentResCmts = resultCmts["content"]
            print("===============================COMMENT CONTENT===============================")
            print(contentResCmts)
            testContent.append(contentResCmts)

        interesting.append(result)
        current += 1
    if current >= maximum:
        break

def RemovingStopWords(instancia):
    instancia = instancia.lower()
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    print("===============================STOP WORDS===============================")
    print(stopwords)
    palavras = [i for i in instancia.split() if not i in stopwords]
    return (" ".join(palavras))

def RemovingVerbs(instancia):
    instancia = instancia.lower()
    print("===============================VERBS WORDS===============================")
    text = open('verbos',encoding = "ISO-8859-1").read()
    palavras = [i for i in instancia.split() if not i in text]
    return (" ".join(palavras))

def RemovingCustomStopWords(instancia):
    instancia = instancia.lower()
    print("===============================VERBS WORDS===============================")
    text = open('stopwords',encoding = "ISO-8859-1").read()
    palavras = [i for i in instancia.split() if not i in text]
    return (" ".join(palavras))

nltk.download('rslp')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

resultTest = re.sub('\W+',' ', str(testContent))
resultTestWithoutXao = resultTest.replace("xa0", "")
resultTestWithoutNao = resultTestWithoutXao.replace("nao", "")
resultTestWithoutDaria = resultTestWithoutNao.replace("daria", "")
resultStopWords = RemovingStopWords(resultTestWithoutDaria)
text = RemovingVerbs(resultStopWords)
textResult = RemovingCustomStopWords(text)

print(textResult)

words = Counter()
words.update(textResult.split()) # Update counter with words
print(words.most_common())

frequencia = FreqDist(textResult.split())
palavras = frequencia.keys()
y_pos = np.arange(len(palavras))
contagem = frequencia.values()
plt.bar(y_pos, contagem, align='center', alpha=0.5)
plt.xticks(y_pos, palavras)
plt.ylabel('Frequencia')
plt.title('Frequencia das palavras nas perguntas, respostas e comentarios')
plt.show()


wordcloud = WordCloud(max_font_size=100,width = 1520, height = 535).generate(textResult)
plt.figure(figsize=(16,9))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

print(len(interesting))

if not os.path.exists(INTERESTING_PATH):
    os.makedirs(INTERESTING_PATH)

with open('{}output.json'.format(INTERESTING_PATH), 'w') as interesting_file_handler:
    json.dump(interesting, interesting_file_handler)

with open('{}general.json'.format(INTERESTING_PATH), 'w') as general_file_handler:
    json.dump(all_posts, general_file_handler)
