from rest_framework.decorators import api_view
from rest_framework.response import Response
from knox.auth import AuthToken
from .serializers import UserRegistretaionSerizalizers


@api_view(['POST',])
def register(request):
    if request.method == 'POST':
        serializer = UserRegistretaionSerizalizers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _,token = AuthToken.objects.create(user)
        return Response({
            'user_id':user.pk,
            'mobile':user.mobile,
            'token':token,
        })