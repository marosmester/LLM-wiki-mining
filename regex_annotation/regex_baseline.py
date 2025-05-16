import re
import json
import os
from pathlib import Path
import numpy as np
import argparse

def find_birth_year(path_to_person):
    '''
    Finds the person's birth year in the wikipedia body text file.  
    '''
    # Get birth year from wiki main text
    main_text = path_to_person / "text.txt"
    pattern = r"Category:\b[12]\d{3}\b births" # 4 digit number beginning with a 1 or a 2
    x = find_year_file(main_text, pattern)
    if x is not None:
        byear = int( x.group()[9:13] )           # extract birth yeat as int
    else:
        byear = None

    return byear

def find_year_file(fpath, pattern):
    '''
    Search any elligible file AS IT WAS A TXT FILE.
    '''
    #print(fpath)
    with open(fpath, "r") as f:
        content = f.read()
    match = re.search(pattern, content)
    return match

def find_year_json_entry(jsonEntry) -> np.array:
    '''
    Search a caption in a single JSON entry for a year.
    Tries multiple patterns. 

    Args:
        jsonEntry: Python dictionary created from a JSON object

    Returns:
        year: 1- or 2-element np.array of ints, depending on the accuracy of the year info. 
              2-element array indicates year interval.
    '''
    cap = jsonEntry['caption']
    no_cap = True if cap is None else False
    found = False

    # 4-digit number:
    if not found and not no_cap: 
        p = r"\b[12]\d{3}\b"    # pattern
        match = re.search(p, cap)
        if match != None:
            found = True
            year = np.array( [int(match.group())] )

    # 4-digit number followed by s (e.g. 1970s or 1970's)
    if not found and not no_cap:
        p = r"\b[12]\d{3}['’]?s\b"
        match = re.search(p, cap)
        if match != None:
            found = True
            year = int( match.group()[:4] )
            year = np.array( [year, year + 9] )

    if not found:
        return None
    else:
        return year

def analyze_person(path_to_person, file = None):
    '''
    Search a person's directory and prints (writes) all years it can find.
    The years are written to a file specified in file arg. If none provided, the output
    will be printed in the  terminal
    '''
    # Get birth year from wiki main text
    main_text = path_to_person / "text.txt"
    pattern = r"Category:\b[12]\d{3}\b births" # 4 digit number beginning with a 1 or a 2
    x = find_year_file(main_text, pattern)
    if x is not None:
        byear = int( x.group()[9:13] )           # extract birth yeat as int
        print("birth year = ", byear, file= file)
    else:
        print("No birth year found in \"text.txt\".", file= file)

    # Get photo year from INFOBOX caption
    infobox = path_to_person / 'infobox_captions.json'
    if os.path.exists(infobox):
        with open(infobox, "r") as f:
            jsonData = json.load(f)
        if jsonData == []:
            print("File \"infobox_captions.json\" is empty", file=file)
        for entry in jsonData:
            year = find_year_json_entry(entry)
            print("year from infobox caption= ", year, file= file)
    else:
        print("No file named \"infobox_captions.json\" found.", file=file)
        
    # For every other non-infobox caption, calculate the age
    captions = path_to_person / "captions.json"
    if os.path.exists(captions):
        with open(captions, "r") as f:
            jsonData = json.load(f)
        if jsonData == []:
            print("File \"captions.json\" is empty", file=file)
        for entry in jsonData:
            year = find_year_json_entry(entry)
            print(f"caption= {entry['caption']}", file = file)
            print(f"year from caption = {year}", file = file)
    else:
        print("No file named \"captions.json\" found.", file=file)

    print("-----------------------------------", file=file)
    return path_to_person

def build_entry_dict(path, bYear, capYear):
    """
    Returns a python dict that when turned into json results
    in json file simmilar to the one created by annotation tool.
    """
    ret = dict()
    ret["path"] = "./" + str(Path(*path.parts[-4:]))
    ret["person_id"] = None
    ret["fully_anotated"] = False
    ret["birthday_annotated"] = True if bYear is not None else False
    ret["figure_year_annotated"] = True if capYear is not None else False
    ret["face_found"] = False
    ret["wiki_page_sufficient"] = True
    ret["birth_day"] = None
    ret["birth_month"] = None
    ret["birth_year"] = bYear if bYear is not None else None
    if capYear is not None:
        if capYear.shape[0] == 1:
            ret["estimated_year_creation_left"] = capYear[0].item()
            ret["estimatee_year_creation_right"] = capYear[0].item()
        elif capYear.shape[0] == 2:
            ret["estimated_year_creation_left"] = capYear[0].item()
            ret["estimatee_year_creation_right"] = capYear[1].item()
    ret["annotation_shortcoming"] = "This simple annotation by regex cannot detect a face in an image."
    ret["bounding_box_index"] = None
    ret["face_pixel_coordinates"] = None
    return ret

def get_persons_json_annotation(path_to_person):
    """
    Creates regex_annotation.json file for given person.
    """
    # create dictionary that will become the ouput json file
    annotation_data = []

    # Get birth year from wiki main text
    main_text = path_to_person / "text.txt"
    pattern = r"Category:\b[12]\d{3}\b births" # 4 digit number beginning with a 1 or a 2
    x = find_year_file(main_text, pattern)
    if x is not None:
        byear = int( x.group()[9:13] )           # extract birth yeat as int
    else:
        byear = None

    # Get photo year from INFOBOX caption
    infobox = path_to_person / 'infobox_captions.json'
    if os.path.exists(infobox):
        with open(infobox, "r") as f:
            jsonData = json.load(f)
        if jsonData != []:
            for entry in jsonData:
                year =  find_year_json_entry(entry)
                if year is not None:
                    p = path_to_person / "title_images" / entry["saved_filename"]
                    json_entry_dict = build_entry_dict( p, byear, year)
                    annotation_data.append( json_entry_dict)
        
    # For every other non-infobox caption, calculate the age
    captions = path_to_person / "captions.json"
    if os.path.exists(captions):
        with open(captions, "r") as f:
            jsonData = json.load(f)
        if jsonData != []:
            for entry in jsonData:
                year =  find_year_json_entry(entry)
                if year is not None:
                    p = path_to_person / "images" / entry["saved_filename"]
                    json_entry_dict = build_entry_dict( p, byear, year)
                    annotation_data.append( json_entry_dict)

    with open(path_to_person/"regex_annotation.json" , "w", encoding="utf-8") as f:
        json.dump(annotation_data, f, indent=4)


if __name__ == "__main__":
    # parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("arg_path", type=str, help="Path from user")
    datasetPath = Path( parser.parse_args().arg_path )
    #datasetPath= Path(os.getcwd()).parent
    #datasetPath = datasetPath / "annotation_tool/example_set"
    # parsedJsonPath = Path(os.getcwd()) / "parsed.json"
    print("Absolute path to dataset drectory provided:", datasetPath)
    # print(parsedJsonPath)

    # print(f'INFO: Parsing data')
    # parser = PersonParser(datasetPath)
    # parser.parse_all_persons(path=parsedJsonPath, write=True)
    # print(f'INFO: Data parsed')

    # find all eleigible folders
    folders = [str(f.name) for f in datasetPath.iterdir()]
    folders.sort()
    #with open(parsedJsonPath, "r") as f:
    #    parsedJson = json.load(f)

    # reset output file
    fname = "output.txt"
    f = open(fname, "w")
    f.close()

    # fill out output file 
    cnt = 0
    with open(fname, "a") as file:
        for person in folders:
            #person = Path( entry["path"] ).parts[1]
            print(f"{cnt} Analyzing: {person}")
            print(str(cnt) + ' ' + str(person), file= file)
            ret = analyze_person(datasetPath/ person, file=file)
            get_persons_json_annotation(datasetPath/ person)
            cnt += 1