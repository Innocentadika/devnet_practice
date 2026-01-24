import PyPDF2

with open('./assets/exam.pdf','rb') as file:
    reader = PyPDF2.pdfFileReader(file)
    print(reader.numPages)
    page = reader.getPage(0)
    page.rotateCounterClockwise(90)

    writer = PyPDF2.pdfFileWriter(page)
    with open('./assets/edited.pdf','wb') as new_file:
        writer.write(new_file)
        