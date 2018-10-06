from flask_restplus import Namespace, Resource, fields
from db_layer.db_operations import *
from auth import *

api = Namespace('ManageContactBook', description='Manage Contact Book')

contact_book_model =  api.model("manage_contact", {
    "first_name": fields.String("First name of the person."),
    "last_name": fields.String("Last name of the person."),
    "phone_number": fields.String("Phone of the person."),
    "email_id": fields.String("Email-ID of the person.")
})

update_contact_book_model = api.model("update_book", {
	"contact_id": fields.Integer("Id Of Contact"),
    "first_name": fields.String("First name of the person."),
    "last_name": fields.String("Last name of the person."),
    "phone_number": fields.String("Phone of the person."),
    "email_id": fields.String("Email-ID of the person.")
})

# remove_contact_model = 

BaseResponse = {
	"data" : None,"ErrMsg":None
}

NewContactAddResponse = {"data" : {
		"ContactId":None,
		"Msg": None
	},
	"ErrMsg":None,
	"StatusCode":1
}

UpdateContactDetailResponse = {
	"data" :{
		"Msg" : None
	},
	"ErrMsg": None,
	"StatusCode":1
}

RemoveContactResponse = {
	"data":{
		"Msg" : None
	},
	"ErrMsg": None,
	"StatusCode":1
}

@api.route('/Add')
class AddContact(Resource):
	@api.expect(contact_book_model,envelope='data')
	@api.doc(security='apikey')
	@AccessTokenRequired
	def post(self,headers=None):
		"""
		add new contact to the phone book
		"""
		request_payload = api.payload
		is_valid_phn,is_valid_email =  contact_details_validation(**request_payload)
		if is_valid_email and is_valid_phn:
			db_response = add_new_contact(**request_payload)
			if db_response["is_added"]:
				NewContactAddResponse["data"]["ContactId"] = str(db_response["ID"])
			# 	NewContactAddResponse["data"]["Msg"] = str(db_response["ErrMsg"])
			# else:
			# 	NewContactAddResponse["data"]["Msg"] = str(db_response["ErrMsg"])
			NewContactAddResponse["data"]["Msg"] = str(db_response["ErrMsg"])
		elif is_valid_phn == False and is_valid_email:
			NewContactAddResponse["data"]["Msg"] = "Please Pass Valid Phone Number."
			NewContactAddResponse["StatusCode"] = -1
		elif is_valid_email == False and is_valid_phn:
			NewContactAddResponse["data"]["Msg"] = "Please Pass Valid Email Id."
			NewContactAddResponse["StatusCode"] = -1
		else:
			NewContactAddResponse["data"]["Msg"] = "Please Pass Valid Email Id and Phone Number."
			NewContactAddResponse["StatusCode"] = -1
		return NewContactAddResponse, 201

@api.route('/Edit')
class EditContactBook(Resource):
	@api.expect(update_contact_book_model,envelope='data')
	@api.doc(security='apikey')
	@AccessTokenRequired
	def put(self,headers=None):
		"""
		edit existing contact detail pass valid contact-id
		"""
		request_payload = api.payload
		is_valid_phn,is_valid_email =  contact_details_validation(**request_payload)
		if is_valid_email and is_valid_phn:
			db_response = update_contact_details(**request_payload)
			UpdateContactDetailResponse["data"]["Msg"] = str(db_response["ErrMsg"])
			# if db_response["is_updated"]:
			# else:
			# 	UpdateContactDetailResponse["data"]["Msg"] = str(db_response["ErrMsg"])
		elif is_valid_phn == False and is_valid_email:
			UpdateContactDetailResponse["data"]["Msg"] = "Please Pass Valid Phone Number."
			UpdateContactDetailResponse["StatusCode"] = -1
		elif is_valid_email == False and is_valid_phn:
			UpdateContactDetailResponse["data"]["Msg"] = "Please Pass Valid Email Id."
			UpdateContactDetailResponse["StatusCode"] = -1
		else:
			UpdateContactDetailResponse["data"]["Msg"] = "Please Pass Valid Email Id and Phone Number."
			UpdateContactDetailResponse["StatusCode"] = -1
		return UpdateContactDetailResponse, 200

@api.route('/<int:id>/')
class RemoveContact(Resource):
    # @api.marshal_with(remove_contact_model,envelope='data')
    @api.doc(security='apikey')
    @AccessTokenRequired
    def get(self,id):
        """
        remove a contact from contact book
        """
        db_response = remove_contact(**{"contact_id":str(id)})
        RemoveContactResponse["data"]["Msg"] = str(db_response["ErrMsg"])
        return RemoveContactResponse,200

def contact_details_validation(*args,**kwargs):
	pass
	import re
	phone_number = str(kwargs["phone_number"]) if "phone_number" in kwargs.keys() else None
	email_id = str(kwargs["email_id"]) if "email_id" in kwargs.keys() else None
	is_valid_phn = False
	is_valid_email = False
	if phone_number:
		if len(phone_number) == 10 and phone_number.isdigit():
			is_valid_phn = True
	else:
		is_valid_phn = True
	if email_id:
		if re.match(r"[^@]+@[^@]+\.[^@]+",email_id):
			is_valid_email = True
	else:
		is_valid_email = True
	return is_valid_phn,is_valid_email