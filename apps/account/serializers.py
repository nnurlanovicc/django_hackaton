from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code
from django.core.mail import send_mail


User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    about = serializers.CharField(required=False)
    link = serializers.CharField(required=False)



    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('пользователь с таким username уже зарегистрирован')
        return username

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs
    

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)        
        return user
        



class ActivationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True) 

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('code')
        email = attrs.get('email')
        if not User.objects.filter(username=username,email=email,activation_code=code).exists():
            raise serializers.ValidationError('не стоит температурить джеки чан')
        return attrs
    

    def activate(self):
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        user = User.objects.get(username=username,email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_username(self,username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return username
    
    def validate(self, attrs):
        request = self.context.get('request')
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(username=username, password=password, request=request)
            if not user:
                raise serializers.ValidationError('Неправильный username или password')
        else:
            raise serializers.ValidationError('username и password обязательны для заполнения')
        attrs['user'] = user
        return attrs
        



class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class ChangePasswordSerializer(
    serializers.Serializer):
    old_password = serializers.CharField(min_length=8, required=True)
    new_password = serializers.CharField(min_length=8, required=True)
    new_password_confirm = serializers.CharField(min_length=8, required=True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError('святой отец ведите правильный пароль')
        return old_password

    def validate(self, attrs):
        old_pass = attrs.get('old_password')
        new_pass1 = attrs.get('new_password')
        new_pass2 = attrs.get('new_password_confirm')
        if new_pass2 != new_pass1:
            raise serializers.ValidationError('просто повторите первый пороль, что в этом сложного')

        if old_pass == new_pass1:
            raise serializers.ValidationError('Пароли совпадают')
        return attrs

    def set_new_password(self):
        new_pass = self.validated_data.get(
            'new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_email_username(self, email,username):
        if not User.objects.filter(email=email,username=username).exists():
            raise serializers.ValidationError('не правильный email или username')
        return email,username

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail('Восстановление пароля',f'Ваш код восстановления: {user.activation_code}',
                    'example@gmail.com',[user.email])


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('code')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if not User.objects.filter(username=username,activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден или неправильный код')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        username = self.validated_data.get('username')
        password = self.validated_data.get('password')
        user = User.objects.get(username=username)
        user.set_password(password)
        user.activation_code = ''
        user.save()