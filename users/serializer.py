from rest_framework import serializers
from .models import User, Staff, Customer

class UserSerializer(serializers.ModelSerializer):
  class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 
            'phone_number', 'password', 'role'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}  # El rol no debería ser asignable en registro
        }
    
  def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user

  def create(self, validated_data):
    password = validated_data.pop('password')
    user = User(**validated_data)
    user.set_password(password)
    user.save()
    return user

  def update(self, instance, validated_data):
    password = validated_data.pop('password', None)
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    if password:
      instance.set_password(password)
    instance.save()
    return instance


class StaffSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Staff
    fields = ['id', 'user', 'restaurant', 'role', 'hire_date', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']

  def create(self, validated_data):
    user_data = validated_data.pop('user')
    user_serializer = UserSerializer(data=user_data)
    user_serializer.is_valid(raise_exception=True)
    user = user_serializer.save()
    staff = Staff.objects.create(user=user, **validated_data)
    return staff

  def update(self, instance, validated_data):
    user_data = validated_data.pop('user', None)
    if user_data:
      user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
      user_serializer.is_valid(raise_exception=True)
      user_serializer.save()
    for attr, value in validated_data.items():
      setattr(instance, attr, value)
    instance.save()
    return instance


class CustomerSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Customer
    fields = ['id', 'user', 'preferences', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']

  def create(self, validated_data):
    user_data = validated_data.pop('user')
    user_data['role'] = 'customer'  # Fijar el rol de forma segura

    user_serializer = UserSerializer(data=user_data)
    user_serializer.is_valid(raise_exception=True)
    user = user_serializer.save()

    return Customer.objects.create(user=user, **validated_data)

  def update(self, instance, validated_data):
    user_data = validated_data.pop('user', None)
    if user_data:
      user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
      user_serializer.is_valid(raise_exception=True)
      user_serializer.save()
    for attr, value in validated_data.items():
      setattr(instance, attr, value)
    instance.save()
    return instance

class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True, write_only=True, min_length=3)
