from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from knox.auth import AuthToken
from .serializers import ( UserRegistretaionSerizalizers, DebtSerializers,UserMessageSerializers )
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView ,GenericAPIView , ListAPIView , UpdateAPIView , DestroyAPIView
from .mixins import MultipleFieldLookupMixin
from user.models import MessageBox , User , Debt
from rest_framework.authtoken.serializers import AuthTokenSerializer
from hesab.celery import app
from user.tasks import my_task
from django.http import HttpResponse 
from rest_framework import status
from rest_framework import mixins
from django.db.models import F
from rest_framework.pagination import PageNumberPagination

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
        request.data['sender'] = request.user.pk
        receiver = request.data['receiver']
        try:
            receiver_user = User.objects.filter(pk=receiver).update(notif=True)
            serializers = UserMessageSerializers(data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(
                "message been sended"
            )
        except:
            return Response("there isn't an receiver or sender with this credentials",status.HTTP_400_BAD_REQUEST)


class UpdateMessage(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMessageSerializers
    
    def update(self, request,**kwargs):
        request.data['sender']=request.user.pk
        instance = MessageBox.objects.filter(sender_id=request.data['sender']).filter(receiver_id=request.data['receiver']).filter(message=request.data['perv_message']).last()
        serializer = self.serializer_class(instance=instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message has changed"})

class DeleteMessage(MultipleFieldLookupMixin,DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMessageSerializers
    lookup_fields = ["message","receiver"]
    
    def get_queryset(self):
        return MessageBox.objects.filter(sender_id=self.request.user.pk)

    
   
class show_user_message(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMessageSerializers
    pagination_class = PageNumberPagination
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
            last_debt = Debt.objects.filter(debtor_id=debtor.pk).filter(creditor_id=creditor.pk).last()
            last_debt.money += money
            last_debt.save()
            return Response(
            "debt been sended",status.HTTP_200_OK
            )
            
        Debt.objects.create(debtor=debtor,creditor=creditor,money=money)
        return Response("debt been sended",status.HTTP_200_OK)


class UpdateDebts(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DebtSerializers
    
    def update(self, request,**kwargs):
        try:
            debtor = User.objects.get(mobile=kwargs['mobile'])
            instance = Debt.objects.filter(creditor_id=request.user.pk).filter(debtor_id=debtor.pk).last()
            serializer = self.serializer_class(instance=instance,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"debt has changed"})
        except:
            raise serializers.ValidationError("false credentials")

class DeleteDebts(MultipleFieldLookupMixin,DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMessageSerializers
    lookup_fields = ["money","debtor"]

    def get_queryset(self):
        return Debt.objects.filter(creditor_id=self.request.user.pk)


class ShowDebt(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DebtSerializers
    pagination_class = PageNumberPagination
    def get_queryset(self):
        debtor = User.objects.get(mobile=self.kwargs['mobile'])
        debtor_user = Debt.objects.filter(debtor_id=debtor.pk).filter(creditor_id=self.request.user.pk).all()
        return debtor_user

class ShowMyDebt(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DebtSerializers
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if Debt.objects.filter(debtor_id=self.request.user.pk).exists():
            all_debts = Debt.objects.filter(debtor_id=self.request.user.pk).all()
            debts = []
            for obj in Debt.objects.filter(debtor_id=self.request.user.pk).all():
                debts.append(obj)
            return debts
        raise serializers.ValidationError("you haven't debt yet bro ")


class SendWarning(CreateAPIView):    
    permission_classes = (IsAuthenticated,)
    serializer_class = DebtSerializers

    def post(self,request):
        my_task.delay({"range":request.data['range'],"creditor_id":request.user.pk}) 
        return HttpResponse('hello')
