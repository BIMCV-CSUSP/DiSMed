"""
Generate html tagging scheme from IOBES
"""

__author__ = "Irene Perez-Diez"

# Generic/Built-in
import os
import argparse

def change_tags(tags, words):
    """
    Converts IOBES tagging scheme to html
    
    Inputs:
        tags    list    list with tags of len X
        words   list    list with words of len X
    
    Output:
        frase   list    list with words tagged html-like of len X
    """
    frase = []
    for i in range(len(tags)):
        if tags[i] != "O":
            tag = tags[i][2:]
            frase.append("<" + tag + ">" + words[i] + "</" + tag + ">")
        else:
            frase.append(words[i])
    return(frase)

def main(input_dir, data_subset):
    
    file_tags = data_subset + ".tags.txt"
    file_words = data_subset + ".words.txt"

    with open(input_dir + "/" + file_tags, "r") as ft:
        tags_lines = ft.readlines()
    with open(input_dir + "/" + file_words, "r") as fw:
        words_lines = fw.readlines()
    
    for j in range(len(tags_lines)):
        result = change_tags(tags_lines[j].strip().split(), words_lines[j].strip().split())
        with open(input_dir + "/" + data_subset + ".html.txt", "a") as wf:
            text = " ".join(result)
            wf.write(text)
            wf.write("\n")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--input_dir', type=str, default='../data/tf_ner', help='Directory that contains the files')
    parser.add_argument('-ds', '--data_subset', type=str, default='train', help='Data subset to change')

    args = parser.parse_args()

    main(
        input_dir = args.input_dir,
        data_subset = args.data_subset
    )