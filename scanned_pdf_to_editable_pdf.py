# create a input folder and place the input file 
# create a output folder
# create  a image folder  
# install tessaract application from this url 
# ( https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe )
# Then using pip install  open cv and install pytersseract
# pip install PyMuPDF
# pip install PyPDF2
import time
start_time = time.time()
import fitz
from win32com.client.dynamic import Dispatch
import pytesseract
import PyPDF2
import os

def Converting_pages_pdf_into_image(input_folder,input_file):
    os.chdir(input_folder)
    file = input_file
    pdf = fitz.open(file)
    page_count = pdf.pageCount # getting to tal no. of pages in the given pdf
    for j in range(page_count):
        page = pdf.loadPage(j)
        zoom_x = 6.0  # horizontal zoom
        zomm_y = 6.0  # vertical zoom
        mat = fitz.Matrix(zoom_x, zomm_y)  # zoom factor 2 in each dimension
        pix = page.getPixmap(matrix = mat)  # use 'mat' instead of the identity matrix
        new_file = file[0:-4]+'_'+str(j)+'.jpg'
        image_path='C://Users//anves//Downloads//pdf_search//images'
        os.chdir(image_path)
        pix.writeImage(new_file)
    print('pages of pdf are converted as high quality images')
    return image_path,input_file,page_count

              
def converting_image_to_editable_pdf(image_path):     
    os.chdir(image_path)
    
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    for filename in os.listdir(image_path):
        if filename.endswith(".jpg"):
            Img =filename
            pdf = pytesseract.image_to_pdf_or_hocr(Img, extension='pdf')
            with open(Img[0:-4]+'.pdf', 'w+b') as f:
               f.write(pdf)
    print('each image is converted to pdf')

def creating_final_editable_pdf(image_path,output_folder,input_file):
        os.chdir(image_path)
        x = [a for a in os.listdir() if a.endswith(".pdf")]
        
        for pdf in x:
            scale = PyPDF2.PdfFileReader(pdf)
            page = scale.getPage(0)
            page.scaleBy(0.175)
            writer = PyPDF2.PdfFileWriter()  # create a writer to save the updated results
            writer.addPage(page)
            with open(pdf , "wb+") as f:
                writer.write(f)
        
        y = [a for a in os.listdir() if a.endswith(".pdf")]
        merger = PyPDF2.PdfFileMerger()
        for pdf in y:
            merger.append(open(pdf, 'rb'))
        os.chdir(output_folder)
        with open(input_file , "wb") as fout:
            merger.write(fout)
        print('complete editable pdf is created')
        return True
        

input_folder ='C://Users//anves//Downloads//pdf_search//input'
output_folder = 'C://Users//anves//Downloads//pdf_search//output'
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        input_file =filename
        image_path,input_file,page_count = Converting_pages_pdf_into_image(input_folder,input_file)
        converting_image_to_editable_pdf(image_path)
        creating_final_editable_pdf(image_path, output_folder,input_file)

def doc_2_pdf(Input_File):
        word = Dispatch('word.Application') # initiation of word application
        word.Visible=False
        input_file = Input_File
        try:
            wb = word.Documents.Open(input_file)
            # Please Mentiion the oupout destination path here 
            #/** the destination path should be different fdrom input path**
            output_file = 'C://Users//anves//Downloads//pdf_search//final//'+doc_pdf[0:-4]
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
            print("Bookmarking f thge pdf is done.")
            wb.Close()
            word.Quit()
        except:
            word.Quit()    
        
input_folder ='C://Users//anves//Downloads//pdf_search//output'
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
os._exit(00)


