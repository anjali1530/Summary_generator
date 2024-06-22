from heapq import nlargest
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
text="""The giraffe is a large African hoofed mammal belonging to the genus Giraffa. 
It is the tallest living terrestrial animal and the largest ruminant on Earth. Traditionally,
giraffes have been thought of as one species, Giraffa camelopardalis, with nine subspecies.
Most recently, researchers proposed dividing them into four extant species due to new research into 
their mitochondrial and nuclear DNA, and individual species can be distinguished by their fur coat patterns. 
Seven other extinct species of Giraffa are known from the fossil record.

The giraffe's chief distinguishing characteristics are its extremely long neck and legs, its horn-like ossicones, 
and its spotted coat patterns. It is classified under the family Giraffidae, along with its closest extant relative, 
the okapi. Its scattered range extends from Chad in the north to South Africa in the south, and from Niger in the west 
to Somalia in the east. Giraffes usually inhabit savannahs and woodlands. Their food source is leaves, fruits, and flowers
of woody plants, primarily acacia species, which they browse at heights most other herbivores cannot reach."""

def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)
    nlp=spacy.load('en_core_web_sm')
    doc=nlp(rawdocs)
    #print(doc)
    tokens=[tokens.text for tokens in doc]
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1   
    #print(word_freq) 
    max_freq=max(word_freq.values())  
    #print(max_freq) 
    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq
    #print(word_freq)  
    sent_tokens=[sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores ={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]    
    #print(sent_scores)
    select_len=int(len(sent_tokens)*0.3)
    print(select_len)
    summary= nlargest(select_len,sent_scores,key=sent_scores.get)
    #print(summary)
    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
    # print(text)
    # print(summary)
    # print("length of original text",len(text.split(' ')))
    # print("length of summary",len(summary.split(' ')))

    return summary,doc,(len(rawdocs.split(' '))),(len(summary.split(' ')))