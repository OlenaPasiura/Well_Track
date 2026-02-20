from django.contrib.auth import authenticate
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def register (self, email, password, gender=None, age=None, role=None,**extra_fields):
        if not email:
            raise ValueError ("Email обов'язковий")

        user = self.model(
            email=email,
            gender=gender,
            age=age,
            profile_type=role or self.model.Role.USER,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def login_user(self, request, email, password):

        user = authenticate(request, username=email, password=password)

        if user is not None:
            print(f"Вхід успішний для: {email}")
            return user
        else:
            print("Помилка: невірний email або пароль")
            return None


