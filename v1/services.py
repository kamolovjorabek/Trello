from django.core.mail import send_mail
import random
from v1.user.models import WorkerCode


def send_message_email(email, user):
    code = random.randrange(1000, 9999)
    WorkerCode.objects.create(user=user, worker_code=code)
    send_mail('Data', f"You {code}", '', [email])


