from __future__ import print_function
import odoorpc
class OdooConnection:
	def __init__(A,host,port,admin_pwd,super_password,admin='admin',lang='en_US'):A.host=host;A.port=int(port);A.admin_password=admin_pwd;A.super_password=super_password;A.language=lang;A.admin=admin
	def get_session(A,db,user=None,pwd=None,login=True,timeout=None):
		D=pwd;C=user
		if A.port==443:B=odoorpc.ODOO(A.host,port=A.port,protocol='jsonrpc+ssl')
		else:B=odoorpc.ODOO(A.host,port=A.port)
		B.config['timeout']=timeout
		if login:
			if not C:C=A.admin
			if not D:D=A.admin_password
			B.login(db,C,D)
		return B
	def backup_database(C,db_name,filename,timeout=1200):
		D=filename;A=db_name;print('Backup database %s...'%A);B=C.get_session(A,login=False)
		if A not in B.db.list():print('    Backup failed! Database',A,'does not exists.');return
		print('    Downloading database %s...'%A);E=B.config['timeout'];B.config['timeout']=timeout;F=B.db.dump(C.super_password,A);B.config['timeout']=E;print('    Downloading database %s done. Writing to zip file %s.'%(A,D))
		with open(D,'wb')as G:G.write(F.read())
		print('    Backup done.')
	def duplicate_database(D,db_name,new_db_name):
		B=new_db_name;A=db_name;C=D.get_session(A,login=False)
		if A not in C.db.list():print('Duplicate failed! Source database',A,'does not exists.');return
		if B in C.db.list():print('Duplicate failed! Target database',A,'already exists.');return
		print('Duplicating database',A,'...');C.db.duplicate(D.super_password,A,B);print('    Database',A,'duplicated to',B,'.');print()
	def create_database(B,db_name,demo=False):
		A=db_name;C=B.get_session(A,login=False)
		if A not in C.db.list():print('Creating database',A,'...');C.db.create(B.super_password,A,demo=demo,lang=B.language,admin_password=B.admin_password);print('Database',A,'created.');print();return True
		else:print('Create failed! Database',A,'already exists.');print();return False
	def drop_database(B,db_name):
		A=db_name;C=B.get_session(A,login=False)
		if A in C.db.list():C.db.drop(B.super_password,A);print('Database',A,'dropped.')
		else:print('Database',A,'do not exist.')
		print()
	def uninstall_modules(F,db_name,module_names):
		C=module_names;B=db_name;print('Uninstall modules on %s: %s'%(B,C));G=F.get_session(B);D=G.env['ir.module.module']
		for A in C:
			E=D.search([('name','=',A),('state','in',['installed','to upgrade','to remove','to install'])]);print('Uninstalling module',A,'...')
			if E:D.button_immediate_uninstall(E);print('    Module',A,'uninstalled.')
			else:print('    Module',A,'was not installed')
		print()
	def install_modules(F,db_name,modules):
		D=modules;C=db_name;print('Install modules on %s: %s'%(C,D));G=F.get_session(C);E=G.env['ir.module.module']
		for A in D:
			B=E.search([('name','=',A),('state','not in',['installed','to upgrade'])]);print('Installing module',A,'...',B)
			if B:E.button_immediate_install(B);print('    Module',A,'installed.')
			else:print('    Module',A,'was not installed. Might already be installed.')
		print()
	def upgrade_modules(F,db_name,modules):
		D=modules;C=db_name;print('Upgrade modules on %s: %s'%(C,D));G=F.get_session(C);E=G.env['ir.module.module']
		for A in D:
			B=E.search([('name','=',A),('state','in',['installed','to upgrade'])]);print('Upgrading module',A,'...',B)
			if B:E.button_immediate_upgrade(B);print('    Module',A,'upgraded.')
			else:print('    Module',A,'was not upgraded.')
		print()
	def update_module_list(B,db_name):A=db_name;print('Update module list on %s.'%A);C=B.get_session(A);D,E=C.env['ir.module.module'].update_list();print('    %s: %s modules updated, %s modules new'%(A,D,E));print()
if __name__=='__main__':conn=OdooConnection('localhost','8069','pass1234','passw0rd');conn.create_database('dbtest0');conn.duplicate_database('dbtest0','dbtest1');conn.uninstall_modules('dbtest1',['im_chat','im_livechat','im_odoo_support']);conn.drop_database('dbtest0');conn.drop_database('dbtest1')