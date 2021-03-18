# coding: utf-8

import sys

from pdfminer import pdfparser
from pdfminer import pdfdocument
from pdfminer import pdfinterp
from pdfminer import pdfpage
from pdfminer import converter
from pdfminer import layout

file_path = r'D:\outprojects\pdf_retrieval\datas\test.pdf'
with open(file_path,'rb') as fp:
    parser = pdfparser.PDFParser(fp)
    document = pdfdocument.PDFDocument(parser)
    if not document.is_extractable:
        raise pdfdocument.PDFTextExtractionNotAllowed
    rsrcmgr = pdfinterp.PDFResourceManager()
    laparams = layout.LAParams()
    device = converter.PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = pdfinterp.PDFPageInterpreter(rsrcmgr, device)
    pdf_pages = pdfpage.PDFPage.create_pages(document)
    for page in pdf_pages:
        interpreter.process_page(page)
        page_layout = device.get_result()

        print(type(page_layout), page_layout)