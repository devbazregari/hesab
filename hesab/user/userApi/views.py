from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from knox.auth import AuthToken
from .serializers import UserRegistretaionSerizalizers , UserMessageSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from user.models import MessageBox,User
from rest_framework.authtoken.serializers import AuthTokenSerializer

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
        serializers = UserMessageSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(
            "message been sended"
        )


