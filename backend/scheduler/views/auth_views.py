from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import User
from ..services import UserService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register(request):

    if request.user.role != 'admin':
        return Response(
            {'error': 'Only admins can create new users'},
            status=status.HTTP_403_FORBIDDEN
        )

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    role = request.data.get('role', 'admin')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=role
    )

    user.set_password(password)
    user.save()

    return Response(
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
    }

    if user.role == 'substitute' and hasattr(user, 'substitute_profile'):
        substitute = user.substitute_profile
        data['substitute_profile'] = {
            'id': substitute.id,
            'postcode': substitute.postcode,
            'phone': substitute.phone,
            'subjects': substitute.subjects,
            'qualifications': substitute.qualifications,
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_substitute(request):

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    postcode = request.data.get('postcode')
    phone = request.data.get('phone')
    subjects = request.data.get('subjects', [])
    qualifications = request.data.get('qualifications', '')

    if not all([username, password, postcode, phone]):
        return Response(
            {'error': 'Username, password, postcode, and phone are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user, substitute = UserService.create_substitute_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            postcode=postcode,
            phone=phone,
            subjects=subjects,
            qualifications=qualifications
        )

        return Response(
            {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                },
                'substitute': {
                    'id': substitute.id,
                    'postcode': substitute.postcode,
                    'phone': substitute.phone,
                    'subjects': substitute.subjects
                }
            },
            status=status.HTTP_201_CREATED
        )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
