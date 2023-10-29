import tkinter as tk

# Morse code dictionary
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 
    'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 
    'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 
    'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 
    'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', 
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.',
    ' ': ' / '
}

# Translate text to Morse code
def text_to_morse():
    text = text_area.get("1.0", "end-1c").upper()
    morse_code = ""
    for char in text:
        if char in morse_code_dict:
            morse_code += morse_code_dict[char] + " "
        else:
            morse_code += char
    morse_area.delete("1.0", "end")
    morse_area.insert("1.0", morse_code)

# Translate Morse code to text
def morse_to_text():
    morse_code = morse_area.get("1.0", "end-1c")
    morse_code = morse_code.split(' ')
    text = ""
    for code in morse_code:
        for char, morse in morse_code_dict.items():
            if code == morse:
                text += char
        if code == '/':
            text += ' '
        else:
            text += ''
    text_area.delete("1.0", "end")
    text_area.insert("1.0", text)

# Main window
window = tk.Tk()
window.title("Morse Code Translator")

font = ('Helvetica', 14)

# Create widgets
text_area = tk.Text(window, height=5, 
                    width=40, font=font)
morse_area = tk.Text(window, height=5, 
                     width=40, font=font)
translate_button = tk.Button(
    window, text="Translate to Morse Code", 
    command=text_to_morse, font=font)
translate_button2 = tk.Button(
    window, text="Translate to Text", 
    command=morse_to_text, font=font)

text_area.pack()
translate_button.pack()
morse_area.pack()
translate_button2.pack()

window.mainloop()
