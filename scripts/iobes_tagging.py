'''
Generate IOBES tagging scheme
'''

__author__ = "Irene Perez-Diez"

# Generic/Built-in
import os
import re
import argparse

def iobes_tagging(phrase):
    regexTag = re.compile(r"(\<(?P<tag>.+?)(?<!\/)\>)(?P<content>.+?)(\<\/(.+?)\>)")
    words = phrase.strip().split()
    check = ["O"]
    write = {
        "tags" : [],
        "text" : []
    }

    for j in range(len(words)):
        match = regexTag.search(words[j])
        if match:
            tag = match.group("tag")
            content = match.group("content")
            try:
                nextMatch = regexTag.search(words[j+1])
                nextTag = nextMatch.group("tag")
            except:
                nextTag = False
            if check[j] == tag:
                if nextTag == tag:
                    write["tags"].append("I-"+tag)
                else:
                    write["tags"].append("E-"+tag)
            else:
                if nextTag == tag:
                    write["tags"].append("B-"+tag)
                else:
                    write["tags"].append("S-"+tag)
            write["text"].append(content)
            check.append(tag)
        else:
            write["tags"].append("O")
            write["text"].append(words[j])
            check.append("O")
    return write



def main(input_dir, output_dir):
    files = os.listdir(input_dir)
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        # directory already exists
        pass
    for doc in files:
        with open(os.path.sep.join([input_dir, doc]), "r") as f:
            structural_report = f.readlines()
        name = doc.split(".")[0]
        for phrase in structural_report:
            result = iobes_tagging(phrase)
            with open(os.path.sep.join([output_dir, name + ".tags.txt"]), "a") as wf:
                for item in result["tags"]:
                    wf.write("%s " % item)
                if len(result["tags"]) != 0:
                    wf.write("\n")
            with open(os.path.sep.join([output_dir, name + ".words.txt"]), "a") as wf:
                for item in result["text"]:
                    wf.write("%s " % item)
                if len(result["text"]) != 0:
                    wf.write("\n")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputdir',  type=str ,default='../data/sr', help='Directory with the files to alter')
    parser.add_argument('-o', '--outputdir',  type=str, default='../data/tf_ner', help='Output directory')

    args = parser.parse_args()

    main(
        input_dir=args.inputdir,
        output_dir=args.outputdir,
        )