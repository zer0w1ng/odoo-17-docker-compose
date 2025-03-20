#!/usr/bin/env python
import logging,sys,time,xmlrpclib
from datetime import datetime
from odoo_xmlrpc import*
_logger=logging.getLogger('sync')
def get_last_sync_id(conn):res=conn.execute('ez.time.log','get_last_sync_id');_logger.debug('get_last_sync_id: sync_id=%s',res);return res
def get_dtr_log(conn,sync_id):
	_logger.debug('get_dtr_log: start')
	if sync_id:ids=conn.execute('hr.ph.attendance.raw','search',[('id','>',sync_id)])
	else:ids=conn.execute('hr.ph.attendance.raw','search',[('name','>=','2018-01-01')])
	_logger.debug('get_dtr_log: ids=%s',len(ids));fields=['name','time','company_id'];logs=conn.execute('hr.ph.attendance.raw','read',ids,fields);_logger.debug('get_dtr_log: done');res=[]
	for log in logs:res.append([log['id'],log['name'],log['time'],log['company_id']])
	return res
def send_logs(conn,logs):_logger.debug('send_logs: start');res=conn.execute('ez.time.log','insert_logs',logs);_logger.debug('send_logs: done res=%s',res)
def del_cloud_logs(conn):res=conn.execute('ez.time.log','delete_logs','2018-01-01','2018-12-31')
def sync_dtr_logs(ecb_conn,cloud_conn,sleep=900):
	server='http://192.168.1.99:8069';db='ECB_ERP2';user='admin';password='adminpass1234';server2='http://localhost';db2='ecb';user2='admin';password2='pass1234'
	while True:
		_logger.info('**DTR Sync: %s',time.ctime());ecb_conn.connect();cloud_conn.connect();sync_id=get_last_sync_id(cloud_conn);logs=get_dtr_log(ecb_conn,sync_id);_logger.info('  - sync_id=%s logs=%s',sync_id,len(logs))
		for log in logs:_logger.info('    %s',log)
		if logs:send_logs(cloud_conn,logs);_logger.info('  - sent=%s',len(logs))
		_logger.debug('-'*40)
		if sleep:time.sleep(sleep)
		else:break
if __name__=='__main__':out=logging.StreamHandler(sys.stdout);logging.basicConfig(filename='dtr_sync.log');_logger.setLevel(logging.INFO);ecb_conn=OdooXmlRpc('http://192.168.1.99:8069','ECB_ERP2','admin','adminpass1234');cloud_conn=OdooXmlRpc('https://ez4.eztechsoft.com','ecb_test','admin','pass1234');sync_dtr_logs(ecb_conn,cloud_conn,sleep=0)