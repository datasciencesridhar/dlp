import PyPDF2
import fitz
import os
def _setup_page_id_to_num(pdf, pages=None, _result=None, _num_pages=None):
    if _result is None:
        _result = {}
    if pages is None:
        _num_pages = []
        pages = pdf.trailer["/Root"].getObject()["/Pages"].getObject()
    t = pages["/Type"]
    if t == "/Pages":
        for page in pages["/Kids"]:
            _result[page.idnum] = len(_num_pages)
            _setup_page_id_to_num(pdf, page.getObject(), _result, _num_pages)
    elif t == "/Page":
        _num_pages.append(1)
    return _result
def creating_table_of_contents(input_file):
    f = open(input_file,'rb')
    p = PyPDF2.PdfFileReader(f)
    # map page ids to page numbers
    pg_id_num_map = _setup_page_id_to_num(p)
    o = p.getOutlines()
    pg_num = pg_id_num_map[o[0].page.idnum] + 1
    ad = PyPDF2.PdfFileMerger()
    ad.addBookmark("Education",2)
    bookmarks = [o[i].title for i in range(len(o))]
    pagenum = [pg_id_num_map[o[i].page.idnum] + 1 for i in range(len(o))]
    print("list of bookmarks in the given pdf file \n",bookmarks)
    print("respective page numbers of the bookmarks \n",pagenum)
    f.close()

    from reportlab.pdfgen import canvas
    from reportlab.lib import pdfencrypt
    pdf = canvas.Canvas("1.pdf",bottomup=0)
    pdf.drawString(30,20,"Table Of Contents")

    s = [i.split(":") for i in bookmarks]
    c=50
    ss = [i[z] for i in s for z in range(len(i))]
    aa= max(ss, key = len)
    print(aa)
    ac= "......................"
    for i,j in enumerate(s):
        x=0
        y=32
        #print(j)
        for z in j:
            if len(z)>2:
                
                dt=len(aa)-len(z)
                #print(dt)
                for l in range(dt):
                    z+=".."
                
                print(len(z))
                pdf.drawString(y,c,str(i+1)+"."+str(x)+' '+z+ac+" "+str(pagenum[i]))
                y+=10
                c+=30
                x+=1
    pdf.save()

def creating_final_editable_pdf(image_path,output_path,input_file):
    os.chdir(image_path)
    x = [a for a in os.listdir() if a.endswith(".pdf")]
    writer = PyPDF2.PdfFileWriter()  # create a writer to save the updated results
    file = input_file
    pdf = fitz.open(file)
    page_count = pdf.pageCount
    for pdf in x:
        scale = PyPDF2.PdfFileReader(pdf)
        if pdf=="1.pdf":
            page = scale.getPage(0)
            writer.addPage(page)
        else:
            for j in range(page_count):
                page = scale.getPage(j)
                writer.addPage(page)
        with open(pdf , "wb+") as f:
            writer.write(f)
    

    print('complete editable pdf is created')
    return True

input_path ='C:\\Users\\anves\\Downloads\\reportlab'
output_path ='C:\\Users\\anves\\Downloads\\reportlab\\final'
input_file ='Anvesh_Resume.pdf'

creating_table_of_contents(input_file)
creating_final_editable_pdf(image_path,output_path,input_file)