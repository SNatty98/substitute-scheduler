from ..models import User, Substitute


class UserService:

    @staticmethod
    def create_substitute_user(username, email, password, first_name, last_name,
                               postcode, phone, subjects, qualifications):

        if User.objects.filter(username=username).exists():
            raise ValueError("Username already exists")

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
            postcode=postcode,
            phone=phone,
            subjects=subjects,
            qualifications=qualifications
        )

        return user, substitute
