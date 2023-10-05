from PyDictionary import PyDictionary

def search_word_meaning(word):
    dictionary = PyDictionary()

    # Get word definitions
    definitions = dictionary.meaning(word)
    
    if definitions:
        print(f"Meaning(s) of '{word}':")
        for part_of_speech, meaning_list in definitions.items():
            print(f"{part_of_speech}:")
            for meaning in meaning_list:
                print(f"  - {meaning}")
    else:
        print(f"No meanings found for '{word}'.")


while True:
    word = input(
        "Enter a word (or 'exit' to quit): ").strip().lower()
    
    if word == 'exit':
        print("Goodbye!")
        break
    
    search_word_meaning(word)
    print("\n")

