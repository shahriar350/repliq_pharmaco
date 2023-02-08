from django.contrib.auth import get_user_model
from django.db import models

from core.utils import PreModel

User = get_user_model()


# Create your models here.
class UserOTP(PreModel):
    user = models.ForeignKey(User, related_name='get_user_otps', on_delete=models.CASCADE)
    otp = models.IntegerField()
    validate_time = models.DateTimeField()
