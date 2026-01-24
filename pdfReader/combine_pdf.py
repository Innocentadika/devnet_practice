import sys
import os
import PyPDF2.merger

inputs = sys.argv[1:]

def pdf_combiner(pdf_list):
    merger = PyPDF2.pdfFileMerger()
    for pdf in pdf_list:
        print(pdf)
        with open('pdf','rb') as f:
            merger.append(f)

    with open('./assets/combined.pdf', 'wr') as f2:
        merger.writer(f2)

    pdf_combiner(inputs)
    pdf_folder = './assets'

    pdf_file = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.endWith('.pdf')]

    if pdf_file:
        pdf_combiner(pdf_file)

    else:
        print("No PDF files found in the folder")