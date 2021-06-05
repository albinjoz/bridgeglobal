from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User as AuthUser

from application.models import *
import application.serializer as app_ser
import json

from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    ser = app_ser.RegisterSerializer(data=request.data)
    reply = {}
    
    mobNum = request.POST.get("mobileno")
    if not ser.is_valid():
        for err in ser.errors:
           
            reply['message'] = ser.errors[err][0]
            reply['status'] = "ERROR"
            reply['error_code'] = "INVALID_"+err.upper()
            dict_obj = json.dumps(reply)
            return HttpResponse(dict_obj, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = AuthUser.objects.filter(username=mobNum).first()
        if user:
            user.first_name=ser.validated_data.get('first_name')
            user.last_name=ser.validated_data.get('last_name')
            user.email=ser.validated_data.get('email')
            user.set_password(request.POST.get('password'))
            user.save()
            
        else:
            user = ser.save()
            user.set_password(request.POST.get('password'))
            user.save()

        pass
    except Exception as e:
        print(str(e))
        reply['status'] = "ERROR"
        reply['message'] = "Server: User not created. Please contact support or retry."
        reply['error_code'] = "DB_CREATE_FAILED"
        dict_obj = json.dumps(reply)
        return HttpResponse(json.dumps(reply), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    reply['status'] = "SUCCESS"
    reply['message'] = "Signup was sucessful"
    dict_obj = json.dumps(reply)
    return HttpResponse(dict_obj, status=status.HTTP_201_CREATED)



class WalletViewset(viewsets.ModelViewSet):

    queryset = Wallet.objects.all()
    model = Wallet
    serializer_class = app_ser.WalletSerializer

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print (str(e))


    def patch(self, request, pk):
        instance = self.get_object(pk)
        
        # set partial=True to update a data partially
        serializer = app_ser.WalletSerializer(instance, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(data="Bad Request", status=status.HTTP_400_BAD_REQUEST)




class DepositViewset(viewsets.ModelViewSet):

    queryset = Deposit.objects.all()
    model = Deposit
    serializer_class = app_ser.DepositSerializer

    def create(self, request):
        try:
            wallet = Wallet.objects.get(id = request.data['wallet_id'])
            if wallet.status == "disabled":
                return Response('Wallet is disabled. please try again later', status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            wallet = Wallet.objects.get(id = serializer.data['wallet_id'])
            wallet.balance = wallet.balance + serializer.data['amount']
            wallet.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print (str(e))
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)



class WithdrawnViewset(viewsets.ModelViewSet):

    queryset = Withdrawn.objects.all()
    model = Withdrawn
    serializer_class = app_ser.WithdrawnSerializer

    def create(self, request):
        try:
            print(request.data['wallet_id'])
            wallet_obj = Wallet.objects.get(id = request.data['wallet_id'])
            
            if wallet_obj.status == "disabled":
                return Response('Wallet is disabled. please try again later', status=status.HTTP_403_FORBIDDEN)

            if(float(request.data['amount']) > wallet_obj.balance):
                return Response("INSUFFICIENT BALANCE", status = status.HTTP_406_NOT_ACCEPTABLE)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            wallet = Wallet.objects.get(id = serializer.data['wallet_id'])
            wallet.balance = wallet.balance - serializer.data['amount']
            wallet.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print (str(e))
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)