from ..models import User, Substitute
from .postcode_service import PostcodeService


class UserService:

    @staticmethod
    def create_substitute_user(username, email, password, first_name, last_name,
                               postcode, phone, subjects, qualifications):

        if User.objects.filter(username=username).exists():
            raise ValueError("Username already exists")

        try:
            postcode_data = PostcodeService.lookup(postcode)
        except ValueError as e:
            raise ValueError(f"Invalid postcode: {str(e)}")

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=User.SUBSTITUTE
        )
        user.set_password(password)
        user.save()

        substitute = Substitute.objects.create(
            user=user,
            postcode=postcode_data['postcode'],
            latitude=postcode_data['latitude'],
            longitude=postcode_data['longitude'],
            phone=phone,
            subjects=subjects,
            qualifications=qualifications
        )

        return user, substitute
