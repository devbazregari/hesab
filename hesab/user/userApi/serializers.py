from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.models import User
from user.models import MessageBox
from rest_framework.validators import UniqueValidator

class UserRegistretaionSerizalizers(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,required=True)
    mobile = serializers.CharField(validators=[UniqueValidator(User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(User.objects.all())])

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("can't validate data")
        return attrs
    
    def create(self, validated_data):
        user = User(
            mobile = validated_data['mobile'],
            username = validated_data['username'],
            media = validated_data['media']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserMessageSerializers(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('get_time_of_message')
    class Meta:
        model = MessageBox
        fields = ['sender','receiver','message','time']

    def get_time_of_message(self,obj):
        return obj.created_on
