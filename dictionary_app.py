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


# store dictionary datasets for access by program
data = []
data.append(load_dataset("dictionary_data/test_data.json"))
data.append(load_dataset("dictionary_data/web_data.json"))
data.append(load_dataset("dictionary_data/webstersenglishdictionary.json"))

# store list of commands for use during runtime
commands = load_dataset('dict_commands.json')

# list of command phrases which can be entered as user input
phrases = ('/h','/help', '/commands', '/q','/quit',
     '/e', '/end', '/x', '/exit', '/file_prompt_enable', 
     '/data', '/datasets', '/clear', '/cls', '/about')


def display_data():
    """Display all available datasets found in 'dictionary_data' folder"""
    print(f"{len(data)} datasets available:\n")
    filenames = [f for f in os.listdir('dictionary_data') if os.path.isfile(os.path.join('dictionary_data', f))]
    print(filenames)


def record_log(definition: str, word: str):
    print
    # Continue prompting for input until valid answer is provided
    while(True):
        # check user preferences file if present on machine
        if(os.path.exists("dict_prefs.txt")):
            with open("dict_prefs.txt") as file:
                content = file.read()
                if "false" in content:
                    break
        u_input = input("Save record of this search? \n(Enter ('y'/'yes')" 
        + " if yes, or ('n'/'no') if no) : ").lower()
        if(u_input == 'y' or u_input == 'yes'):
            if(os.path.exists("dict_search_records.txt")):
                print("\nSaving to logfile...")
                with open("dict_search_records.txt", 'a') as file:
                    file.write("- " + word.title() + "\n" + definition)
                    file.write("\n")
                print("Saved succesfully, view records in dict_search_records.txt."
                +"\nPress Enter to continue: \n")
                input()
                break
            else:
                print("\nLogfile not found, creating new logfile...")
                with open("dict_search_records.txt", 'a') as file:
                    file.write("Record of searches made with this"
                    +" installation of dictionary_app:\n")
                    file.write("- " +word.title() + "\n" + definition)
                    file.write("\n\n")
                    print("dict_search_records.txt successfully created\n"
                    +f"file can be found at {os.path.dirname(os.path.abspath(__file__))}.")
                    break
        elif(u_input == 'n' or u_input == 'no'):
            u_input = input("\nType ('/x' or '/stop') to disable this prompt,\n"
            +"or press enter to continue: ").lower()
            if(u_input == '/x' or u_input == '/stop'):
                if(os.path.exists("dict_prefs.txt")):
                    with open("dict_prefs.txt", "w") as file:
                        file.write("-record_prompt = false")
                        print("\ndict_prefs.txt successfully updated.\n")
                        print("Enter '/file_prompt_enable' when prompted"
                        +" to enter a word to turn file prompt back on.")
                else:
                    print("dict_prefs.txt not found, creating prefs file...")
                    with open("dict_prefs.txt", "w") as file:
                        file.write("-record_prompt = false")
                        print("dict_prefs.txt successfully created.\n"
                        +f"file can be found at {os.path.dirname(os.path.abspath(__file__))}.")
                        print("Enter '/file_prompt_enable' when prompted"
                        +" to enter a word to turn file prompt back on.")
            break
        else:
            print("Expecting ('y'/'yes' or 'n'/'no') : ")
            

def clear_screen():
    """Clear the screen of any present output."""
    if os.name == 'nt':
        os.system('cls') # use format for NT-systems if running windows
    else:
        os.system('clear') # use format for linux/osx if not running windows


def user_query(user_input = ''):
    """
    Evaluate user queries against valid commands from 'phrases' list,
    handle prompting user to enter more words after a successful sequence.
    """
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
        print("========================================================\n"
        +"Search for more terms?\nEnter ('y'/'yes' or 'n'/'no') : ")
        while(True):
            u_input = input().lower()
            if(u_input in response_phrases[0:2]):
                clear_screen()
                break
            elif(u_input in response_phrases[2:4]):
                clear_screen()
                terminate_program()
            else:
                print("Expecting ('y'/'yes') or ('n'/'no') : ")


    def display_help():
        """
        Display available commands and greeting to user
        to be called at startup or whenever '/help' or
        '/h' is entered.
        """
        print("Welcome to the dictionary, to see datasets that\n"
                +"were used to generate definitions, type ('/datasets').\n"
                +"\nTo exit the program, enter one of the following\n"
                +"preceeded by a '/' character, ie: '/q' or '/quit'.\n"
                +"-> ('x', 'exit', 'q', 'quit', 'e', 'end')\n"
                +"\nTo see this message again, type ('/h' or '/help').\n"
                +"To see a full list of available commands, \n"
                +"type ('/commands')."
                +"\n======================================================")
                  

    def display_commands():
        """
        Display full list of available commands executed with the '/command'
        format, ie /exit, /help, /file_prompt_enable.
        """
        print("\nComplete list of commands useable at word prompt\n"
        +"Format is as follows:\n'Name of command - description' : "
        +"[comma separated list\nof phrases to execute the command]\n" 
        +"--------------------------------------------------------")
        for key, value in commands.items():
            output = format_str_len(f"{key} {value}")
            print(f"{output}\n")


    def check_input():
            """Check user input against valid commands from 'phrases' list."""   
            if(user_input == "retry"):
                retry_prompt()
            elif(user_input in phrases[0:2]):
                display_help()
            elif(user_input == phrases[2]):
                display_commands()
            elif(user_input in phrases[3:9]):
                clear_screen()
                terminate_program(user_input)
            elif(user_input == phrases[9]):
                clear_screen()
                if(os.path.exists("dict_prefs.txt")):
                    with open("dict_prefs.txt", 'w') as file:
                        file.write('-record_prompt = true')
                    print("File prompt after search enabled.")
            elif(user_input in phrases[10:12]):
                display_data()
            elif(user_input in phrases[12:14]):
                clear_screen()
            else:
                print("\n==================================================")
    
    # call check_input whenever user_query is executed
    check_input()


def typo_check(word: str):
    """
    First make sure word doesn't match any phrases in data.
    If exact match cannot be found, attempt to find a single
    close-matching word to suggest.
    """
    w_cases = [word, word.lower(), word.title(), word.upper()]
    for case in w_cases:
        if(get_word_dataset(case) != None):
            dataset = get_word_dataset(case)
            for word in w_cases:
                if word in phrases or word in dataset:
                    return word
            break
    

    # if word isn't found in the current dataset, search for a close match
        suggested_word = None
        for case in w_cases:
            if(suggest_word(case) != None):
                suggested_word = suggest_word(case)
                break
        
        if(suggested_word != None):
            u_response = input(f"Did you mean {suggested_word[0]}?"
            +"\nEnter ('y'/'yes' if yes, or ('n'/'no) if no: ").lower()
            if(u_response == 'y' or u_response == 'yes'):
                return suggested_word[0]
            else:
                print(f"Can't find {w_cases[0]} in dictionary, please provide valid English words.") 
                return '' # return blank line so user doesn't see 'none'
    
    # if word isn't found in the current dataset and there are no similar words, prompt the user
    print(f"Can't find {w_cases[0]} in dictionary, please provide valid English words.") 
    return '' # return blank line so user doesn't see 'none'


def suggest_word(word: str):
    """Take provided word and search for any similar words in available datasets."""
    for dataset in data:
        if(len(get_close_matches(word, dataset))>1):
            return get_close_matches(word, dataset,n=1)
    return None # return none if no viable suggestions are found


def format_word(word):
    """
    If word is provided in lowercase, convert to titlecase.
    Otherwise preserve formatting (USA, England, proper nouns etc).
    """
    if(word.lower() == word):
        return word.title()
    else: 
        return word


def format_definition(raw_definition, dataset=data[0]):
    """
    Return a formatted version of the raw definition for a word,
    applies simple line-wrap formatting.
    """
    if(type(raw_definition) == list):
        formatted_output = []
        for value in raw_definition:
            formatted_output.append(f"{format_str_len(value)}\n")
        return formatted_output
    else:
        formatted_output = [""]
        formatted_output[0] = f"{format_str_len(raw_definition)}\n"
        return formatted_output
    
def format_str_len(str_input: str, str_len=72):
    """
    Take in a string and format it to be within specific
    length parameter.
    """
    return fill(str_input, str_len)

def get_word_dataset(word: str):
    """
    Find proper dataset based on word-matching.
    """
    for dataset in data:
        if word in dataset:
            return dataset
    
    # should use dict_commands.json and commands functionality once implemented
    if word in phrases:
        return data[1]
    
    # return None if word not found
    return None


def retrieve_definition(word: str) :
    """
    Return the definition (if found) of the
    provided string assuming it is a valid
    English word found in selected dataset.
    """
    curr_data = get_word_dataset(word)
    if(curr_data != None):
        w_cases = [word, word.lower(), word.title(), word.upper()]
        for case in w_cases:
            if case in curr_data:
                return format_definition(curr_data[case], curr_data)
            else:
                return {"NULL":'No results found for this phrase.'}
    return {""} # return a blank line if dataset is None
            

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
            print(format_word(proc_input) + f"\n\n{definition}")
            record_log(str(definition), proc_input)         

    def cleanup(proc_input=""):
        if("NULL" not in retrieve_definition(proc_input)):
            user_query("retry")
            clear_screen()

    # main sequence
    u_input = process_search_phrase(input("Please enter a word: "))
    display_output(u_input)
    cleanup(u_input)


def main():
    # display commands and instructions at startup
    user_query("/help")
    while(True) :
        dictionary_operations()


# startup
if __name__ == "__main__":
    main()
