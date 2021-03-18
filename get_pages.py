# -*- coding: utf-8 -*-
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


# from cStringIO import StringIO

def convert_pdf_to_txt(path, save_name):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    with open(path, 'rb') as fp:
        # fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)
    # fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    try:
        with open("%s" % save_name, "w") as f:  # 格式化字符串还能这么用！
            for i in str:
                f.write(i)
        print("%s Writing Succeed!" % save_name)
    except:
        print("Writing Failed!")


path = r'D:\outprojects\pdf_retrieval\datas\me02.pdf'
convert_pdf_to_txt(path, "c.txt")
