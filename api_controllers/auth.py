from flask_restplus import Namespace, Resource, fields
from flask_restplus import reqparse
from flask import request
import hashlib
from db_layer.db_operations import *

PlivoTokenKey = "PlivoCommunication"
DevelopmentKey = "YouKnowNothing"

api = Namespace('Auth', description='Get Access Token')

AuthModel = api.model("auth", {
    "SecretKey": fields.String("Pass Super Secret Key")
})

AuthResponse = {
	"data" : {
		"Token":None
	},
	"ErrMsg":None
}

def AccessTokenRequired(func):
    def decorated(*args,**kwargs):
        access_token = None
        parser = reqparse.RequestParser()
        # print request.headers
        if "X-API-KEY" in request.headers:
            access_token  = request.headers["X-API-KEY"]
        if not access_token:    
            return {"ErrMsg":"Access Token Is Missing."}, 401
        true_toke = get_md5_token(DevelopmentKey)
        if access_token != true_toke:
            return {"ErrMsg":"Access Token Is Wrong."}, 401
        return func(*args,**kwargs)
    return decorated

def get_md5_token(key):
    m = hashlib.md5()
    m.update(key)
    token = m.hexdigest()
    return token

@api.route('/')
class GetAuthToken(Resource):
    @api.expect(AuthModel,envelope='data')
    @api.doc(security=None)
    def post(self):
        """
        Generate Access Token
        """
        request_payload = api.payload
        requested_key = str(request_payload["SecretKey"])
        SuperSecretKey = get_secret_key()
        if requested_key == SuperSecretKey:
            # token = get_md5_token(PlivoTokenKey+SuperSecretKey)
            token = get_md5_token(DevelopmentKey+SuperSecretKey)
            AuthResponse["data"]["Token"] = token
        else:
            AuthResponse["ErrMsg"] = "Pass Valid SuperSecretKey"
        return AuthResponse, 200