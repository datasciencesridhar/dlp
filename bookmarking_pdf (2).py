import time
start_time = time.time()
from win32com.client.dynamic import Dispatch
import os


def doc_2_pdf(Input_File):
    word = Dispatch('word.Application') # initiation of word application
    word.Visible=False
    input_file = Input_File
    try:
        wb = word.Documents.Open(input_file)
        # Please Mentiion the oupout destination path here 
        #/** the destination path should be different fdrom input path**
        output_file = 'C://Users//anves//Downloads//pdf_search//output//'+doc_pdf[0:-4]
        wb.ExportAsFixedFormat2 (output_file,
                                 ExportFormat=17,
                                 OpenAfterExport=False,
                                 OptimizeFor=0, 
                                 Range=0,
                                 Item=7,
                                 IncludeDocProps=True,
                                 KeepIRM=True,
                                 CreateBookmarks=1,
                                 DocStructureTags=True,
                                 BitmapMissingFonts=True,
                                 UseISO19005_1=True,
                                 OptimizeForImageQuality=True
                                 )
        print("word is converted back to pdf conversion is done.")
        wb.Close()
        word.Quit()    
    except:
        word.Quit()
        

input_folder ='C://Users//anves//Downloads//pdf_search//input'
os.chdir(input_folder)
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        doc_pdf =filename
        Input_File = os.path.abspath(doc_pdf)
        doc_2_pdf(Input_File)
        #os.remove(input_file)

        continue
    else:
        continue
print("--- %s seconds ---" % (time.time() - start_time))
