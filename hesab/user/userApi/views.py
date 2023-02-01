from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from knox.auth import AuthToken
from .serializers import UserRegistretaionSerizalizers, DebtSerializers, UserMessageSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView , ListAPIView
from user.models import MessageBox , User , Debt
from rest_framework.authtoken.serializers import AuthTokenSerializer
from hesab.celery import app
from user.tasks import my_task
from django.http import HttpResponse
from rest_framework import status
from django.db.models import F


class register(CreateAPIView):
    def post(self, request):
        print(request.data)
        serializer = UserRegistretaionSerizalizers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _,token = AuthToken.objects.create(user)
        return Response({
            'user_id':user.pk,
            'mobile':user.mobile,
            'token':token,
        })


class login(CreateAPIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        _,token = AuthToken.objects.create(user)
        return Response({
            'username':user.username,
            'token':token
        })


class send_user_message(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        receiver = request.data['receiver']
        receiver_user = User.objects.filter(pk=receiver).update(notif=True)
        serializers = UserMessageSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(
            "message been sended"
        )

class show_user_message(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMessageSerializers
    def get_queryset(self):
        User.objects.filter(pk=self.request.user.id).update(notif=False)
        return MessageBox.objects.filter(receiver=self.request.user.id).all()


class SaveDebt(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            debtor = User.objects.get(pk=request.data['debtor'])
            creditor = User.objects.get(pk=request.data['creditor'])
            money = request.data['money']
        except:
            return Response("the user doesn't exist",status.HTTP_404_NOT_FOUND)

        if Debt.objects.filter(debtor_id=debtor.pk).filter(creditor=creditor.pk):
            print('inja')
            last_debt = Debt.objects.filter(debtor_id=debtor.pk).filter(creditor_id=creditor.pk).last()
            last_debt.money += money
            last_debt.save()
            return Response(
            "debt been sended",status.HTTP_200_OK
            )
            
        Debt.objects.create(debtor=debtor,creditor=creditor,money=money)
        return Response("debt been sended",status.HTTP_200_OK)






def home(request):
    my_task.delay()
    return HttpResponse('hello')
