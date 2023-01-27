from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.models import User
from rest_framework.validators import UniqueValidator

class UserRegistretaionSerizalizers(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,required=True)
    mobile = serializers.CharField(validators=[UniqueValidator(User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(User.objects.all())])

    class Meta:
        model = User
        fields = ['username','mobile','password','password2']

    def validate(self, attrs):
        print(attrs)
        print('salam')
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("can't validate data")
        return attrs
    
    def create(self, validated_data):

        print(validated_data)
        print('by')
        user = User(
            mobile = validated_data['mobile'],
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user