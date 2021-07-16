"""
Simple console dictionary application,
uses console input to get definitions.
"""
import json
import os
from textwrap import fill
from difflib import get_close_matches

def load_dataset(data_path: str) :
    """
    Load the json object at specified path into data,
    intended for dictionary data and definitions.
    """
    json_file = open(data_path)
    return json.load(json_file)

# store dictionary dataset for access by program, test_data for tests
data = []
data.append(load_dataset("data.json"))
data.append(load_dataset("test_data.json"))

# list of command phrases which can be entered as user input
phrases = ('/h','/help',
    '/q','/quit','/e','/exit','/x')

def record_log(definition: str, word: str):
    print
    # Continue prompting for input until valid answer is provided
    while(True):
        u_input = input("Save record of this search? (Enter ('y'/'yes')" 
        + " if yes, or ('n'/'no') if no) :").lower()
        if(u_input == 'y' or u_input == 'yes'):
            if(os.path.exists("dict_search_records.txt")):
                print("Saving to logfile...")
                with open("dict_search_records.txt", 'a') as file:
                    file.write("- " + word.title() + "\n" + definition)
                    file.write("\n")
                print("Saved succesfully, view records in dict_search_records.txt."
                +"\nPress Enter to continue:")
                input()
                break
            else:
                print("Logfile not found, creating new logfile...")
                with open("dict_search_records.txt", 'a') as file:
                    file.write("Record of searches made with this"
                    +" installation of dictionary_app:\n")
                    file.write("- " +word.title() + "\n" + definition)
                    file.write("\n")
                    print("dict_search_records.txt successfully created\n"
                    +f"file can be found at {os.path.dirname(os.path.abspath(__file__))}.")           
        elif(u_input == 'n' or u_input == 'no'):
            print("Press Enter to continue:")
            input()
            os.system('cls')
            break
        else:
            print("Expecting ('y'/'yes' or 'n'/'no') :")
            

def user_query(user_input = ''):
    # store list of phrases for checking against user responses
    response_phrases = ('y','yes','n','no',)
    
    def terminate_program(value='/q'):
        """
        Display a closing message, terminate the program instance.
        """
        print("Exiting program...")
        exit()


    def retry_prompt():
        """
        Prompt if user would like to continue searching the dictionary.
        """
        print("===================================================="
        + "==========================================================\n"
        +"Search for more terms?\nEnter ('y'/'yes' or 'n'/'no') :")
        while(True):
            u_input = input().lower()
            if(u_input in response_phrases[0:2]):
                os.system('cls')
                break
            elif(u_input in response_phrases[2:4]):
                os.system('cls')
                terminate_program()
            else:
                print("Expecting ('y'/'yes') or ('n'/'no') :\n")


    def display_help():
        """
        Display available commands and greeting to user
        to be called at startup or whenever '/help' or
        '/h' is entered.
        """
        print("Welcome to the dictionary, the following dataset has been" 
                +" used to generate these definitions: (link goes here)\n"
                +"To exit the program, enter one of the following phrases"
                +" preceeded by a '/' character, ie: '/q' or '/quit'"
                +"\n('x', 'exit', 'q', 'quit', 'e', 'end')"
                +"To see this message again, type ('/h' or '/help')"
                +"\n================================================"
                +"==================================================")
                  

    def process_input():   
            if(user_input == "retry"):
                retry_prompt()
            elif(user_input in phrases[0:2]):
                display_help()
            elif(user_input in phrases[2:7]):
                os.system('cls')
                terminate_program(user_input)
            else:
                print("\n================================================"
                +"==================================================")
    
    process_input()


def typo_check(word: str):
    
    w_cases = [word, word.lower(), word.title(), word.upper()]
    for word in w_cases:
        if word in phrases:
            return word
        for dataset in data:
            if word in dataset:
                return word
    
    if len(get_close_matches(word, data[0].keys())) > 0:
        suggested_word = get_close_matches(word, data[0].keys(),n=1)
        u_response = input(f"Did you mean {suggested_word[0]}?"
        +"\nEnter ('y'/'yes' if yes, or ('n'/'no) if no: ").lower()
        if(u_response == 'y' or u_response == 'yes'):
            return suggested_word[0]
        else:
            print(f"Can't find {word} in dictionary, please provide valid English words.") 
            return '' # return blank line so user doesn't see 'none'
    else:
        print(f"Can't find {word} in dictionary, please provide valid English words.")
        # return blank line so user doesn't see 'none'
        return ''


def format_output(raw_input):
    """
    Return a formatted version of the raw input
    applies simple line-wrap formatting.
    """
    formatted_output = []
    for value in raw_input:
        formatted_output.append(fill(value, 72))
    return formatted_output

def get_word_dataset(word: str):
    """
    Find proper dataset based on word-matching.
    """
    for dataset in data:
        if word in dataset:
            return dataset
    return data[0] # return "data.json" as default dataset

def retrieve_definition(word: str) :
    """
    Return the definition (if found) of the
    provided string assuming it is a valid
    English word found in selected dataset.
    """
    curr_data = get_word_dataset(word)
    if word != "":
        w_cases = [word, word.lower(), word.title(), word.upper()]
        for case in w_cases:
            if case in curr_data:
                return format_output(curr_data[case])
            elif case in phrases:
                return {"NULL":'No results found for this phrase.'}
    else:
        return {"NULL":'No results found for this phrase.'}
            

def dictionary_operations():
    """
    Handle sequencing of dictionary operations,
    getting input, displaying output.
    """
    def process_search_phrase(u_input):
        # check for typos in user input  
        search = typo_check(u_input)
        # check if user input matches any special phrases
        user_query(search)
        return search
    
    def display_output(proc_input):
        # retrieve definitions from dictionary
        definition = "\n".join(retrieve_definition(proc_input))
        if("NULL" not in definition):
            print(proc_input.title() + f"\n{definition}")
            record_log(str(definition), proc_input)

    def cleanup(proc_input=""):
        if("NULL" not in retrieve_definition(proc_input)):
            user_query("retry")
            os.system('cls')

    u_input = process_search_phrase(input("Please enter a word: "))
    display_output(u_input)
    cleanup(u_input)

def main():
    user_query("/help")
    while(True) :
        dictionary_operations()

# startup sequence
if __name__ == "__main__":
    main()