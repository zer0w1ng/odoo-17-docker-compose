from ast import literal_eval
import babel
from dateutil.relativedelta import relativedelta
import itertools,json,base64
from odoo.tools.misc import xlwt
from babel.dates import format_datetime,format_date
from odoo import http,fields,_
from odoo.http import request,content_disposition
from odoo.tools import float_round
from odoo.addons.web.controllers.main import clean_action
from.pdf import create_pdf
import io,os,inspect,base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,legal
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfFileWriter,PdfFileReader
import logging
_logger=logging.getLogger(__name__)
class PdfCreatorController(http.Controller):
	@http.route(['/hdmf_er2/<int:hdmf_er2_id>/er2.pdf'],type='http',auth='user')
	def bir2316(self,hdmf_er2_id=False):A=create_pdf(request,hdmf_er2_id);C='HDMF-ER2.pdf';B=[('Content-Type','application/pdf')];return request.make_response(A,headers=B)
def Xcreate_pdf(hdmf_er2_id):E=request.env['ez.hdmf.er2'].browse(hdmf_er2_id);F=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));G=os.path.join(F,'er2.pdf');H=open(G,'rb');B=PdfFileReader(H);C=B.getFormTextFields();_logger.debug('fields: %s',C);C['NAME OF EMPLOYERFIRM']=E.employer_name;I=B.getPage(0);D=PdfFileWriter();D.addPage(I);A=io.BytesIO();D.write(A);J=A.getvalue();A.close();return J