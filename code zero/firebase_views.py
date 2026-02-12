import requests
from google.cloud.firestore import SERVER_TIMESTAMP
from .firebase_authentication import FirebaseAuthentication
from .supabase_client import supabase
from JTbackend.firebase import auth as firebase_auth, db
import uuid

@api_view(['POST'])
def create_admin(requests):
    serializer = UserSerializer(data=requests.data)
    if serializer.is_valid():
        username = serializer.validated_data['email']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user_record = firebase_auth.create_user(
                email=email,
                password=password,
                display_name=username
            )

            db.collection('user').document(user_record.uid).set({
                'email': email,
                'password': password,
                'created_at': SERVER_TIMESTAMP,
                'role': 'admin'
            })

            return Response({"message": "User created successfully", "uid": user_record.uid} status=status_code.HTTP_201_CREATED)
        
        except firebase_auth.EmailAlreadyExistsError:
            return Response({"message": "User already exists", "uid": user_record.uid} status=status.HTTP_400_BAD_REQUEST)
        except firebse_auth.FirebaseErrors as e:
            return Response({"error": f"Firebase terminated: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------
# Fetching users connected to the system
# ------------------------------------
@api_view(['GET'])
@authentication_classes([FirebaseAuthentication])
def get_users(request):
    user = request.user

    if not getattr(user, 'is_authenticated', False):
        return Response({"error": "Login required."}, status=401)
    
    if not (getattr(user, 'is_admin', False) or getattr(user, 'is_superAdmin', False)):
        return Response({"error": "Login required as an admin or superAdmin."}, status=403)
    
    try:
        user = []
        docs = db.collection('Users').stream()
        for doc in docs:
            data = doc.to_dict()
            data['uid'] = doc.id
            user.append(data)

        return Response(users, status=200)
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
# ------------------------------------
# promoting users connected to the system
# ------------------------------------
@api_view(['POST'])
@authentication_classes([FirebaseAuthentication])
def promote_user(request):
    user = request.user

    if not getattr(user, 'is_superAdmin', False):
        return Response({"error": "You are not authorized to update roles."}, status=403)
    
    uid = request.data.get('uid')
    new_role = request.data.get('role')

    ALLOWED_ROLES = ['user', 'admin', 'moderator', 'superAdmin']
    if not uid or not new_role:
        return Response({"error": "UID and role are required."}, status=400)
    if new_role not in ALLOWED_ROLES:
        return Response({"error": "Invalid role."}, status=400)
    
    try:
        user_ref = db.collection('Users').document(uid)
        if not user_ref.get().exists():
            return Response({"error": "User not found."}, status=404)
        
        # Update the role field
        user_ref.update({'role': new_role})

        return Response({"message": f"User role updated to '{new_role}' successfully."}, status=200)
    
    except Exception as e:
        return Response({"Failed to update user": str(e)}, status=400)