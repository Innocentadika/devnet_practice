import requests

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
