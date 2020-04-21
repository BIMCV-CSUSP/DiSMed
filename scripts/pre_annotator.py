"""
Python 3

Pre-annotate reports
"""

import pandas as pd
import os
import re
import argparse
import codecs
import multiprocessing as mp
import time

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', type=str, default="../data/sr/", help="Directory where the text files are stored")
parser.add_argument('-v', '--verbose', type=bool, default=True, help="Whether to show in screen progress notes or not")
parser.add_argument('-nf', '--names', type=str, default="../data/databases/names.csv", help='Path of the file containing the name database')
parser.add_argument('-sf', '--surnames',  type=str, default='../data/databases/surnames.csv', help='Path of the file containing the surname database')
parser.add_argument('-o', '--overwrite', type=bool, default=False, help="Whether to overwrite input files or not")

args = parser.parse_args()

directory = args.directory,
verbose = args.verbose,
name_file = args.names,
surname_file = args.surnames,
ow = args.overwrite

def replace_hospitals(sr, hospital_list, verbose=True):
    """
    Replaces the hospital names or words from the structural report

    inputs:
        sr              content of the structural report 
        hospital_list   list of names of the hospitals, or list of words found in 
                        the names of the hospitals

    output:
        copy of the structural report replaced
    """

    copySr = sr
    tag = "<INST>"
    endTag = "</INST>"
    for j in range(len(copySr)):
        for hospital in hospital_list:
            p = re.compile(r"\b" + r"(?<!\>)(?!\<)" + hospital + r"\b", re.IGNORECASE)
            hospital = hospital.split()
            if len(hospital) == 1:
                copySr[j] = p.sub(tag + str(hospital[0]) + endTag, copySr[j])
            else:
                new_string = [tag + i + endTag for i in hospital]
                copySr[j] = p.sub(" ".join(new_string))
    
    return copySr

def replace_database(sr, dataBase, ignoreList = None, tag="<NAME>", endTag ="</NAME>"):
    """
    Replaces the wotds in the database from the structural report

    inputs:
        sr          content of the structural report 
        dataBase    list of words
        tag         tag used to replace

    output:
        copy of the structural report replaced
    """


    copySr = sr
    for j in range(len(copySr)):
        for word in dataBase:
            if word not in ignoreList:
                p = re.compile(r"\b" + r"(?<!\>)(?!\<)" + str(word) + r"\b", re.IGNORECASE | re.UNICODE)
                word = word.split()
                if len(word) == 1:
                    copySr[j] = p.sub(tag + str(word[0]) + endTag, copySr[j])
                else:
                    new_string = [tag + i + endTag for i in word]
                    copySr[j] = p.sub(" ".join(new_string), copySr[j])

    return copySr

def collect_results(result):
    """
    Collects results from paralelized database function
    """
    global results
    if ((result != None) and (result not in results)):
        results.append(result)


def words_to_replace(word, sr, verbose):
    try:
        p = re.compile(r"\b" + str(word).strip() + r"\b")
        ignoreWords = [
            "HOSPITAL",
            "NAME",
            "CABEZA",
            "PET", 
            "SEGA",
            "FO",
            "NACIMIENTO",
            "PER",
            "SALUT",
            "MC",
            "WILLIS",
            "AVI",
            "SWAN",
            "DADA",
            "ELA",
            "CAI",
            "CLINICO",
            "SIN", 
            "CON"
        ]
        if word.strip() in ignoreWords:
            return
        elif len(word.strip()) <= 3:
            return
        else:
            for i in sr:
                if p.search(i):
                    return word
    except AttributeError:
        if verbose:
            print("Attribute Error, trying to strip word '{}'".format(word))
        return



# Read name database
name_db = pd.read_csv(args.names)
name_db.columns = ["Nombre", "Frecuencia"]
name_db = name_db["Nombre"].values.tolist()

# Read surname database
surname_db = pd.read_csv(args.surnames)
surname_db.columns = ["Apellido", "Frecuencia"]
surname_db = surname_db["Apellido"].values.tolist()

# Set valencian region hospital words database
hospital_db = [
    "HOSPITAL CLINICO", "HOSPITAL CLÍNICO", "HOSPITAL", "HOSPITAL GENERAL",
    "VINARÓS", "VINAROS", "CASTELLON", "CASTELLÓN", "GENERAL",
    "PLANA", "SAGUNTO","VALENCIA", "VALÈNCIA",  "LA FE",
    "REQUENA", "DOCTOR PESET", "PESET", "DR. PESET", "GANDIA", "ALCOY", "ALCOI", 
    "MARINA BAIXA", "SANT JOAN", "ALACANT", "ELDA", "ALICANTE", "SAN JUAN",
    "ELCHE", "ORIHUELA", "TORREVIEJA", "MANISES", "ANTIGUO", "MILITAR",
    "VINALOPO", "VINALOPÓ", "PEDRERA", "PROVINCIAL", "CASTELLÓ", "CASTELLO",
    "MAGDALENA", "MADALENA", "MALVARROSA", "ARNAU", "VILANOVA", "LLIRIA",
    "LLÍRIA", "MOLINER", "PARE JOFRE", "JOFRE", "RIBERA", "DENIA", "XATIVA",
    "JATIVA", "XÁTIVA", "JÁTIVA", "ONTINYENT", "ONTENIENTE", "LLUIS ALCANYIS",
    "LUIS ALCAÑIZ", "SAN VICENTE", "SANT VICENT", "RASPEIG", 
]

# Set words to ignore
ignoreList = ["DE", "LA", "DEL", "LOS", "Y", "I", "A", "E", "NI", "QUE", "MAS", "SI", "SIN", "INST", "NAME"]

files = os.listdir(args.directory)

for file in files:
    # Read report file
    with codecs.open(args.directory + file, "r", encoding="ISO-8859-1") as f:
        report = f.readlines()
        
    # Tag hospital words
    if verbose:
        print("Tagging hospital words\n")
    start_time = time.time()
        
    try: 
        report = replace_database(report, hospital_db, ignoreList, tag="<INST>", endTag="</INST>")
    except re.error:
        if verbose:
            print("Regex error replacing hospital names at {}\n".format(file))
        pass

    if verbose:
        print(str(time.time() - start_time))
        middle_time = time.time()
        
    # Tag names
    if verbose:
        print("Tagging names")
    pool = mp.Pool(mp.cpu_count())
    results = []
    for j in range(len(name_db)):
        pool.apply_async(words_to_replace, args=(name_db[j], report, verbose), callback=collect_results)
    pool.close()
    pool.join()

    if verbose:
        print(results)

    try:
        report = replace_database(report, results, ignoreList)
    except re.error:
        if verbose:
            print("Regex error replacing with database at {}\n".format(file))
        pass
        
    if verbose:
        print(str(time.time() - middle_time))
    middle_time = time.time()
    # Replace surnames in surname database
    if verbose:
        print("Replacing with surname database\n") 

    pool = mp.Pool(mp.cpu_count())
    results = []
    for j in range(len(surname_db)):
        pool.apply_async(words_to_replace, args=(surname_db[j], report)) #, callback=collect_results
    pool.close()
    pool.join()
    if verbose:
        print(results)
    try:
        report = replace_database(report,results, ignoreList)
    except re.error:
        if verbose:
                print("Regex error replacing with database at {}\n".format(file))
        pass
    
if verbose:
    print(str(time.time() - middle_time))
if ow:
    outputFile = file
else:
    p = re.compile("(.*).txt")
    outputFile = p.search(file).group(1) + "_tagged.txt"

with codecs.open(args.directory + outputFile, "w", encoding="ISO-8859-1") as o:
    o.writelines(report)
    
if verbose:
    print("total time {}".format(time.time() - start_time))

