# -*- coding: utf-8 -*-
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from path import Path

stop_sentence = "pdf@home.icm.ac.cn"

def Pdf2Txt(source_file, save_file):
    # 来创建一个pdf文档分析器
    parser = PDFParser(source_file)
    # 创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr = PDFResourceManager()
        # 设定参数进行分析
        laparams = LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 处理每一页
        with open(save_file, "w", encoding="utf-8") as f:
            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        # print(x.get_text())
                        # p = Path(save_file)
                        # if p.exists():
                        #     p.remove_p()
                            results = x.get_text()
                            if stop_sentence not in results:
                                print(results)
                                f.write(results)



path = r'D:\outprojects\pdf_retrieval\datas\me02.pdf'
result_file = r"D:\outprojects\pdf_retrieval\results\me02.txt"
# Path = open(path, 'rb')
with open(path,'rb') as f:
    Pdf2Txt(f, result_file)


# f = "lucky.txt"
#
# a =8
# with open(f,"w", encoding='utf-8') as file:   #只需要将之前的”w"改为“a"即可，代表追加内容
#     for i in range(a):
#         file.write(str(i) + "d" + " "+"\n")
#     a +=1