from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from JTbackend.firebase import auth as firebase_auth, db
from django.contrib.auth.models import AnonymousUser, User

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split('Bearer ')[1]

        try:
            decoded_token = firebase_auth.verify_id_token(id_token, clock_skew_seconds=20)
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            

            # Fake user object just for compatibility
            user = type('User', (), {})()
            user.email = email
            user.uid = uid
            user.is_authenticated = True

            # Check if Firebase custom claim exists
            user_doc = db.collection('users').document(uid).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                role = user_data.get('role', 'user')

                user.role = role
                user.is_superAdmin = role == 'superAdmin'
                user.is_admin = role == 'admin'
                user.is_moderator = role == 'moderator'
                user.is_user = role == 'user'
            else:
                user.role = 'user'
                user.is_superAdmin = False
                user.is_admin = False
                user.is_moderator = False
                user.is_user = True

            # print(f"[ROLE CHECK] User: {email}, UID: {uid}, is_superAdmin: {user.is_superAdmin}, Claims: {decoded_token}")

            return (user, None)

        except Exception as e:
            raise AuthenticationFailed(f"Invalid Firebase token: {e}")

# -----------------------------------------
# Profile update
# -----------------------------------------
@api_view(['POST', 'PATCH'])
@authentication_classes([FirebaseAuthentication])
def update_user_profile(request):
    serializer = ProfileSerializer(data=request.data, partial=True)

    if serializer.is_valid():
        uid = request.user.uid

        try:
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            phone = serializer.validated_data.get('phone')
            location = serializer.validate_data.get('location')
            payment_method = serializer.validated_data.get('payment_method')

            if username:
                firebase_auth.update_user(uid, display_name=username)

            update_data = {}
            if username:
                update_data['username'] = username
            if phone:
                update_data['phone'] = phone
            if location:
                update_data['location'] = location
            if payment_method:
                update_data['payment_method'] = payment_method

            if update_data:
                db.collection('users').document(uid).update(update_data)

            return Response({'message': 'Profile updated successfully'}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=400)

    return Response(serializer.errors, status=400)
            