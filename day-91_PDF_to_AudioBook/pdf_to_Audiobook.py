import pyttsx3
import PyPDF2
import PySimpleGUI as sg

# Ask to choose a PDF file
layout = [[sg.Text('Choose a PDF file:')],
          [sg.Input(), sg.FileBrowse()],
          [sg.OK(), sg.Cancel()]]
window = sg.Window('PDF to AudioBook', layout)
event, values = window.read()
window.close()

# Extract text from PDF file
pdf_file = values[0]

pdfreader = PyPDF2.PdfReader(pdf_file)
pages = len(pdfreader.pages)

speaker = pyttsx3.init()
for num in range(0, pages):
    page = pdfreader.pages[num]
    text = page.extract_text()
    speaker.say(text)
    speaker.runAndWait()


