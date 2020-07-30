
import re
import spacy

def spaCy_to_html(model, sr):
    """
    Format a text in free format to HTML NERs labels detected by the spaCy model:
    Inputs:
        model: spacy NER model previously loaded.
        sr: structural report to be formated.
    outpus:
        srtext: strucutral report in HTML format.
    """
    endstring = ""
    removecounter = 0
    for srtext in sr.split("\n"):
        srtext = srtext.strip()
        doc = model(srtext)
        count = 0
        counter = 0
        if doc.ents != ():
            for ent in doc.ents:
                #Labeling
                if count == 0:
                    counter = len("<"+ent.label_ +">"+"<" + ent.label_  + "/>")
                    srtext = srtext[:ent.start_char] + "<"+ ent.label_  +">" + ent.text + "</" + ent.label_  + ">" + srtext[(ent.end_char):] 

                elif count >= 1:
                    oldcounter = counter
                    counter = counter + len("<"+ent.label_ +"><"+ent.label_ +"/>")
                    srtext = srtext[:(ent.start_char+oldcounter)] + "<"+ ent.label_  +">" + ent.text + "</" + ent.label_  + ">" + srtext[(ent.end_char+oldcounter):] 
                count = count + 1
              
                
            endstring = endstring + srtext
        else:
             endstring = endstring + srtext
        endstring = endstring + "\n"

    return endstring[:-2]

def main(model_dir, input, output):
    module_load = spacy.load(model_dir)
    f = open(input, "r")
    text = f.read()
    text = spaCy_to_html(module_load, text)
    fw = open(output, "w+")
    with open(output, 'a') as the_file:
        the_file.write(text)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-md', '--modeldir',  type = str ,default='../data/models/example_model', help='Path of the directory with the spaCy model')
    parser.add_argument('-in', '--input',  type = str, default='../data/text_to_html/text_no_labels.txt', help='Path of the file to formart')
    parser.add_argument('-out', '--output',  type = str, default='../data/text_to_html/text_html_labels.txt', help='Path of the output file')
    args = parser.parse_args()

    main(model_dir=args.modeldir, input=args.input, output=args.output)