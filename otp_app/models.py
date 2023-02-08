from dirtyfields import DirtyFieldsMixin
from django.contrib.auth import get_user_model
from django.db import models

from pharmaco_backend.utils import PreModel

User = get_user_model()


# Create your models here.
class UserOTP(DirtyFieldsMixin, PreModel):
    user = models.ForeignKey(User, related_name='get_user_otps', on_delete=models.CASCADE)
    otp = models.IntegerField()
    validate_time = models.DateTimeField()
