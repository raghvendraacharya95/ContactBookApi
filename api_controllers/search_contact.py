from flask_restplus import Namespace, Resource, fields
from flask_restplus import reqparse
from db_layer.db_operations import *
from manage_contact_book import *
from auth import *

DEFAULT_ROWS = 10

api = Namespace('SearchContact', description='Search Contact')

search_contact_model =  api.model("search_contact", {
    "email_id": fields.String(""),
    "first_name": fields.String(""),
    "page_count": fields.String("Page Count")
})

SearchResponse = {
	"data" : [],"ErrMsg" : None, "StatusCode": 1
}

parser = reqparse.RequestParser()
parser.add_argument('email_id', type=str)
parser.add_argument('first_name', type=str)
parser.add_argument('page_count', type=str)

# @api.route('/<string:email_id>/<string:first_name>/<int:page_count>')
@api.route('/')
class GetContactDetails(Resource):
	@api.expect(parser)
	@api.doc(security='apikey',params={'email_id': 'Email ID'})
	@AccessTokenRequired
	def get(self):
		"""
		search contact from contact book
		"""
		# switcher = {"email_id":None}
		##Note - Can Use dictionary as switcher to api - ToDo
		request = parser.parse_args()
		email_id = request["email_id"]
		first_name = request["first_name"]
		page_count = request["page_count"]
		# print request
		SearchResponse = {	"data" : [],"ErrMsg" : None, "StatusCode": 1}
		if email_id or (email_id and first_name):
			is_valid_email = contact_details_validation(**{"email_id":email_id})
			if is_valid_email:
				db_response = get_contact_details(email_id=email_id)
			else:
				SearchResponse["ErrMsg"] = "Please Pass Valid Email Id."
				SearchResponse["StatusCode"] = -1
		elif first_name:
			db_response = get_contact_details(first_name=first_name)
		else:
			##Default Case
			if page_count == None:
				page_count = 1
			db_response = get_contact_details(page_count=int(page_count)*DEFAULT_ROWS)
		if db_response["data"]:
			for item in db_response["data"]:
				# ContactDetailRes = {"ContactId"	: None,"FirstName"	: None,"LastName"	: None,"PhoneNumber":None,"EmailId"	: None}
				ContactDetailRes = {}
				ContactDetailRes["ContactId"] = int(item["id"])
				ContactDetailRes["FirstName"] = str(item["first_name"])
				ContactDetailRes["LastName"] = str(item["last_name"])
				ContactDetailRes["PhoneNumber"] = str(item["phone_number"])
				ContactDetailRes["EmailId"] = str(item["email_id"])
				SearchResponse["data"].append(ContactDetailRes)
		return SearchResponse, 200