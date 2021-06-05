from rest_framework import serializers,validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth.models import User as AuthUser
from application.models import *
import json, re, logging

logger = logging.getLogger('django')


class RegisterSerializer(serializers.ModelSerializer):

    mobileno = serializers.CharField(source='username')
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()



    class Meta:
            model = AuthUser
            error_messages = {"mobileno": {"required": "Please enter a valid mobile number"}}
            fields = ['first_name','last_name','email','password','mobileno']


    def validate_first_name(self,first_name):
        if len(first_name)>0:
            return first_name
        else:
            raise serializers.ValidationError("first name cannot be empty")
    

    def validate_last_name(self,last_name):
        if len(last_name)>0:
            return last_name
        else:
            raise serializers.ValidationError("last name cannot be empty")


    def validate_email(self,email):
        user = AuthUser.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError("email already exists")
        else:
            return email

    
    def validate_mobileno(self,mobileno):
        user = AuthUser.objects.filter(username=mobileno).first()
        if user:
            pass

        Pattern = re.compile("^[0-9]*$")
        if Pattern.match(mobileno):
            return mobileno
        
        else:
            logger.info('invalid')
            raise serializers.ValidationError("invalid mobile number")



class MultiFieldJWTSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        user =  AuthUser.objects.filter(username=attrs.get("username")).first()
        
        if user:
            credentials['username'] = user.username
        reply = {}

        try:
            data = super().validate(credentials)
            print(json.dumps(data))
            reply['status'] = "SUCCESS"
            data['user'] = str(user.id)
            reply['data'] = data
        
        except Exception as ex:
            reply['status'] = "ERROR"
            reply['message'] = str(ex)
            reply['error_code'] = "AUTH_ERROR"

        return reply
    

class CustomRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'access': str(refresh.access_token)}
        data['expiry'] = (refresh.lifetime + refresh.current_time).timestamp()

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)
        return data




class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = '__all__'


class DepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = '__all__'

class WithdrawnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Withdrawn
        fields = '__all__'