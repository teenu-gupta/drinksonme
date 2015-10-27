from core.utils import Event
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

 User = get_user_model()
 

class UserEmailVerify(Event):
    code = 'email_verify'
    notify = 'email'
    app_name = 'accounts'

    def run(self, ctx):
        super(UserEmailVerify, self).run(ctx)