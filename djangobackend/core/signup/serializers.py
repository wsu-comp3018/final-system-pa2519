# from rest_framework import serializers
# from accounts.models import User

# class UserSerializer(serializers.ModelSerializer):
#     password=serializers.CharField(write_only=True)
#     confirm_password=serializers.CharField(write_only=True)

#     class Meta:
#         model=User
#         fields=["first_name","last_name","email","password","confirm_password"]

#     def validate(self,attrs):
#         password=attrs.get('password')
#         confirm_password=attrs.get('confirm_password')

#         if password!=confirm_password:
#             raise serializers.ValidationError("Password and Confirm_Password " \
#                                               "do not match.")
#         return attrs
    
#     def validate_email(self,value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError('User with this email already exists.')
#         return value
    
#     def create(self, validated_data):
#         user=User.objects.create_user(
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             password=validated_data['password'],
#         )
#         user.is_active=False
#         user.save()
#         return user

