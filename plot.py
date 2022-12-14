"""
    Utility file to plot
"""
from Data.dataExp import CorpusInterface as CI
from matplotlib import pyplot as plt 
import numpy as np
import os


"""
    These two functions can (and probably should) be rewritten as one function
"""

def author_text_length_plot(ci: CI, n_authors: int = 50, save_file: bool = False, extra_text: str = "all_data"):
    values = ci.get_authors_by_text_size()
    plt.rcParams["figure.figsize"] = (20,20)
    plt.title("Top " + str(n_authors) + " authors - " + extra_text)
    x = []
    
    for i in range(n_authors):
        x.append(values[i][0])
        plt.bar(values[i][0],values[i][1], color = ci.get_author_color(values[i][0]))
    plt.xticks(rotation='vertical')
    plt.xlabel("Authors")
    plt.ylabel("Number of words in all of author's texts")
    if save_file:
        path = os.getcwd()+"/Data/Plots/" + extra_text +" author_word_plot.png"
        plt.savefig(path)
        plt.close()
    else:
        plt.show()
    return values, x

def author_work_count_plot(ci: CI, n_authors: int = 50, save_file: bool = False, extra_text: str = "all_data"):
    values = ci.get_authors_by_text_size(characterCount=False)
    plt.rcParams["figure.figsize"] = (20,20)
    plt.title("Top " + str(n_authors) + " authors - " + extra_text)
    x = []

    for i in range(n_authors):
        x.append(values[i][0])
        plt.bar(values[i][0],values[i][1], color = ci.get_author_color(values[i][0]))
    plt.xticks(rotation='vertical')
    plt.xlabel("Authors")
    plt.ylabel("Number of works per author")
    if save_file:
        path = os.getcwd()+"/Data/Plots/" + extra_text +" author_work_count_plot.png"
        plt.savefig(path)
        plt.close()
    else:
        plt.show()
    return values

def author_lexical_diversity_plot(ci: CI, authors, save_file: bool = False, extra_text: str = "all_data"):
    values = ci.lexical_diversity(authors)
    plt.rcParams["figure.figsize"] = (20,20)
    plt.title("Top " + str(len(authors)) + " authors - " + extra_text)
    x = []
    for i in range(len(authors)):
        x.append(values[i][0])
        plt.bar(values[i][0],values[i][1], color = ci.get_author_color(authors[i]))
    plt.xticks(rotation='vertical')
    plt.xlabel("Authors")
    plt.ylabel("Lexical diversity across all of author's texts")
    if save_file:
        path = os.getcwd()+"/Data/Plots/" + extra_text +" author_lexical_diversity_plot.png"
        plt.savefig(path)
        plt.close()
    else:
        plt.show()


def all_plots(ci = None, save_files=False, n_authors:int = 25, extra_text: str = "all_data"):
    if ci is None:
        ci = CI()
    topAuthorsByTextLength, authors = author_text_length_plot(ci, n_authors, save_file = save_files, extra_text = extra_text)
    topAuthorsByWorkCount = author_work_count_plot(ci, n_authors, save_file = save_files, extra_text = extra_text)
    author_lexical_diversity_plot(ci, authors, save_file = save_files, extra_text = extra_text)
    
