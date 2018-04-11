from rest_framework import serializers
from .models import User, Blog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'emailid', 'mobile', 'username', 'password',
                  'security_question','security_answer')
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields='__all__'