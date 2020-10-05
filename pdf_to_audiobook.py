import pyinputplus as pyip
import os
import sys
import filetype


def audiobook_maker(filepath, choice):
    if choice == 'listen directly':
        print('listen')
    elif choice == 'as a file':
        print('file')


def pdf_to_audiobook():
    filepath = pyip.inputFilepath(prompt='Please enter the path to your pdf: ', mustExist=True, limit=2)
    file_type = filetype.guess(filepath).extension
    print(file_type)
    # print(file_type.mime)
    if file_type != 'pdf':
        sys.exit('Filetype is not supported. Please insert a path to a pdf file.')

    choice = pyip.inputMenu(['listen directly', 'as a file'], limit=2, numbered=True, prompt='How would you like your audiobook?')
    print(choice)
    audiobook_maker(filepath, choice)


if __name__ == '__main__':
    pdf_to_audiobook()
