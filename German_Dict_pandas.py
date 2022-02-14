from asyncore import ExitNow
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from random import uniform
import time

native_lang = 'english'
target_lang = 'german'
no_match = "Sorry, we found no matches for your search term(s) ."


def search(input_word, word_freq, native_lang, target_lang, timeout = None):
    ### term = search term
    ### timeout = None or max. number of seconds to wait for response
    print("######### ", input_word, " #########")
    Dict_File = "dict_test.json"
    
    #Dict subsections
    Def = "Definition"
    Dec = "Declination"
    Conj = "Conjugation"
    Freq = "Frequency"

    Definition_Table = [
        "Noun",
        "Adjective",
        "Verb",
        "Preposition",
        "Phrase",
        "Example",
    ]
    Declination_Table = [
        "Deklination",
    ]
    Conjugation_Table = [
        "Indikativ",
        "Konjunktiv",
        "Imperativ",
        "Unpers"
    ]




    short_url="https://dict.leo.org"
    url_sufix = "?side=right"  ## adding this at the end sets translation one directinoal from Target lang to Native lang
    url = short_url + "/" + target_lang + "-" + native_lang + "/" + url_sufix

    ## Main html requests
    Main_Definition_Req_Response = requests.get(url, params={'search': input_word}, timeout=timeout)
    soup=BeautifulSoup(Main_Definition_Req_Response.content, "html.parser")
    match = soup.find_all("p", string = no_match)
    if len(match) > 0:
        return "No_Match"
        exit()
    try:
        Reference_Table_URL = short_url + soup.select_one('a[href*="flecttab/flectionTable"]')['href']
        Reference_Tables_Req_Response = requests.get(Reference_Table_URL, timeout=timeout)
        Term_Dataframe = pd.read_html(Main_Definition_Req_Response.text) + pd.read_html(Reference_Tables_Req_Response.text)
    except:
        Term_Dataframe = pd.read_html(Main_Definition_Req_Response.text)
    
    
    #Initialize Dict entry
    with open(Dict_File) as file:
        Main_Dict=json.load(file)

    Main_Dict[input_word] = {
        Def: {},
        Dec: {},
        Conj: {},
        Freq: word_freq
    }
    ## Combine html responses into pandas Dataframes and clean up dataframe
        ###Remove empty df
        ###Remove tables we do not need
        ###Remove Columns containing only null values
        ###Remove duplicate columns if they are present (the conjugation table columns are doubled)

    for dataframe in Term_Dataframe:
        if dataframe.empty:
            del dataframe
            continue
        Df_Title = str(dataframe.columns[0])
        if any(substring in Df_Title for substring in Definition_Table):
            Tab = Def
        elif any(substring in Df_Title for substring in Declination_Table):
            Tab = Dec
        elif any(substring in Df_Title for substring in Conjugation_Table):
            Tab = Conj
        else:
            del dataframe
            continue

        check_col=[]
        for col in dataframe.columns:
            if pd.isnull(dataframe[col]).all() or dataframe[col].equals(check_col):
                dataframe = dataframe.drop(col, axis=1)
                continue
            else:
                check_col = dataframe[col]
        dataframe = dataframe.fillna("N/A")
        Main_Dict[input_word][Tab][Df_Title]= dataframe.to_numpy().tolist()


    with open(Dict_File, 'w') as fp:
        json.dump(Main_Dict, fp)
    
    return "Success"









def Create_Dict(UpperLimit):
    ### Scrape all term definitions and tables in the list with a random delay between 1.5 and 5 seconds
    ### In word list file, mark each as either entered or "No Match"
    Word_List = "Word_File.csv"
    with open(Word_List) as fp:
        Word_df = pd.read_csv(fp, encoding = 'utf=8')
    for i in range(UpperLimit):
        Word = Word_df.iloc[i, 0]
        Freq = int(Word_df.iloc[i, 1])
        No_Match = Word_df.iloc[i, 2]
        Entered = Word_df.iloc[i, 3]
        
        if No_Match == 0 and Entered == 0:
            time.sleep(uniform(1.5,5))
            result = search(Word, Freq, native_lang, target_lang)
            if result == "Success":
                print(Word, "PASS")
                Word_df.iloc[i, 3] = 1
            elif result == "No_Match":
                print(Word, "FAIL")
                Word_df.iloc[i, 2] = 1
            else:
                continue
        Word_df.to_csv(Word_List, index=False, encoding = 'utf=8')

# search("stattfinden", 0, native_lang, target_lang)
Create_Dict(1000)

# for each in word_list:
#     ## Scrape all term definitions and tables in the list with a random delay between 1.5 and 5 seconds
#     search(each, 0, native_lang, target_lang)
#     time.sleep(uniform(1.5,5))

