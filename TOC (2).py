import PyPDF2
import fitz
import os
import time
from reportlab.pdfgen import canvas
from reportlab.lib import pdfencrypt
from reportlab.platypus import PageBreak
from textwrap import wrap

def creating_final_editable_pdf(input_path,input_file):
    #pythoncom.CoInitialize()
    os.chdir(input_path)
    x = [a for a in os.listdir() if a.endswith(".pdf")]
    x.sort()
    print(x)
    writer = PyPDF2.PdfFileWriter()  # create a writer to save the updated results
    file = input_file
    print("\n",file)
    
    
    for i in x:
        if i !=file:
            pdf = fitz.open(i)
            page_count = pdf.pageCount
            #pdf.close()
            scale = PyPDF2.PdfFileReader(i)
            print("\n",page_count,"\n")
            for j in range(page_count):
                #print(j)
                page = scale.getPage(j)
                writer.addPage(page)
    with open("toc.pdf" , "wb+") as f:
        writer.write(f)
    f.close()
    writer1 = PyPDF2.PdfFileWriter()
    pdf = fitz.open("toc.pdf")
    page_count1 = pdf.pageCount
    #pdf.close()
    scale1 = PyPDF2.PdfFileReader("toc.pdf")
    print("\n",page_count,"\n")
    pdf0 = fitz.open(file)
    page_count = pdf0.pageCount
    #pdf.close()
    print("\n",page_count,"\n")
    scale = PyPDF2.PdfFileReader(file)
    count=0
    for jj in range(page_count):
        #print(j)
        if count ==0:
            for j in range(page_count1):
                #print(j)
                page = scale1.getPage(j)
                writer1.addPage(page)
            count+=1
        page = scale.getPage(jj)
        writer1.addPage(page)
    with open(file , "wb+") as f:
        writer1.write(f)
    f.close()
    
    time.sleep(1)
    #os.remove("0.pdf")
    print('Table of Contents is added to the pdf.')
    
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
def toc_page(pd,bookmarks,pagenum,w,h,pg,ii,g):
    pdf = canvas.Canvas(pd,bottomup=0,pagesize=(w,h))
    if pd =="0.pdf":pdf.drawString(30,20,"Table Of Contents")
    #s = [i.split(":") for i in bookmarks]
    c=50
    ac= "..................."
    lines = 0
    rr=True
    j=bookmarks
    try:      
        for ii in range(len(j)):
            x=0
            y=32
            if lines ==23:
                rr=True
                break
            if type(j[ii]) is list:
                y+=10
                if len(j[ii])>=1:
                    while g in range(len(j[ii])):
                        sd=j[ii][g]
                        lc=len(sd)
                        if lc>75:
                            sd=sd[0:76]
                        if lc<75:
                            dh=75-lc
                            for i in range(dh):
                                sd=sd+"."
                            
                        pdf.drawString(y,c,sd+ac+" "+str(pagenum[pg]))
                        c+=30
                        pg+=1
                        g+=1
                        lines+=1
                    ii+=1
                        
            else:
                sb = j[ii]
                lc = len(sb)
                if lc>75:
                    sb=sb[0:76]
                if lc<75:
                    dh=75-lc
                    for i in range(dh):
                        sb=sb+"."
                pdf.drawString(y,c,sb+ac+" "+str(pagenum[pg]))
                c+=30
                lines+=1
                pg+=1
                ii+=1
        pdf.save()
        return [rr,pg,ii,g]
    except IndexError:
        rr=False
        return [rr,pg,ii,g]

def creating_table_of_contents(input_path,input_file):
    #pythoncom.CoInitialize()
    os.chdir(input_path)
    doc = fitz.open(input_file)
    page = doc.loadPage(0)
    a =page.MediaBox
    w = a[2]
    h = a[3]
    doc.close()
    print(input_path)
    print('\n',input_file)
    f = open(input_file,'rb')
    p = PyPDF2.PdfFileReader(f)
    # map page ids to page numbers
    pg_id_num_map = _setup_page_id_to_num(p)
    o = p.getOutlines()
    #print('\n',len(o[3]),'\n')
    #print('\n',len(o[0]),'\n')
    pg_num = pg_id_num_map[o[0].page.idnum] + 1
    #print("\n",pg_num,"\n")
    bookmarks=[]
    for i in range(len(o)):
        if len(o[i])==6:
            try:
                bookmarks.append(o[i].title)
            except:pass
        else:
            aa=[]
            for j in o[i]:
                if len(j)==6:
                    try:
                        aa.append(j.title)
                    except:pass
                else:
                    for a in j:
                        if len(a)==6:
                            try:
                                aa.append(a.title)
                            except:pass
                        else:
                            for b in a:
                                if len(b)==6:
                                    try:
                                        aa.append(b.title)
                                    except:pass
                                else:
                                    try:
                                        for c in b:
                                            if len(c)==6:
                                                aa.append(c.title)
                                    except:pass
            
            try:
                bookmarks.append(aa)
            except:pass

    pagenum=[]
    for i in range(len(o)):
        if len(o[i])==6:
            try:
                pagenum.append(pg_id_num_map[o[i].page.idnum] + 1)
            except:pass
        else:
            for j in o[i]:
                if len(j)==6:
                    try:
                        pagenum.append(pg_id_num_map[j.page.idnum] + 1)
                    except:pass
                else:
                    for a in j:
                        if len(a)==6:
                            try:
                                pagenum.append(pg_id_num_map[a.page.idnum] + 1)
                            except:pass
                        else:
                            for b in a:
                                if len(b)==6:
                                    try:
                                        pagenum.append(pg_id_num_map[b.page.idnum] + 1)
                                    except:pass
                                else:
                                    try:
                                        for c in b:
                                            if len(c)==6:
                                                pagenum.append(pg_id_num_map[c.page.idnum] + 1)
                                    except:pass

    #  = [pg_id_num_map[o[i].page.idnum] + 1 for i in range(len(o))]
    #print("\n list of bookmarks in the given pdf file:",bookmarks[3])
    #print("\n respective page numbers of the bookmarks : ",pagenum[3])
    f.close()
    aa=0
    pg=0
    ii=0
    g=0
    while True:
        pd=str(aa)+".pdf"
        fg=toc_page(pd,bookmarks,pagenum,w,h,pg,ii,g)
        print(pd)
        aa+=1
        try:
            result=fg[0]
            pg=fg[1]
            ii=fg[2]
            g=fg[3]
            print(len(bookmarks))
        except:pass
        time.sleep(1)
        if result==False:break
    creating_final_editable_pdf(input_path,input_file)