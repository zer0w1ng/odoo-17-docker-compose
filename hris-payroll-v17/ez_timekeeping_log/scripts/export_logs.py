from __future__ import print_function
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time,sys,xmlrpclib
class Struct:
	def __init__(A,**B):A.__dict__.update(B)
def export_logs(conn):
	A=conn;E=xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(A.url));B=['name','time','identification_id','sync_id'];C=E.execute_kw(A.db,A.uid,A.password,'ez.time.log','search_read',[[('name','>=','2018-10-01')],B])
	if C:
		with open('log.csv','w')as D:
			D.write(','.join(B)+'\n')
			for F in C:G=[str(F[A])for A in B];D.write(','.join(G)+'\n')
if __name__=='__main__':
	if 0:url='http://localhost';admin_password='pass1234';super_password='pass1234';admin='admin';language='en_US';db='ecb_test'
	if 1:url='https://ez4.eztechsoft.com';admin_password='pass1234';super_password='passw0rd';admin='admin';language='en_US';db='ecb'
	common=xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url));print('VERSION',common.version());uid=common.authenticate(db,admin,admin_password,{});print('UID:',uid);p={'uid':uid,'password':admin_password,'db':db,'url':url};conn=Struct(**p);export_logs(conn)