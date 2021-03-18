# -*- coding: utf-8 -*-
from typing import List

from path import Path
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser

from configuration import Configuration
from helpers import load_config, get_package_root_path
import traceback
stop_sentence = "pdf@home.icm.ac.cn"


class ParsePDFFile:
    def __init__(self):
        self.configuration: Configuration = load_config()
        self.target_location = Path(get_package_root_path()) / "results"

    def _load_files(self) -> List[Path]:
        raw_file_path = Path(self.configuration.raw_file_location)
        results = raw_file_path.walkfiles(match=r"*.pdf")
        return list(results)

    def parse(self):
        files = self._load_files()
        for f in files:
            print("parsing file :", str(f.realpath()))
            file_name = f.name.replace("pdf", "txt")
            target_file = self.target_location / file_name
            try:
                with open(str(f.realpath()), 'rb') as f:
                    self.pdf2txt(f, str(target_file.realpath()))
            except Exception as e:
                # print(traceback.print_stack())
                print(f"解析文件{file_name}发生错误啦，跳过此文件，请查找原因: {str(e)}")

    def pdf2txt(self, source_file, save_file):
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
                    try:
                        interpreter.process_page(page)
                        # 接受该页面的LTPage对象
                        layout = device.get_result()
                        for x in layout:
                            if (isinstance(x, LTTextBoxHorizontal)):
                                results = x.get_text()
                                if stop_sentence not in results:
                                    print(type(results))
                                    f.write(results)
                    except Exception:
                        print("error occurred on the page:")
                        print(traceback.print_exc())



if __name__ == '__main__':
    p = ParsePDFFile()
    p.parse()
    print("parse file done.")
