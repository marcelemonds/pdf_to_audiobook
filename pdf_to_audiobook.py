import pyinputplus as pyip
import os
import sys
import filetype
import PyPDF2
import pyttsx3


def audiobook_maker(filepath, filename, choice):
    pdf = open(filepath, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    num_pages = pdf_reader.numPages
    player = pyttsx3.init()
    if choice == 'listen directly':
        for num in range(0, num_pages):
            page = pdf_reader.getPage(num)
            data = page.extractText()
            player.say(data)
            player.runAndWait()
        sys.exit()

    elif choice == 'as a file':
        for num in range(0, num_pages):
            output = f'{filename}_part-{num+1}.mp3'
            page = pdf_reader.getPage(num)
            data = page.extractText()
            player.save_to_file(data, output)
            player.runAndWait()


def pdf_to_audiobook():
    filepath = pyip.inputFilepath(prompt='Please enter the path to your pdf: ', mustExist=True, limit=2)
    file_type = filetype.guess(filepath).extension
    if file_type != 'pdf':
        sys.exit('Filetype is not supported. Please insert a path to a pdf file.')
    filename = os.path.basename(filepath).split('.')[0].replace(' ','_')
    choice = pyip.inputMenu(['listen directly', 'as a file'], limit=2, numbered=True, prompt='How would you like your audiobook?')
    audiobook_maker(filepath, filename, choice)


if __name__ == '__main__':
    pdf_to_audiobook()
