#!/usr/bin/env python
# coding: utf-8
"""
Python 3

Transform a text file to Json format to training with SPACY
"""
__author__ = "Raul Perez-Moraga"
import re
import spacy
import srsly
import argparse
import os
from spacy.gold import docs_to_json, biluo_tags_from_offsets, spans_from_biluo_tags


def load_SRs_file(path):
    """
    Load a SRs file from a txt file and create a list, where each item of the list is a SR

    inputs: 
    path[string]: path of the txt file

    outputs: 
    reportlist[list]: list of SRs
    """
    reportlist = [""]
    x = 0
    with open(path, "r") as reprotsfile:
    
        for line in reprotsfile:
            if line != "----------------------------------------------\n" and x >= 0:
                reportlist[x] = reportlist[x] + line
            elif line == "----------------------------------------------\n":
                x = x+1
                reportlist.append(line)
    return reportlist

def spacy_format(SRlist, label_list):
    """
    Use a list of tagged SR and generate a string to train/test the NER models
    inputs: 
    SRlist [list]: A list of SR
    
    outputs:
    finaltraing: A string with the required format to train a NLP model with spacy.
    """
    
    finaltraing = "["
    counterx = 0
    strintrue = False
    all_regexp = ""
    one_regexp = ""
    
    for i in label_list:
        all_regexp = "\<" + i + "\>(.\s*.*)\<\/" + i + "\>|" + all_regexp
        one_regexp = "\<" + i + "\>(.\s*.+?)\<\/" + i + "\>|" + one_regexp
    all_regexp = all_regexp[:-1]
    one_regexp = one_regexp[:-1]    
    for reportsub in SRlist:
        for stringbits in reportsub.splitlines():
            cleanstring = stringbits.strip()
            cleanstring = re.sub("'",",",cleanstring)
            if len(cleanstring) > 0:
                if cleanstring[len(cleanstring)-1] == ".":
                    cleanstring = cleanstring[0:len(cleanstring)-1]
            if None is not re.search(all_regexp, cleanstring):
                inercounter = 0
                strintrue = True
                correctiter = 1
                counter = 0
                for itering in re.finditer(one_regexp, cleanstring):
                    #Start a formated string
                    if inercounter == 0:
                        for label in label_list:
                            if None is not re.search("\<"+label+"\>", itering[0]):
                                counter = len("<"+label+"></"+label+">")
                                finaltraing = finaltraing+"('"+re.sub("\<"+label+"\>|\<\/"+label+"\>","",cleanstring)+"', {'entities':[("+ str(itering.span()[0])+","+str(itering.span()[1]-counter)+", '"+label+"')"
                                inercounter = inercounter + 1
                     #Continue formated string
                    elif inercounter >= 1:
                        for label in label_list:
                            if None is not re.search("\<"+label+"\>", itering[0]):
                                oldcounter = counter
                                counter = counter + len("<"+label+"></"+label+">")
                                finaltraing = finaltraing + ",(" + str(itering.span()[0]-oldcounter)+","+str(itering.span()[1]-counter)+ ", '"+label+"')" 
            elif "" != cleanstring:
                finaltraing = finaltraing + "('"+cleanstring + "',{'entities':["
                strintrue = True
            if strintrue == True:    
                finaltraing = finaltraing + "]}),"
                strintrue = False
                                 
    finaltraing = finaltraing + "]"
    if None is not re.search(all_regexp, finaltraing):
        for label in label_list:
            finaltraing = re.sub("\<"+label+"\>|\<\/"+label+"\>","", finaltraing)
    return finaltraing

def mkdir_p(path):
    """
    Make a directory
    input: path to create the directory

    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def main(textfile, output, dummymodel, labellist):
    #Need a dummy model to create a nlp object with the aim to transform a txt file to json
    nlp = spacy.load(dummymodel)
    sr_transfrom = load_SRs_file(textfile)

    sr_transfrom_string = eval(spacy_format(sr_transfrom, labellist))
    docs = []
    for text, annot in sr_transfrom_string:
        doc = nlp(text)
        doc.is_parsed = True
        tags = biluo_tags_from_offsets(doc, annot['entities'])
        entities = spans_from_biluo_tags(doc, tags)
        doc.ents = entities
        docs.append(doc)
    #Create the json file in the same directory that textfile
    
    mkdir_p(os.path.split(output)[0])
    srsly.write_json(output, [spacy.gold.docs_to_json(docs)])


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-txt','--textfile', type=str, default='../data/sr/train.txt', help = 'Path of the file with records to transform')
    parser.add_argument('-out','--output', type=str, default='../data/sr/srjson/train.json', help = 'Path to save the json output')
    parser.add_argument('-mn','--dummymodel', type=str, default='../data/models/dummy_model', help = 'Directory of the dummy model')
    parser.add_argument('-ll','--labellist', type=list, default=["FECHA", "INST","CAB","NUM","LOC","DIR","NAME"], help = 'NERs to use in the model')
   

    args = parser.parse_args()
    
    
    main(
        textfile = args.textfile,
        output = args.output,
        dummymodel = args.dummymodel,
        labellist = args.labellist
    )