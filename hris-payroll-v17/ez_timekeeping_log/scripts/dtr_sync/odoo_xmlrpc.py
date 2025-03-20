import xmlrpclib
class OdooXmlRpc:
	def __init__(A,url,db,username,password):A.url=url;A.db=db;A.username=username;A.password=password;A.sock=False;A.uid=0
	def connect(A):B=xmlrpclib.ServerProxy('%s/xmlrpc/common'%A.url);A.uid=B.login(A.db,A.username,A.password);A.sock=xmlrpclib.ServerProxy('%s/xmlrpc/object'%A.url)
	def execute(A,*B):return A.sock.execute(A.db,A.uid,A.password,*B)