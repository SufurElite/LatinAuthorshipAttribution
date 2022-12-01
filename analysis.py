#!/usr/bin/env python
# coding: utf-8

# # Latin Authorship Attribution
# <hr>
# This is the notebook for Rufus Behr's CS4040 Mini-Project
# 

# ### Module Imports

# In[1]:


import numpy as np
import plot
from Data import dataExp
#get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import pyplot as plt
import LatinBERT
from LatinBERT.gen_berts import LatinBERT
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=UserWarning)
    from cltk.tokenizers.lat.lat import LatinWordTokenizer as WordTokenizer
    from cltk.tokenizers.lat.lat import LatinPunktSentenceTokenizer as SentenceTokenizer
from cltk.embeddings.embeddings import Word2VecEmbeddings as W2VE
import pickle

# ## Data Preprocessing:
# The data has already been preprocessed and stored in the corpus.pickle file.
# text_corpus.pickle contains a plaintext version of the corpus, as for the semantic embeddings further tokenization will either not take place (as is the case for Word2Vec) or happens within the model (as is the case for LatinBERT)

# In[2]:


CI = dataExp.CorpusInterface(corpus_name="text_corpus.pickle", shouldTokenize = False)
preprocessed_CI = dataExp.CorpusInterface(corpus_name="corpus.pickle", shouldTokenize = True)


# ### Initial Data Exploratory Analysis

# In[3]:


topAuthorsByTextLength, authors = plot.author_text_length_plot(preprocessed_CI, n_authors=50)
topAuthorsByWorkCount = plot.author_work_count_plot(preprocessed_CI, n_authors=50)
plot.author_lexical_diversity_plot(preprocessed_CI, authors)


# ## Experiments
# Research Questions
# 1. Are the styles of the Latin texts distinct enough to accurately classify by author? Additionally, how do the varying embeddings, both word and lemma, compare in encoding the semantic relation between documents to perform this task?
# 2. Is it possible to identify the most important stylometric features for authorship attribution? If so, what are they?
# 
# <hr> 
# 
# ### Semantic 
# 
# To address the first research question ....
# 
# Let's load in our 2 models
# 

# In[3]:


tokenizerPath = 'LatinBERT/latin.subword.encoder'
bertPath = 'LatinBERT/latin_bert/'
lat_bert = LatinBERT(tokenizerPath=tokenizerPath, bertPath=bertPath)

w2v = W2VE("lat")
# will be necessary for the word2vec tokenizer
st = SentenceTokenizer()
wt = WordTokenizer()


# Before using word2vec's model, let's write a function that performs the equivalent of get_berts in gen_berts for CLTK's word2vec model.
# The main difference is that in our retrieval of embeddings and authors instead of returning a list of of size 2 of respective embeddings and authors it returns a list the size of the sentences where each i details the sentence and the author as a list pair.

# In[28]:


def get_word2vec_encodings(input_sents, authors):
    all_sents = []
    for i in range(len(input_sents)):
        sents = st.tokenize(input_sents[i])
        for sent in sents:
            encoded_sent = []
            words = wt.tokenize(sent)
            for word in words:
                encoded_word = w2v.get_word_vector(word)
                if encoded_word is not None:
                    encoded_sent.append((word, encoded_word))
            all_sents.append([encoded_sent, authors[i]])
    return all_sents


# Let's now load in our desired data, currently I'm just looking at the top 50 (in terms of characters in text) authors.

# In[26]:


initial_texts, initial_authors = CI.get_data()
texts = []
authors = []
for i in range(len(initial_texts)):
    for j in range(len(initial_texts[i])):
        texts.append(initial_texts[i][j][0])
        authors.append(initial_authors[i])


# And now we can create the sentence embeddings for both LatinBERT and word2vec

# In[ ]:


bert_embedded_sents = lat_bert.get_berts(texts, authors)
word2vec_embedded_sents = get_word2vec_encodings(texts, authors)
with open("bert_embedded_sents", "wb") as f:
    pickle.dump(bert_embedded_sents, f)
with open("word2vec_sents", "wb") as f:
    pickle.dump(word2vec_embedded_sents, f)

# In[ ]:




