from tkinter import *
from googletrans import Translator
import re

# create an instance of the Translator class
translator = Translator()

# function to translate Roman Urdu to English
def translate_urdu_to_english(roman_urdu_text):
    # define a regular expression pattern to match only Roman Urdu characters
    roman_urdu_pattern = r"[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF\u08A9\u200c ]+"
    # find all matches of the pattern in the input text
    matches = re.findall(roman_urdu_pattern, roman_urdu_text)
    # join the matches to form a single string
    urdu_text = " ".join(matches)
    # detect the language of the input text
    detected_lang = translator.detect(urdu_text).lang
    if detected_lang == "ur":
        # translate the text to English
        english_text = translator.translate(urdu_text, src="ur", dest="en").text
        return english_text
    else:
        return "The input text is not in Roman Urdu."

# function to handle translation when the "Translate" button is clicked
def translate_text():
    roman_urdu_text = roman_urdu_entry.get()
    english_text = translate_urdu_to_english(roman_urdu_text)
    english_translation_label.config(text=english_text)

# create a new window
window = Tk()
window.title("Roman Urdu to English Translator")

# create a label and an entry field for the Roman Urdu text
roman_urdu_label = Label(window, text="Enter Roman Urdu text:")
roman_urdu_label.pack()
roman_urdu_entry = Entry(window, width=50)
roman_urdu_entry.pack()

# create a "Translate" button
translate_button = Button(window, text="Translate", command=translate_text)
translate_button.pack()

# create a label to display the English translation
english_translation_label = Label(window, text="")
english_translation_label.pack()

# function to open a new window to display the English translation
def show_translation_window():
    translation_window = Toplevel(window)
    translation_window.title("English Translation")
    english_translation_text = english_translation_label.cget("text")
    english_translation_label_in_window = Label(translation_window, text=english_translation_text)
    english_translation_label_in_window.pack()

# create a "Show Translation" button to open a new window with the English translation
show_translation_button = Button(window, text="Show Translation", command=show_translation_window)
show_translation_button.pack()

# start the event loop
window.mainloop()
