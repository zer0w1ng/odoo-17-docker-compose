from openpyxl import load_workbook
import csv
from pprint import pprint
import json,re,random
from datetime import datetime
from dateutil.relativedelta import relativedelta
from string import ascii_lowercase
import urllib.request,odoorpc
def test(odoo):A=odoo.env['hr.applicant'];B=A.search([('stage_id.name','=','New')],limit=1);D='Initial Qualification';C=odoo.env['hr.recruitment.stage'].search([('name','=',D)],limit=1);E=A.write(B,{'stage_id':C[0]});print(E,B,C)
def odoo_login(odoo_conn):A=odoo_conn;B=odoorpc.ODOO(A['host'],port=A['port'],protocol=A['protocol']);B.login(A['db'],A['user'],A['password']);return B
if __name__=='__main__':odoo_conn={'host':'wipro.eztechsoft.com','port':443,'protocol':'jsonrpc+ssl','db':'wipro','user':'rberdin@eztechsoft.com','password':'7470de99e712c5fa0b81c3a224c8b4ced60a6b5b'};odoo=odoo_login(odoo_conn);test(odoo)