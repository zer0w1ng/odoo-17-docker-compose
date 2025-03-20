from PyPDF2 import PdfFileWriter,PdfFileReader
if __name__=='__main__':from PyPDF2 import PageObject
else:from PyPDF2.pdf import PageObject
from io import StringIO,BytesIO
import os,inspect,base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,legal,landscape
from reportlab.lib.utils import ImageReader
from datetime import datetime
import base64,logging
_logger=logging.getLogger(__name__)
if __name__!='__main__':from odoo import api,fields,models
data={'company':[180,-107,'ABCD CORP.'],'company_number':[655,-107,'111-222-333-0000'],'company_address':[83,-129,'Adrdsfadsf dfsadfsa df'],'company_email':[530,-129,'abcd@efg.com'],'signatory':[650,-563,'Abcdasd E. Aasdfsaaa','C'],'is_initial_list':[351,-72,'x','C'],'is_subseq_list':[351,-82,'x','C']}
data_footer={'number_listed':[170,-561,'123'],'page':[423,-577,'1','C'],'page_count':[454,-577,'5','C']}
data_lines={'hdmf_number0':[60,-190,'0000000','C'],'employee0':[118,-190,'John Doe'],'position0':[357,-190,'Manager','C'],'salary0':[481,-190,'50,000.00','R'],'hired0':[519,-190,'12/25/2023','C'],'prev_employer0':[626,-190,'XYZ Company']}
def create_page(ref_page,texts,pagesize=letter):
	D=BytesIO();B=canvas.Canvas(D,pagesize=letter);B.setFont('Helvetica',12);B.rotate(90)
	for A in texts:
		C='L'
		if len(A)>=4:C=A[3]
		if C=='C':
			if A[2]:B.drawCentredString(A[0],A[1],A[2])
		elif C=='R':
			if A[2]:B.drawRightString(A[0],A[1],A[2])
		elif C=='F':B.setFont(A[0],A[1])
		elif A[2]:B.drawString(A[0],A[1],A[2])
	B.save();D.seek(0);G=PdfFileReader(D);H=G.getPage(0);E=ref_page;I=H;F=PageObject.createBlankPage(None,E.mediaBox.getWidth(),E.mediaBox.getHeight());F.mergeScaledTranslatedPage(E,1,0,0);F.mergePage(I);return F
def create_pdf(request,hdmf_er2_id):
	def E(texts,ref,i,value):A=ref[:];A[1]=ref[1]-i*12;A[2]=value;texts.append(A)
	def J(npage,texts,existing_pdf,output):
		A=texts;A.append(['Helvetica',12,0,'F']);data_footer['page'][2]='{}'.format(npage);data_footer['number_listed'][2]='{}'.format(B)
		for C in data_footer:A.append(data_footer[C])
		D=existing_pdf.getPage(0);E=create_page(D,A);output.addPage(E.rotateClockwise(90))
	C=request.env['ez.hdmf.er2'].browse(hdmf_er2_id);L=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));M=os.path.join(L,'er2.pdf');N=open(M,'rb');K=PdfFileReader(N);data['company'][2]=C.employer_name;data['company_number'][2]=C.employer_number;data['company_address'][2]=C.employer_address;data['company_email'][2]=C.employer_email;data['signatory'][2]=C.signatory;data['is_initial_list'][2]=C.is_initial_list and'x'or'';data['is_subseq_list'][2]=C.is_subseq_list and'x'or'';G=PdfFileWriter();A=[];H=True;O=data_lines['hdmf_number0'];P=data_lines['employee0'];Q=data_lines['position0'];R=data_lines['salary0'];S=data_lines['hired0'];T=data_lines['prev_employer0'];B=0;F=0;data_footer['page_count'][2]='{}'.format(1+int(len(C.hdmf_er2_line_ids)/30))
	for D in C.hdmf_er2_line_ids:
		_logger.debug('create: i=%s page=%s',B,F)
		if H:
			A=[];H=False;A.append(['Helvetica',12,0,'F'])
			for U in data:A.append(data[U])
			A.append(['Helvetica',10,0,'F'])
		E(A,O,B,D.hdmf_number);E(A,P,B,D.employee_id.name);E(A,Q,B,D.position);E(A,R,B,'{:0,.2f}'.format(D.salary))
		if D.hired:E(A,S,B,fields.Date.from_string(D.hired).strftime('%b-%d-%Y'))
		E(A,T,B,D.prev_employer);B+=1
		if B>=30:F+=1;J(F,A,K,G);H=True;B=0
	if B:J(F,A,K,G)
	I=BytesIO();G.write(I);V=I.getvalue();I.close();return V
if __name__=='__main__':
	from pprint import pprint
	if 1:
		fpdf=open('er2.pdf','rb');output=PdfFileWriter();existing_pdf=PdfFileReader(fpdf);page_template=existing_pdf.getPage(0);texts=[]
		for x in range(0,800,50):texts.append([x,-20,'X%s'%x])
		for y in range(-600,0,20):texts.append([250,y,'Y%s'%y])
		texts.append(['Helvetica',12,0,'F'])
		for k in data:texts.append(data[k])
		texts.append(['Helvetica',12,0,'F'])
		for k in data_footer:texts.append(data_footer[k])
		texts.append(['Helvetica',10,0,'F'])
		for k in data_lines:texts.append(data_lines[k])
		h=data_lines['hdmf_number0']
		for i in range(1,30):d=h[:];d[1]=h[1]-i*12;d[2]='%s'%i*5;texts.append(d)
		page=create_page(page_template,texts);output.addPage(page.rotateClockwise(90));outputStream=open('out.pdf','wb');output.write(outputStream);outputStream.close()