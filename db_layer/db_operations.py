##Author R@ghvendra
from make_db_connection import DB
from raw_queries_model import *
# global server_name
global_server = "localhost"

def add_new_contact(*args,**kwargs):
	db_response = {"is_added":False,"ID":None,"ErrMsg":None}
	if kwargs:
		try:
			db = DB(global_server)
			phn_number = str(kwargs["phone_number"])
			email_id = str(kwargs["email_id"])
			f_name = str(kwargs["first_name"])
			l_name = str(kwargs["last_name"]) if "last_name" in kwargs.keys() else ""
			##Check Unique Email and Uniq Phone number
			##Method 1 Scan Table For Email And Phone(Indexed Column)
			##Method 2 Get From Redis Cache
			is_phn_exists,is_email_exists =  is_phn_email_exists(phn_number,email_id)
			if is_phn_exists and is_email_exists:
				db_response["is_added"] = False
				db_response["ErrMsg"] = "Email-ID and Phone number already exists"				
			elif is_phn_exists and is_email_exists == False:
				db_response["is_added"] = False
				db_response["ErrMsg"] = "Phone number already exists"
			elif is_phn_exists == False and is_email_exists:
				db_response["is_added"] = False
				db_response["ErrMsg"] = "Email ID already exists"
			else:
				last_id = db.execute_query(ADD_NEW_CONTACT,params=(f_name,l_name,phn_number,email_id),execute_query=True,commit=True,return_result=True,return_id=True)
				db_response["is_added"] = True
				db_response["ID"] = int(last_id)
				db_response["ErrMsg"] = "Contact added successfully!!!!"
			return db_response
		except Exception as e:
			raise e
	return False

def update_contact_details(*args,**kwargs):
	db_response = {"is_updated":False,"ErrMsg":None}
	if kwargs:
		try:
			contact_id = int(kwargs["contact_id"])
			# print contact_id,type(contact_id)
			phn_number = str(kwargs["phone_number"]) if "phone_number" in kwargs.keys() else None
			email_id = str(kwargs["email_id"]) if "email_id" in kwargs.keys() else None
			f_name = str(kwargs["first_name"]) if "first_name" in kwargs.keys() else None
			l_name = str(kwargs["last_name"]) if "last_name" in kwargs.keys() else None
			##Get Detail From DB
			db = DB(global_server)
			contact_dtl = db.execute_query(GET_CONTACT_DETAILS,params=(contact_id),execute_query=True,commit=True,return_result=True)
			# print contact_dtl
			if phn_number == None:
				phn_number = str(contact_dtl[0]["phone_number"])
			if email_id == None:
				email_id = str(contact_dtl[0]["email_id"])
			if f_name == None:
				f_name = str(contact_dtl[0]["first_name"])
			if l_name == None:
				l_name = str(contact_dtl[0]["last_name"])
			# x = (f_name,l_name,phn_number,email_id,contact_id)
			# print x
			db.execute_query(UPDATE_CONTACT_DETAILS,params=(f_name,l_name,phn_number,email_id,contact_id),execute_query=True,commit=True,return_result=True)
			db_response["is_updated"] = True
			db_response["ErrMsg"] = "Contact details updated successfully!!!!"
		except Exception as e:
			raise e
	return db_response

def remove_contact(*args,**kwargs):
	pass
	try:
		db_response = {"is_deleted":False,"ErrMsg":None}
		contact_id = str(kwargs["contact_id"])
		db = DB(global_server)
		##Remove From Redis Cache If Exists -ToDo
		is_contact_id_exists = is_contact_exists(contact_id)
		if is_contact_id_exists:
			db.execute_query(REMOVE_CONTACT,params=(contact_id),execute_query=True,commit=True,return_result=True)
			db_response["is_deleted"] = True
			db_response["ErrMsg"] = "Contact details delete"
		else:
			db_response["ErrMsg"] = "Contact-Id does not Exists"
		return db_response
	except Exception as e:
		raise e

def is_phn_email_exists(phn_number,email_id):
	pass
	try:
		is_phn_exists = False
		is_email_exists = False
		db = DB(global_server)
		res = db.execute_query(CHECK_PHONE_NUMBER_EXISTS,params=(phn_number),execute_query=True,commit=True,return_result=True)
		if res:
			is_phn_exists = True
		res = db.execute_query(CHECK_EMAIL_EXISTS,params=(email_id),execute_query=True,commit=True,return_result=True)
		if res:
			is_email_exists = True
		return is_phn_exists,is_email_exists
	except Exception as e:
		raise e

def is_contact_exists(contact_id):
	try:
		is_contact_id_exists = False
		db = DB(global_server)
		res = db.execute_query(CHECK_CONTACT_ID_EXISTS,params=(contact_id),execute_query=True,commit=True,return_result=True)
		if res:
			is_contact_id_exists = True
		return is_contact_id_exists
	except Exception as e:
		raise e

def get_contact_details(email_id=None,first_name=None,page_count=None):
	db_response = {"ErrMsg":None,"data":None}
	try:
		db = DB(global_server)
		if email_id:
			res = db.execute_query(CHECK_EMAIL_EXISTS,params=(email_id),execute_query=True,commit=True,return_result=True)
		elif first_name:
			res = db.execute_query(GET_CONTACT_DETAILS_BY_FIRST_NAME,params=(first_name),execute_query=True,commit=True,return_result=True)
		else:
			res = db.execute_query(GET_CONTACT_DETAILS,params=(page_count),execute_query=True,commit=True,return_result=True)
		db_response["data"] = res
		return db_response
	except Exception as e:
		raise e

def get_secret_key():
	try:
		db = DB(global_server)
		auth_id = 1
		res = db.execute_query(GET_SECRET_KEY,params=auth_id,execute_query=True,commit=True,return_result=True)
		key = str(res[0]["auth_key"])
		return key
	except Exception as e:
		raise e