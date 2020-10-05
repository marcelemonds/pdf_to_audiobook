import pyinputplus as pyip
import os
import sys
import filetype
import PyPDF2
import pyttsx3
from progress.bar import Bar


def audiobook_maker(filepath, filename, choice, language):
    pdf = open(filepath, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    num_pages = pdf_reader.numPages
    player = pyttsx3.init()
    # set player language
    voices = player.getProperty('voices')
    for voice in voices:
        if language in voice.name:
            player.setProperty('voice', voice.id)
    # play pdf directly
    if choice == 'listen directly':
        bar = Bar(f'Playing audiobook {filename} ', max=num_pages)
        for num in range(0, num_pages):
            page = pdf_reader.getPage(num)
            data = page.extractText()
            player.say(data)
            player.runAndWait()
            bar.next()
        bar.finish()
        print(f'Audiobook {filename} finished playing.')
    # save audiobook to file
    elif choice == 'as a file':
        bar = Bar(f'Saving audiobook {filename} ', max=num_pages)
        for num in range(0, num_pages):
            output = f'{filename}_part-{num+1}.mp3'
            page = pdf_reader.getPage(num)
            data = page.extractText()
            player.save_to_file(data, output)
            player.runAndWait()
            bar.next()
        bar.finish()
        print(f'Audiobook {filename} completely saved.')
    sys.exit()


def pdf_to_audiobook():
    filepath = pyip.inputFilepath(prompt='Please enter the path to your pdf: ', mustExist=True, limit=2)
    file_type = filetype.guess(filepath).extension
    if file_type != 'pdf':
        sys.exit('Filetype is not supported. Please insert a path to a pdf file.')
    filename = os.path.basename(filepath).split('.')[0].replace(' ','_')
    choice = pyip.inputMenu(['listen directly', 'as a file'], limit=2, numbered=True, prompt='How would you like your audiobook?')
    language = pyip.inputMenu(['German', 'English'], limit=2, numbered=True, prompt='How would you like your audiobook?')
    audiobook_maker(filepath, filename, choice, language)


if __name__ == '__main__':
    pdf_to_audiobook()
