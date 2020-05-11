#!/usr/bin/env python
# coding: utf-8
"""
Python 3

Evaluate a spaCy model with a ground truth formatted file.
"""
__author__ = "Raul Perez-Moraga"
import spacy
import argparse
import re

def load_SRs_file(path):
    """
    Load a SRs file from a txt file and create a list, where each item of the list is a record

    inputs: 
    path[string]: path of the txt file

    outputs: 
    reportlist[list]: list of records
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
    inputs: SRlist [list]: A list of SR
    
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
    #Remove labels
    if None is not re.search(all_regexp, finaltraing):
        for label in label_list:
            finaltraing = re.sub("\<"+label+"\>|\<\/"+label+"\>","", finaltraing)
    return finaltraing

def main(groundtruth, modelspacy, labellist):
    model= spacy.load(modelspacy)
    sr_ground = load_SRs_file(groundtruth)
    sr_ground_string = eval(spacy_format(sr_ground, labellist))
    train = model.evaluate(sr_ground_string)
    print(train.scores)
    


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-gf','--groundtruth', type=str, default= '../data/sr/testa.txt',help = 'Path of the ground truth file')
    parser.add_argument('-ms','--modelspacy', type=str, default='../data/models/example_model/model-best', help = 'Directory of the spaCy model')
    parser.add_argument('-ll','--labellist', type=list, default=["FECHA", "INST","CAB","NUM","LOC","DIR","NAME"], help = 'NERs to use in the model')

    args = parser.parse_args()
    
    
    main(
        groundtruth = args.groundtruth,
        modelspacy = args.modelspacy,
        labellist = args.labellist
    )

