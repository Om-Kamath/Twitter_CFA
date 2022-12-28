import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import pandas as pd

# spacy.cli.download("en_core_web_lg") #download the model only once
nlp = spacy.load("en_core_web_lg")


def chunking(df):
    
    df = df['Tweet']
    all_sentences = []

    #sentence tokenization
    for sentence in df:
        all_sentences.append(sentence)


    #lemmatization
    lemma=[]
    for line in all_sentences:
        line = re.sub(r'[^\w\s]', '', line)
        if line !='':
            doc = nlp(line.lstrip().lower())
            for token in doc:
                lemma.append(token.lemma_)

    #Removing all stopwords
    lemma2 = []
    custom_stop_words = ['please','try','vfs','day','need','hi','apply','visa',' ']

    for word in lemma:
        if word not in custom_stop_words:
            lexeme = nlp.vocab[word]
            if lexeme.is_stop==False:
                lemma2.append(word)

    df2 = pd.DataFrame(lemma2)

    searchfor = ["urgent","help"]
    df2 = df2[df2[0].str.contains('|'.join(searchfor)) == False]
    df2 = df2.value_counts().rename_axis('_id').reset_index(name='counts')

    return df2

