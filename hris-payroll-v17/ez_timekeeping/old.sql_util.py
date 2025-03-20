'\nINSERT INTO ir_logging(create_date, create_uid, type, dbname, name, level, message, path, line, func)\nVALUES (NOW() at time zone \'UTC\', %s, %s, %s, %s, %s, %s, %s, %s, %s)\n(self.env.uid, \'server\', self._cr.dbname, __name__, level, message, "action", action.id, action.name))\n'
def sql_single_insert(env,table,data):A=sql_insert(env.cr,env.uid,table,[data]);A+=' RETURNING id;';return A
def fast_insert(env,table,data):B=table;A=env;C=sql_insert(A.cr,A.uid,B,data);A.cr.execute(C);A[B].invalidate_cache()
def sql_insert(cr,uid,table,data):
	B=table;F=[];B=B.replace('.','_');A=set()
	for C in data:H=set(C.keys());A=A.union(H)
	D=[]
	for G in A:D.append('%s')
	D.append('%s')
	for C in data:
		E=[]
		for G in A:E.append(C.get(G))
		E.append(uid);I='('+', '.join(D)+", NOW() at time zone 'UTC')";F.append(cr.mogrify(I,tuple(E)).decode('utf-8'))
	J='INSERT INTO %s\n(%s, create_uid, create_date)\nVALUES\n%s'%(B,', '.join(A),',\n'.join(F));return J