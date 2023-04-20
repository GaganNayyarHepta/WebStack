import pandas as pd
import nltk
from nltk import tokenize
nltk.download('punkt')
import requests
import time
from pprint import pprint

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
PATH = r'/workspace/WebStack/Sentence_Simialrity/data/ArunPrasad.xlsx'

source_sentence = []
talent_list = []



jtbd = pd.read_excel(PATH, sheet_name="jtbd")
for i in jtbd['jtbd']:
    for j in i.split(u'•'):
        if len(j.split(' ')) > 5:
            source_sentence.append(j)

talent = pd.read_excel(PATH, sheet_name="resume")
text = str(talent[0][0])
import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

sentence_list = split_into_sentences(text=text)

for i in sentence_list:
    if len(i) > 40:
        if '•' in i:
            for j in i.split(u'•'):
                talent_list.append(j)
        if '-' in i:
            for j in i.split('-'):
                talent_list.append(j)
        else:
            talent_list.append(i)
    else:
        talent_list.append(i)

for i in talent_list:
    if len(i) <= 10:
        talent_list.remove(i)

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


main = pd.DataFrame()	
for sentence in source_sentence:
    output = query({
        "inputs": {
            "source_sentence": sentence,
            "sentences": talent_list
        },
    })
    print(sentence)
    df = pd.DataFrame(list(zip(talent_list, output)), columns=['talent', 'score'])
    #df = df[df['score'] == max(df['score'])]
    df['sentence'] = sentence
    #print(df.sort_values(by=['score'], ascending=False))
    df = df[df['score'] > 0.4]
    
    main = main._append(df)
    
main.to_excel(f'.xlsx')