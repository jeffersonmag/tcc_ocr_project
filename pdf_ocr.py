from PyPDF2 import PdfFileReader, PdfFileWriter
import re
import os

def split(path, name_of_split):
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output = f'{name_of_split}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
            output_pdf.close()
            ler(output)


def ler(output):
    pdf_file = open(output, 'rb')
    read_pdf = PdfFileReader(pdf_file)
    #number_of_pages = read_pdf.getNumPages()
    page = read_pdf.getPage(0)
    page_content = page.extractText()
    pdf_file.close()

    parsed = ''.join(page_content)
    parsed = re.sub('\n', ' ', parsed)
    #parsed = re.sub('Empresa', 'CPF ', parsed)

    #Empresa
    texto = re.search(r'Empresa', parsed)
    valor = texto.end()
    empresa = parsed[valor+23:valor+27]
    empresa = re.sub(r'[-,.:@#?!&$]', '', empresa)

    #Nome
    textoInicio = re.search(r'Nome', parsed) #inicio
    textoFim = re.search(r'Cód.', parsed) #fim
    valorInicio = textoInicio.end()  # acaba a identificacao da localizacao
    valorFim = textoFim.start()    # começa outras informacoes
    nome = parsed[valorInicio + 5:valorFim]
    nreg = parsed[valorInicio:valorInicio + 5]
    #nome = re.sub(r'[-,.:@#?!&$]', '', nome)

    # Fim do Nome i

    valor = texto.end()
    nreg = re.sub(r'[-,.:@#?!&$]', '', nreg)
    os.rename(output, nreg+' - '+nome+'.pdf')
    print(nome)
    #print(parsed)
    #print(page_content)


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)



def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = """
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information

if __name__ == '__main__':
    path = 'holerite.pdf'
    split(path, 'jupyter_page')
    #extract_information(path)
    #paths = ['document1.pdf', 'document2.pdf']
    #(paths, output='merged.pdf')