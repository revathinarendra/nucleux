from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Account
from django.contrib.auth.password_validation import validate_password
from .models import  UserProfile, Referral, Objectives, University, Profession
from django.utils.http import  urlsafe_base64_decode
from django.utils.encoding import  force_str
from django.contrib.auth.tokens import default_token_generator


Account = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.ChoiceField(choices=Account.GENDER_CHOICES, required=True)
    referral = serializers.PrimaryKeyRelatedField(queryset=Referral.objects.all(), required=False)
    objectives = serializers.PrimaryKeyRelatedField(queryset=Objectives.objects.all(), required=False)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all(), required=False)
    profession = serializers.PrimaryKeyRelatedField(queryset=Profession.objects.all(), required=False)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = [
            "first_name", "last_name", "date_of_birth", "gender", "username", "email", "phone_number",
            "referral", "profession", "university", "expected_graduation_date", "current_area_of_focus",
            "objectives", "password", "confirm_password"
        ]
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 6, 'write_only': True},
        }

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        # Pop confirm_password and other related fields
        validated_data.pop('confirm_password')
        date_of_birth = validated_data.pop('date_of_birth')
        gender = validated_data.pop('gender')

        # Extract additional fields for user profile
        # referral = validated_data.pop('referral', None)
        # objectives = validated_data.pop('objectives', None)
        # university = validated_data.pop('university', None)
        # profession = validated_data.pop('profession', None)

        # Create the user
        user = Account.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', None),
            is_active=False  # User is not active until email is verified
        )

        # Create the associated UserProfile
        # UserProfile.objects.create(
        #     user=user,
            # date_of_birth=date_of_birth,
            # gender=gender,
            # referral=referral,
            # objectives=objectives,
            # university=university,
            # profession=profession,
            # expected_graduation_date=validated_data.get('expected_graduation_date', None),
            # current_area_of_focus=validated_data.get('current_area_of_focus', None),
        # )

        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# User Profile Serializer (for retrieving and updating profile)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'phone_number', 'profile_picture', 'city', 'state', 'country')

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(source='userprofile', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'user_profile')
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Account.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=6)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            raise serializers.ValidationError("Invalid token or user ID")
        
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid token")

        return data

    def save(self):
        uid = force_str(urlsafe_base64_decode(self.validated_data['uidb64']))
        user = Account.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            if not Account.objects.filter(email=email).exists():
                raise serializers.ValidationError('No user found with this email address.')

        return data
class UserProfileEditSerializer(serializers.ModelSerializer):
    user = SignUpSerializer(required=False) 
 
    # Fields from the Account model
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    #phone_number = serializers.CharField(required=False)
    referral = serializers.PrimaryKeyRelatedField(queryset=Referral.objects.all(), required=False)
    objectives = serializers.PrimaryKeyRelatedField(queryset=Objectives.objects.all(), required=False)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all(), required=False)
    profession = serializers.PrimaryKeyRelatedField(queryset=Profession.objects.all(), required=False)
    expected_graduation_date = serializers.DateField(required=False)
    current_area_of_focus = serializers.PrimaryKeyRelatedField(queryset=Objectives.objects.all(), required=False)

    class Meta:
        model = UserProfile
        fields = [
            "first_name", "last_name", "email",   "user",
             "profile_picture",  "country",  # UserProfile fields
            "referral", "objectives", "university", "profession", "expected_graduation_date", "current_area_of_focus"
        ]

    def update(self, instance, validated_data):
        # Update UserProfile fields
        userprofile_fields = [
             "profile_picture", "city", "state", "country"
        ]
        for field in userprofile_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        # Update Account fields
        account_fields = [
            "first_name", "last_name", "email", "phone_number", "referral", "objectives",
            "university", "profession", "expected_graduation_date", "current_area_of_focus"
        ]
        account = instance.user  # Access the related Account object
        for field in account_fields:
            if field in validated_data:
                setattr(account, field, validated_data[field])

        # Save changes
        instance.save()
        account.save()
        return instance

    
from rest_framework import serializers
from .models import Referral, Profession, Objectives, University

# Serializer for Referral
class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'

# Serializer for Profession
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'

# Serializer for Objectives
class ObjectivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectives
        fields = '__all__'

# Serializer for University
class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'country_name', 'university_name']

# Parent Serializer to group all data
class UniversityDataSerializer(serializers.Serializer):
    universities = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()
    professions = serializers.SerializerMethodField()
    objectives = serializers.SerializerMethodField()

    class Meta:
        fields = ['universities', 'referrals', 'professions', 'objectives']

    def get_universities(self, obj):
        universities = University.objects.all()
        return UniversitySerializer(universities, many=True).data

    def get_referrals(self, obj):
        referrals = Referral.objects.all()
        return ReferralSerializer(referrals, many=True).data

    def get_professions(self, obj):
        professions = Profession.objects.all()
        return ProfessionSerializer(professions, many=True).data

    def get_objectives(self, obj):
        objectives = Objectives.objects.all()
        return ObjectivesSerializer(objectives, many=True).data



