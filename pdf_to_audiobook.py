import pyinputplus as pyip
import os
import sys
import filetype
import PyPDF2
import pyttsx3
import shutil
from progress.bar import Bar
from gtts import gTTS 

def audiobook_maker_online(filepath, filename, choice, language):
    languages = {'German': 'de', 'English': 'en'}
    pdf = open(filepath, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    num_pages = pdf_reader.numPages
    # create directory for audiobook
    if not os.path.exists(f'{filename}'):
        os.mkdir(filename)
    if choice == 'listen directly':
        print(f'Playing audiobook {filename}.')
        bar = Bar('Page: ', max=num_pages)
    elif choice == 'as file(s)':
        print(f'Saving audiobook {filename} to file.')
        bar = Bar('Page: ', max=num_pages)
    for num in range(0, num_pages):
        bar.next()
        output = f'{filename}_part-{num+1}.mp3'
        path = os.path.join(filename, output)
        page = pdf_reader.getPage(num)
        data = page.extractText()
        speech = gTTS(text = data, lang = languages[language], slow = False)
        speech.save(path)
        if choice == 'listen directly':
            os.system(path)
    # remove audiobook directory
    if choice == 'listen directly':
        shutil.rmtree(os.path.join(filename))
    bar.finish()
    return sys.exit()


def audiobook_maker_offline(filepath, filename, choice, language):
    pdf = open(filepath, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    num_pages = pdf_reader.numPages
    player = pyttsx3.init()
    # set player language
    voices = player.getProperty('voices')
    for voice in voices:
        if language in voice.name:
            player.setProperty('voice', voice.id)
    # chnage player speed
    rate = player.getProperty('rate')
    player.setProperty('rate', rate-15)
    # play pdf directly
    if choice == 'listen directly':
        print(f'Playing audiobook {filename}.')
        bar = Bar('Page: ', max=num_pages)
        for num in range(0, num_pages):
            bar.next()
            page = pdf_reader.getPage(num)
            data = page.extractText()
            player.say(data)
            player.runAndWait()
        bar.finish()
        print(f'Audiobook {filename} finished playing.')
    # save audiobook to file
    elif choice == 'as file(s)':
        # create directory for audiobook
        if not os.path.exists(f'{filename}'):
            os.mkdir(filename)
        print(f'Saving audiobook {filename} to file.')
        bar = Bar('Page: ', max=num_pages)
        # save audiobook page by page to directory
        for num in range(0, num_pages):
            bar.next()
            output = f'{filename}_part-{num+1}.mp3'
            path = os.path.join(filename, output)
            page = pdf_reader.getPage(num)
            data = page.extractText()
            player.save_to_file(data, path)
            player.runAndWait()
        bar.finish()
        print(f'Audiobook {filename} completely saved.')
    return sys.exit()


def pdf_to_audiobook():
    try:
        filepath = pyip.inputFilepath(prompt='Please enter the path to your pdf: ', mustExist=True, limit=2)
    except pyip.ValidationException:
        sys.exit('Error: Please insert an existing filepath.')
    # check for filetype
    file_type = filetype.guess(filepath).extension
    if file_type != 'pdf':
        sys.exit('Error: Filetype is not supported. Please insert a path to a pdf file.')
    filename = os.path.basename(filepath).split('.')[0].replace(' ','_')
    try:
        choice = pyip.inputMenu(['listen directly', 'as file(s)'], limit=2, numbered=True, prompt='How would you like your audiobook?')
        connection = pyip.inputMenu(['no', 'yes'], limit=2, numbered=True, prompt='Do you have internet connection?')
        language = pyip.inputMenu(['German', 'English'], limit=2, numbered=True, prompt='What language is audiobook in?')
    except pyip.RetryLimitException:
        sys.exit('Error: Please restart the program and select one of the given choices.')
    if connection == 'no':
        audiobook_maker_offline(filepath, filename, choice, language)
    elif connection == 'yes':
        audiobook_maker_online(filepath, filename, choice, language)
    return sys.exit()



if __name__ == '__main__':
    pdf_to_audiobook()
