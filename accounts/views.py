from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from .serializers import LoginSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, SignUpSerializer, UserProfileEditSerializer, UserSerializer
from .models import Account, EmailVerificationToken  
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ViewSet
from .serializers import UniversityDataSerializer



#Registration View
User = get_user_model()
# @api_view(['POST'])
# def register(request):
#     data = request.data
#     user_serializer = SignUpSerializer(data=data)

#     if user_serializer.is_valid():
#         if not User.objects.filter(username=data['email']).exists():
#             user = user_serializer.save()
#             token = EmailVerificationToken.objects.create(user=user)
#             current_site = get_current_site(request).domain
#             verification_link = f"http://{current_site}{reverse('verify-email', kwargs={'token': token.token})}"
#             send_mail(
#                 'Verify your email address',
#                 f'Please click the link to verify your email: {verification_link}',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [user.email],
#                 fail_silently=False,
#             )
#             return Response({'message': 'User registered. Please verify your email.'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register(request):
    data = request.data
    user_serializer = SignUpSerializer(data=data)

    if user_serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = user_serializer.save()
            # Activate user by default
            user.is_active = True
            user.save()  # Save the updated is_active field
            
            # Skip sending email verification
            return Response({'message': 'User registered and activated successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        # Validate the token
        token_obj = get_object_or_404(EmailVerificationToken, token=token)

        if token_obj.is_expired():
            return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Activate the user
        user = token_obj.user
        user.is_active = True
        user.save()

        # Delete the token after successful verification
        token_obj.delete()

        # Redirect to frontend or return a response
        return redirect(settings.FRONTEND_URL)  


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:  # Check if the user's account is active
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Please verify your email before logging in.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get Current Logged-in User 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentUser(request):
    user = UserSerializer(request.user)
    return Response(user.data)


# Password Reset Request View
@api_view(['POST'])
def password_reset_request(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/resetpassword?uidb64={uidb64}&token={token}"
        
        send_mail(
            'Password Reset Request',
            f'Click the link below to reset your password:\n{reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Password Reset Confirm View
@api_view(['POST'])
def password_reset_confirm(request, uidb64, token):
    data = {
        'uidb64': uidb64,
        'token': token,
        'new_password': request.data.get('new_password')
    }
    serializer = PasswordResetSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile = request.user.userprofile  # Get the user's profile
        serializer = UserProfileEditSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UniversityViewSet(ViewSet):
    def list(self, request):
        # Create a single point of data aggregation
        data = {
            "universities": None,  # Placeholder for universities
            "referrals": None,     # Placeholder for referrals
            "professions": None,   # Placeholder for professions
            "objectives": None     # Placeholder for objectives
        }
        serializer = UniversityDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
