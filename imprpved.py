import json
import os
from textwrap import fill
from difflib import get_close_matches

def load_dataset(data_path):
    with open(data_path, 'r') as file:
        return json.load(file)

def load_datasets():
    datasets = []
    for file_path in ["dictionary_data/test_data.json",
                      "dictionary_data/web_data.json",
                      "dictionary_data/webstersenglishdictionary.json"]:
        datasets.append(load_dataset(file_path))
    return datasets

def display_available_datasets():
    filenames = [f for f in os.listdir('dictionary_data') if os.path.isfile(os.path.join('dictionary_data', f))]
    print(f"{len(filenames)} datasets available:\n{filenames}")

def record_log(definition, word):
    record_prompt = input("Save record of this search? (y/n): ").lower()
    if record_prompt in ['y', 'yes']:
        with open("dict_search_records.txt", 'a') as file:
            file.write("- " + word.title() + "\n" + definition + "\n\n")
        print("Record saved successfully.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_help():
    print("Welcome to the dictionary!")
    print("To see available datasets, type '/datasets'.")
    print("To exit, type '/q' or '/quit'.")
    print("For help, type '/help'.")

def display_about():
    clear_screen()
    print("About SimpleDictionary:")
    print("This is a simple console dictionary application.")
    print("It allows you to search for words and phrases within a set of dictionary data.")

def display_commands():
    print("\nList of Available Commands:")
    for command, description in commands.items():
        print(f"{command} - {description}")

def process_user_input(user_input, datasets):
    if user_input in ['/q', '/quit']:
        return True
    elif user_input in ['/h', '/help']:
        display_help()
    elif user_input in ['/datasets']:
        display_available_datasets()
    elif user_input in ['/about']:
        display_about()
    elif user_input in ['/commands']:
        display_commands()
    else:
        search_word = typo_check(user_input, datasets)
        display_output(search_word, datasets)

def typo_check(word, datasets):
    word_variants = [word, word.lower(), word.title(), word.upper()]
    for variant in word_variants:
        for dataset in datasets:
            if variant in dataset:
                return variant
    suggested_word = suggest_word(word, datasets)
    if suggested_word:
        user_response = input(f"Did you mean {suggested_word}? (y/n): ").lower()
        if user_response in ['y', 'yes']:
            return suggested_word
    print(f"Can't find '{word}' in the dictionary. Please provide a valid English word.")
    return None

def suggest_word(word, datasets):
    for dataset in datasets:
        suggested_word = get_close_matches(word, dataset, n=1)
        if suggested_word:
            return suggested_word[0]
    return None

def format_word(word):
    return word.title() if word.islower() else word

def format_definition(definition):
    return fill(definition, width=72)

def display_output(search_word, datasets):
    if search_word:
        for dataset in datasets:
            if search_word in dataset:
                definitions = dataset[search_word]
                if isinstance(definitions, list):
                    for definition in definitions:
                        formatted_definition = format_definition(definition)
                        print(f"{format_word(search_word)}\n\n{formatted_definition}")
                        record_log(formatted_definition, search_word)
                else:
                    formatted_definition = format_definition(definitions)
                    print(f"{format_word(search_word)}\n\n{formatted_definition}")
                    record_log(formatted_definition, search_word)
                break
        else:
            print("No results found for this phrase.")
def main():
    datasets = load_datasets()
    display_help()
    while True:
        user_input = input("--> Please enter a word: ").strip()
        if process_user_input(user_input, datasets):
            break
        clear_screen()

if __name__ == "__main__":
    main()
