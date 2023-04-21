import pandas as pd
import nltk
from nltk import tokenize
nltk.download('punkt')
import requests
import time
from pprint import pprint
import os

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

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


for file in os.listdir('/workspace/WebStack/Sentence_Simialrity/data'):
    PATH = os.path.join('/workspace/WebStack/Sentence_Simialrity/data', file)

    source_sentence = []
    talent_list = []
    weights = []


    jtbd = pd.read_excel(PATH, sheet_name="jtbd")
    for i in jtbd['jtbd']:
        weight = jtbd[jtbd['jtbd'] == i]['weight'].tolist()
        for j in i.split(u'•'):
            if len(j.split(' ')) > 5:
                source_sentence.append(j)
                weights.append(weight)
            

    weight_mapper = {source_sentence[i]: weights[i][0] for i in range(len(source_sentence))}

    talent = pd.read_excel(PATH, sheet_name="resume")
    text = str(talent[0][0])

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




    main = pd.DataFrame()	
    for sentence in source_sentence:
        output = query({
            "inputs": {
                "source_sentence": sentence,
                "sentences": talent_list
            },
        })
        df = pd.DataFrame(list(zip(talent_list, output)), columns=['talent', 'score'])
        #df = df[df['score'] == max(df['score'])]
        df['sentence'] = sentence
        #print(df.sort_values(by=['score'], ascending=False))
        df = df[df['score'] > 0.4]
        df['weight'] = weight_mapper[sentence]
        df['main_score'] = (df['score'].max()) / 0.7
        df['interim_score'] = df['main_score'] * df['weight']
        
        main = main._append(df)
        
    main_scores = main.groupby('weight', as_index=False)['interim_score'].mean()
    main = main.merge(main_scores, on='weight', how='left')
    main['talent_score'] = main_scores['interim_score'].sum()
    #main_scores.to_excel('main_s.xlsx')
    main.to_excel(f'{file.split(".")}_scores.xlsx')