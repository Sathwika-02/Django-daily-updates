from rest_framework import serializers
from .models import Student,Article
import re
from django.contrib.auth.models import User
class StudentSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    roll=serializers.IntegerField()
    city=serializers.CharField(max_length=100)

    def create(self,validate_data):
        return Student.objects.create(**validate_data)
    
    def validate(self, validate_data):
        if validate_data.get('name'):
            name=validate_data['name']
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if not regex.search(name)==None:
                raise serializers.ValidationError('name cannot contain special characters')
               
            

class ArticleSerializer(serializers.ModelSerializer):
      """title=serializers.CharField(max_length=100)
      author=serializers.CharField(max_length=100)
      email=serializers.EmailField(max_length=100)
      date=serializers.DateTimeField()
      
      def create(self,validate_data):
        return Article.objects.create(**validate_data)
    
      def update(self,instance,validate_data):
          instance.title=validate_data.get('title',instance.title)
          instance.author=validate_data.get('title',instance.author)
          instance.email=validate_data.get('title',instance.email)
          instance.date=validate_data.get('title',instance.date)
          instance.save()
          return instance"""
      
      class Meta:
          model=Article
          fields='__all__'

class Userserialzer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    def create(self,validated_data):
        user=User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user