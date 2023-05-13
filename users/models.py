from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.core.validators import MinValueValidator


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **kwargs):
        if not user_id:
            raise ValueError("Users must have an ID")

        user = self.model(user_id=user_id, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password):
        user = self.create_user(
            user_id,
            password=password,
            age=100,
        )
        user.is_admin = True
        # 이메일 인증 시 active가 1로 바뀌기 때문에 슈퍼유저는 이 과정을 거치지 않는다.
        user.is_active = 1
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.CharField("아이디", max_length=20, unique=True)
    email = models.EmailField(
        verbose_name="이메일",
        max_length=255,
        # unique=True,
    )
    nickname = models.CharField("닉네임", max_length=10)
    profile_img = models.ImageField("프로필 사진", null=True, blank=True)

    age = models.PositiveIntegerField(
        "나이", validators=[MinValueValidator(20)], default=0
    )
    followings = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="followers", blank=True
    )
    # follow 기능 구현하시는 분이 골라서 선택!
    # followings = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)
    created_at = models.DateTimeField("생성 시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시간", auto_now=True)

    class AlcoholChoices(models.TextChoices):
        SOJU = "SOJU", "소주"
        BEER = "BEER", "맥주"
        WINE = "WINE", "와인"
        LIQUOR = "LIQUOR", "양주"
        TAKJU = "TAKJU", "탁주"
        ETC = "ETC", "기타"
        # ALL = "ALL", "모든 종류" 추가하고 싶어요..
        NO = "NO", "응답하지 않음"

    fav_alcohol = models.CharField(
        "주종", choices=AlcoholChoices.choices, null=True, blank=True, max_length=10
    )
    AMOUNT = (
        ("BABY", "알쓰"),
        
        ("CHOBO", "술찌"),
        ("JUNGSU", "애주가"),
        ("GOSU", "술꾼"),
        ("GOD", "디오니소스"),
    )
    amo_alcohol = models.CharField(
        "주량", choices=AMOUNT, null=True, blank=True, max_length=10
    )

    # null=true 빈값상관없다 #blank=true isvalid에서 null값이더라도 통과!

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "user_id"  # 로그인 뭘로 할건지
    REQUIRED_FIELDS = []  # null true 안 줄 것들

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
