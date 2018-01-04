# This code transforms a all PDFs found in a folder typed by the user into one txt file
# then it counts the words found in the txt

import os
import glob
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from StringIO import StringIO
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

from collections import Counter
import string


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    try:
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
    except Exception, e:
        print "the error is:", str(e)
        return str()


    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


pdflist = glob.glob("/Users/astrid/Downloads/Emma/2017/*.pdf")

for pdf in pdflist:


    print("Working on: " + pdf + '\n')
    fout = open('pdfs_2017.txt', 'a')
    fout.write(convert_pdf_to_txt(pdf))
    fout.close()

fin = open('pdfs_2017.txt', 'r')
words = fin.read().lower()
out = words.translate(string.maketrans("", ""), string.punctuation)
fin.close()

wordss = out.split()

cnt = Counter(wordss)

fout = open('counts_2017.txt', 'w')
for k, v in cnt.items():
    fout.write(k + "," + str(v) + '\n')
fout.close()






