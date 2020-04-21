'''
Generate a synthetic dataset from original identified data
'''

__author__ = "Irene Perez-Diez"

# Generic/Built-in
import re
import argparse
import random
import string
from datetime import date

# Other libs
import pandas as pd
from numpy.random import choice


def load_reports_file(path):
    """
    Loads radiology reports from a file. Radiology reports must be separated by
    the following string: '----------------------------------------------'

    Inputs:
        path    str     path to the file containing the reports
    
    Output:
        reportlist  list    a list with a report for each element
    """
    reportlist = [""]
    x = 0
    with open(path, "r") as reportsfile:

        for line in reportsfile:
            if "----------------------------------------------" in line:
                x = x+1
                reportlist.append("")
            else:
                reportlist[x] = reportlist[x] + line

    return reportlist


def case_pattern(content, new_word):
    """
    Determines the uppercase and lowercase pattern of a token and applies it to
    another

    Inputs:
        content     str     Token to replace
        new_word    str     New token, apply here the upper/lowercase pattern
    
    Output:
        new_word    str     New token with appropiate upper/lowercase pattern
    """
    if content.isupper():
        new_word = new_word.upper()
    elif content.islower():
        new_word = new_word.lower()
    else:
        new_word = new_word.title()
    return new_word


def replace_name(prev_tag, prev_word, content, name_db, surname_db, tag = "NAME"):
    """
    Replaces names and surnames with randomly selected ones

    Inputs:
        prev_tag        str     Named Entity (NE) tag of the previous token
        prev_word       str     Previous token
        content         str     Current token
        name_db         list    Name database
        surname_db      list    Surname database
        tag             str     Tag to attach to the new token, NAME by default
    
    Output:
        new_word        str     New token selected
    """
    # pattern for surnames
    pattern = r"apellidos?:?"
    # pattern for names
    pattern_name = r"nombre:?"
    if re.match(pattern, prev_word, re.IGNORECASE):
        new_word = choice(surname_db["Apellido"], p=surname_db["Probabilidad"]).strip()
        while re.match(new_word, content, re.IGNORECASE):
            new_word = choice(surname_db["Apellido"], p=surname_db["Probabilidad"]).strip()
            
    elif re.match(pattern_name, prev_word, re.IGNORECASE):
        new_word = choice(name_db["Nombre"], p=name_db["Probabilidad"]).strip()
        while re.match(new_word, content, re.IGNORECASE):
            new_word = choice(name_db["Nombre"], p=name_db["Probabilidad"]).strip()
            
    elif prev_tag == "NAME":
        new_word = choice(surname_db["Apellido"], p=surname_db["Probabilidad"]).strip()
        while re.match(new_word, content, re.IGNORECASE):
            new_word = choice(surname_db["Apellido"], p=surname_db["Probabilidad"]).strip()
            
    else:
        new_word = choice(name_db["Nombre"], p=name_db["Probabilidad"]).strip()
        while re.match(new_word, content, re.IGNORECASE):
            new_word = choice(name_db["Nombre"], p=name_db["Probabilidad"]).strip()
    
    new_word = case_pattern(content,new_word)
    new_word = new_word.split()
    new_word = " ".join(["<"+tag+">"+j+"</"+tag+">" for j in new_word])
    
    return new_word


def replace_date(content, month_db, tag = "FECHA"):
    """
    Replaces dates with randomly selected ones with the same formatting style

    Inputs:
        content     str     Current token
        month_db    list    Month database in spanish
        tag         str     Tag to attach to the new token, FECHA by default
    
    Output:
        new_word    str     New token selected
    """
    try:
        content = int(content)
        if content < 31:
            new_word = str(random.choice(list(range(1,32))))
        else:
            new_word = str(random.choice(list(range(1920,int(date.today().year)))))
    except:
        if re.search(r'\/', content):
            day = str(random.choice(list(range(1,32))))
            month = str(random.choice(list(range(1,13))))
            year = str(random.choice(list(range(1920,2021))))
            new_word = day + "/" + month + "/" + year
        elif re.search(r'-', content):
            day = str(random.choice(list(range(1,32))))
            month = str(random.choice(list(range(1,13))))
            year = str(random.choice(list(range(1920,2021))))
            new_word = day + "-" + month + "-" + year
        elif re.search(r'\.', content):
            day = str(random.choice(list(range(1,32))))
            month = str(random.choice(list(range(1,13))))
            year = str(random.choice(list(range(1920,2021))))
            new_word = day + "." + month + "." + year
        elif content == "de":
            new_word = content
        else:
            new_word = random.choice(month_db)
            
    new_word = case_pattern(str(content),new_word)
    new_word = "<"+tag+">"+new_word+"</"+tag+">"
    
    return new_word


def replace_loc(content, city_db, tag = "LOC"):
    """
    Replaces locations (city names) with randomly selected ones

    Inputs:
        content     str         Current token
        city_db     pandas_df   Cities database
        tag         str         Tag to attach to the new token, LOC by default
    
    Output:
        new_word    str         New token or sequence of tokens selected
    """
    new_word = choice(city_db["NOMBRE"], p=city_db["Probabilidad"]).strip()
    
    new_word = case_pattern(content,new_word)
    new_word = new_word.split()
    new_word = " ".join(["<"+tag+">"+j+"</"+tag+">" for j in new_word])
        
    return new_word


def replace_inst(content, hospital_db, hc_db, tag = "INST"):
    """
    Replaces names of hospitals with randomly selected ones

    Inputs:
        content         str     Current token
        hospital_db     list    Hospital database
        tag             str     Tag to attach to the new token, INST by default
    
    Output:
        new_word        str     New token or sequence of tokens selected
    """
    # Hospitals - Intial of "Hospital"  + name of hospital
    if content == "H.":
        hospital = random.choice(hospital_db["NOMBRE"]).strip()
        hospital = hospital.split()
        content = hospital[0][0] + "."
        hospital = hospital[1:]
        new_word = " ".join(["<"+tag+">"+j+"</"+tag+">" for j in hospital])
        new_word = " ".join(["<"+tag+">"+content+"</"+tag+">", new_word])
        # Health centers - Initials of "Centro Especialidades" + name of center
    elif content == "C.E.":
        hospital = random.choice(hc_db["NOMBRE"]).strip()
        hospital = hospital.split()
        hospital = hospital[2:]
        new_content = random.choice([content, "C.S."])
        new_word = " ".join(["<"+tag+">"+j+"</"+tag+">" for j in hospital])
        new_word = " ".join(["<"+tag+">"+new_content+"</"+tag+">", new_word])
        # Non hospital institutions are deleted
    elif content == "GENERALITAT" or content == "CONSELLERIA":
        new_word = ""
        # Hospitals or centers - full name
    else:
        hospital = random.choice(hospital_db["NOMBRE"]).strip()
        hospital = hospital.split()
        new_word = " ".join(["<"+tag+">"+j+"</"+tag+">" for j in hospital])
    
    return new_word


def replace_dir(address_db, city_db, tag_dir = "DIR", tag_city = "LOC"):
    """
    Replaces full addresses with randomly selected ones

    Inputs:
        address_db      str     Addresses database
        tag_dir         str     Tag to attach to the new direction tokens,
                                DIR by default
        tag_city        str     Tag to attach to the new city tokens,
                                LOC by default
    
    Output:
        new_word        str     New token or sequence of tokens selected
    """
    i = random.randint(0,(address_db.shape[0]-1))
    new_dir = address_db.loc[address_db.index[i],["tipo_via", "dir_via", "dir_cp"]]
    new_dir = new_dir.to_list()
    new_dir = [z for y in new_dir for z in str(y).split()]
    new_dir = " ".join(["<"+tag_dir+">"+j+"</"+tag_dir+">" for j in new_dir])
    
    new_loc = choice(city_db["NOMBRE"], p=city_db["Probabilidad"]).strip()
    new_loc = new_loc.split()
    new_loc = " ".join(["<" + tag_city + ">"+j.upper()+"</"+tag_city+">" for j in new_loc])
    
    new_word = " ".join([new_dir, new_loc])
    
    return new_word


def replace_num(content, tag = "NUM"):
    """
    Replaces numbers with randomly selected ones with the same formatting style

    Inputs:
        content     str     Current token
        tag         str     Tag to attach to the new token, NUM by default
    
    Output:
        new_word    str     New token selected
    """
       
   # structure uppercase letters + number
    if re.match(r"^(?P<letters>[A-z]*)(?P<numbers>[0-9]*)$", content): 
        match = re.match(r"^(?P<letters>[A-z]*)(?P<numbers>[0-9]*)$", content)
        letter = ''.join(random.choice(string.ascii_uppercase) for _ in range(len(match.group("letters"))))
        number = ''.join(random.choice('0123456789') for _ in range(len(match.group("numbers"))))
        new_word = "<"+tag+">"+letter+number+"</"+tag+">"
        
    # structure 2 digits . 3 letters - 4 digits /- 1 digit or two
    elif re.match(r"^[0-9]{2}.[A-z]{3}-[0-9]{4}[-/][0-9]*$", content):
        letters = ''.join(random.choice(string.ascii_letters) for _ in range(3))
        numbers_1 = ''.join(random.choice('0123456789') for _ in range(2))
        numbers_2 = ''.join(random.choice('0123456789') for _ in range(4))
        numbers_3 = random.randint(0,27)
        symbol = random.choice("/-")
        new_word = "<"+tag+">"+numbers_1+"."+letters+"-"+numbers_2+symbol+str(numbers_3)+"</"+tag+">"
        
    # structure 10 digit mixed numbers and uppercase letters
    elif re.match(r"^[A-z0-9]{10}$", content):
        letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
        numbers_1 = ''.join(random.choice('0123456789') for _ in range(2))
        numbers_2 = ''.join(random.choice('0123456789') for _ in range(4))
        new_word = "<"+tag+">"+numbers_1+letters+numbers_2+"</"+tag+">"
        
    # structure two letters - 5 digit number
    elif re.match(r"^[A-z]{2}\-[0-9]*$", content):
        letters = ''.join(random.choice(string.ascii_letters) for _ in range(2))
        numbers = ''.join(random.choice('0123456789') for _ in range(len(content)-3)) # -3 = 2 letters + "-"
        new_word = "<"+tag+">"+letters+"-"+numbers+"</"+tag+">"
        
    # structure * numbers *
    elif re.match(r"^\*[0-9]*\*$", content):
        numbers = ''.join(random.choice('0123456789') for _ in range(len(content)-2)) # -3 = 2 *
        new_word = "<"+tag+">"+numbers+"</"+tag+">"
    
    # structure two numbers o number+letter / numbers
    elif re.match(r"^[0-9][0-9A-Z]/[0-9]*(-[0-4])?$", content):
        i = random.randint(0,5)
        if i > 1:
            numbers_1 = ''.join(random.choice('0123456789') for _ in range(2))
            numbers_2 = ''.join(random.choice('0123456789') for _ in range(len(content)-3))
            new_word = "<"+tag+">"+numbers_1+"/"+numbers_2+"</"+tag+">"
        else:
            numbers_1 = random.choice('0123456789')
            letter = random.choice(string.ascii_uppercase)
            numbers_2 = ''.join(random.choice('0123456789') for _ in range(len(content)-3))
            new_word = "<"+tag+">"+numbers_1+letter+"/"+numbers_2+"</"+tag+">"
    
    # structure numbers - numbers
    elif re.match(r"^(?P<first>[0-9]*)-(?P<second>[0-9]*)$", content):
        match = re.match("(?P<first>[0-9]*)-(?P<second>[0-9]*)", content)
        first = match.group("first")
        second = match.group("second")
        numbers_1 =''.join(random.choice('0123456789') for _ in range(len(first)))
        numbers_2 =''.join(random.choice('0123456789') for _ in range(len(second)))
        new_word = "<"+tag+">"+numbers_1+'-'+numbers_2+"</"+tag+">"
    
    # structure numbers - letters
    elif re.match(r"^(?P<first>[0-9]*)-(?P<second>[A-z]*)$", content):
        match = re.match(r"^(?P<first>[0-9]*)-(?P<second>[A-z]*)$", content)
        first = match.group("first")
        second = match.group("second")
        numbers =''.join(random.choice('0123456789') for _ in range(len(first)))
        letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(len(second)))
        new_word = "<"+tag+">"+numbers+'-'+letters+"</"+tag+">"
    
    # structure only numbers any length
    elif re.match(r"^[0-9]*$", content):
        number = ''.join(random.choice('0123456789') for _ in range(len(content)))
        new_word = "<"+tag+">"+number+"</"+tag+">"
        
    # Digital firm
    else:
        length = random.randint(22,39)
        new_word = ''.join(random.choice(string.ascii_letters + '0123456789' + '+=/') for _ in range(length))
        new_word = "<"+tag+">"+new_word+"</"+tag+">"
    
    return new_word


def randomize_report(report, name_db, surname_db, month_db, address_db, city_db, hospital_db, hc_db):
    """
    Randomizes the content every Named Entity (NE) that contains
    personal information.

    Intpus:
        report      str     Full report, with phrases separated by line breaks
    
    Output:
        new_report  list    Full report, with each phrase in a different element
                            of the list     
    """
    regex_tag = re.compile(r"(\<(?P<tag>.+?)(?<!\/)\>)(?P<content>.+?)(\<\/(.+?)\>)")
    new_report = []

    for phrase in report.split("\n"):
        new_phrase = [w for w in phrase.split()]
        tags = []
        contents = []

        for element in new_phrase:
            match = regex_tag.search(element)

            if match:
                tag = match.group("tag")
                content = match.group("content")
                tags.append(tag)
                contents.append(content)
            else:
                tags.append("O")
                contents.append(element)

        for index in range(len(tags)):
            if index == 0:
                prev_tag = "O"
                prev_word = ""
            else:
                prev_tag = tags[index-1]
                prev_word = contents[index-1]

            if tags[index] == "NAME":
                new_word = replace_name(prev_tag, prev_word, contents[index], name_db, surname_db)
                contents[index] = new_word
            elif tags[index] == "FECHA":
                new_word = replace_date(contents[index], month_db)
                contents[index] = new_word
            elif tags[index] == "LOC":
                j = index + 1

                try:
                    while tags[j] == tags[index]:
                        tags[j] = "O"
                        contents[j] = ""
                        j = j + 1
                except: pass
                new_word = replace_loc(contents[index], city_db)
                contents[index] = new_word

            elif tags[index] == "INST":
                j = index + 1
                try:
                    while tags[j] == tags[index]:
                        tags[j] = "O"
                        contents[j] = ""
                        j = j + 1
                except: pass
                new_word = replace_inst(contents[index], hospital_db, hc_db)
                contents[index] = new_word
            elif tags[index] == "DIR":
                dir_tags = ["DIR", "LOC"]
                j = index + 1
                try:
                    exit = True
                    while exit:
                        if tags[j] in dir_tags:
                            tags[j] = "O"
                            contents[j] = ""
                            j = j + 1
                        elif tags[j+1] in dir_tags:
                            tags[j+1] = "O"
                            contents[j+1] = ""
                            j = j + 1
                        else: 
                            exit = False
                except: pass
                new_word = replace_dir(address_db, city_db)
                contents[index] = new_word
            elif tags[index] == "NUM":
                new_word = replace_num(contents[index])
                contents[index] = new_word
            
            elif tags[index] == "CAB":
                contents[index] = "<CAB>"+contents[index]+"</CAB>"
            else:
                pass
        new_report.append(" ".join(contents))
    
    return new_report


def main(data_file, name_file, surname_file, address_file, cities_file, hospital_file, hc_file, output_file):

    data = load_reports_file(data_file)
    # Read name database
    name_db = pd.read_csv(name_file)
    name_db.columns = ["Nombre", "Frecuencia"]
    # Compute probability for each name in spanish population
    name_db["Probabilidad"] = name_db["Frecuencia"] / name_db.sum(axis=0)["Frecuencia"]

    # Read surname database
    surname_db = pd.read_csv(surname_file)
    surname_db.columns = ["Apellido", "Frecuencia"]
    # Compute probability distribution for each surname in spanish population
    surname_db["Probabilidad"] = surname_db["Frecuencia"] / surname_db.sum(axis=0)["Frecuencia"]


    # Read address database
    address_db = pd.read_csv(address_file)
    address_db.columns = ["n_mun","tipo_via", "dir_via", "dir_cp", "dir_mun", "dir_prov"]

    # Read city database
    city_db = pd.read_csv(cities_file)
    city_db["Probabilidad"] = city_db["POB19"] / city_db.sum(axis=0)["POB19"]

    # Date database
    month_db = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
                "octubre", "noviembre", "diciembre"]

    # Hospital database
    hospital_db = pd.read_csv(hospital_file)

    new_address = {
        "tipo_via": pd.Series(["" for i in range(hospital_db.shape[0])]),
        "dir_via": pd.Series(hospital_db["DIRECCION"]),
        "dir_cp": pd.Series(hospital_db["CODPOSTAL"]),
        "dir_mun": pd.Series(hospital_db["MUNICIPIOS"]),
        "dir_prov": pd.Series(hospital_db["PROVINCIAS"])
    }

    new_address = pd.DataFrame(new_address)
    address_db = pd.concat([address_db, new_address], axis=0)


    # Health centres database
    hc_db = pd.read_csv(hc_file)

    new_address = {
        "tipo_via": pd.Series(["" for i in range(hospital_db.shape[0])]),
        "dir_via": pd.Series(hc_db["DIRECCION"]),
        "dir_cp": pd.Series(hc_db["CP"]),
        "dir_mun": pd.Series(hc_db["MUNICIPIO"]),
        "dir_prov": pd.Series(hc_db["PROVINCIAS"])
    }

    new_address = pd.DataFrame(new_address)
    address_db = pd.concat([address_db, new_address], axis=0)

    hc_db = hc_db[hc_db["TIPOCENTRO"] == "CENTRO SALUD"]
    hc_db = hc_db.reset_index()
    address_db = address_db.reset_index()
    address_db = address_db.fillna("")
    
    new_data = []

    for report in data:
        new_report = randomize_report(report, name_db, surname_db, month_db, address_db, city_db, hospital_db, hc_db)
        new_data.append("\n".join(new_report))
    
    with open(output_file, "w") as wf:
        separator = '----------------------------------------------\n'
        wf.write(separator.join(new_data))



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-df', '--datafile',  type=str ,default='../data/sr/train.txt', help='Path of the file to alter')
    parser.add_argument('-nf', '--names',  type=str, default='../data/databases/names.csv', help='Path of the file containing the name database')
    parser.add_argument('-sf', '--surnames',  type=str, default='../data/databases/surnames.csv', help='Path of the file containing the surname database')
    parser.add_argument('-af', '--addresses',  type=str, default='../data/databases/address.csv', help='Path of the file containing the address database')
    parser.add_argument('-hf', '--hospitals', type=str, default='../data/databases/hospitals.csv', help='Path of the file containing the hospital database')
    parser.add_argument('-hcf', '--healthcentres', type=str, default='../data/databases/CentrosSalud.csv', help='Path of the file containing the health centres database')
    parser.add_argument('-cf', '--cities', type=str, default='../data/databases/PoblacionMunicipios.csv', help='Path of the file containing the cities database')
    parser.add_argument('-of', '--output', type=str, default='../data/sr/train.txt', help='Path of the output file')

    args = parser.parse_args()

    main(
        data_file=args.datafile,
        name_file=args.names,
        surname_file=args.surnames,
        address_file=args.addresses,
        cities_file=args.cities,
        hospital_file=args.hospitals,
        hc_file=args.healthcentres,
        output_file=args.output
        )
