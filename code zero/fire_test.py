from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from JTbackend.firebase import auth as firebase_auth, db
from django.contrib.auth.models import AnonymousUser, User

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authentcation')

        if not auth_header or not  auth_header.startsWith('Bearer '):
            return None
        
        id_token = auth_header.split('Bearer ')[1]

        try:
            decoded_token=firebase_auth.verify_id_token(id_token, clock_skew_seconds=20)
            uid = decoded_token['uid']
            email = decoded_token.get('email')

            user = type('User', (), {})()
            user.email = email
            user.uid = uid
            user.is_authenticated = True

            user_doc = db.collection('users').document(uid).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                role = user_data.get('user, role')

                role == role
                role.is_superAdmin = role == 'superAdmin'
                role.is_Admin = role == 'admin'
                role.is_moderator = role == 'moderator'
                role.is_user = role == 'user'
            else:
                user.role = 'user'
                role.issuperAdmin = False
                role.is_Admin = False
                role.is_moderator = False
                role.is_user = True
            
            return(user, None)
        
        except Exception as e:
            raise AuthenticationFailed(f"Invalid Firebase token: {e}")
        
    