from authentication.models import UserToken, AppUser
import re
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_token
from django.core.mail import EmailMessage
import secrets, string

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

async def send_verification_email(user, token):
    username = user.username
    email = user.email
    subject = "Revelio - Verify Email"
    message = render_to_string('verify_email_msg.html', {
        'username': username,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':token,
    })
    email = EmailMessage(
        subject, message, to=[email]
    )
    email.content_subtype = 'html'
    email.send()

async def send_recover_account_email(user, token):
    email = user.email
    subject = "Revelio - Password Recovery Email"
    message = render_to_string('change_password_email_msg.html', {
        'token':token,
    })
    email = EmailMessage(
        subject, message, to=[email]
    )
    email.content_subtype = 'html'
    email.send()


def validate_input(username, email, password):
    if username is None or password is None or email is None:
            return'One or more fields are missing!'
    if AppUser.objects.filter(username = username, is_verified_user=True).exists() or AppUser.objects.filter(email = email, is_verified_user=True).exists():
            return 'Username and/or email already taken by verified user!'
    if username.strip() == '' or password.strip() == '' or email.strip() == '':
        return 'Empty input! Make sure all the fields are filled.'
    if re.match(EMAIL_REGEX, email) is None:
        return 'Email format is wrong.'
    return 'valid'

def create_shortened_token(user):
    UserToken.objects.filter(user=user).delete()
    long_token = account_token.make_token(user)
    short_token = long_token[-8:]
    letters = string.ascii_letters + string.digits
    is_short_exist = UserToken.objects.filter(shortened_token = short_token).exists()
    while is_short_exist:
        short_token = ''.join(secrets.choice(letters) for _ in range(8))
        is_short_exist = UserToken.objects.filter(shortened_token = short_token).exists()
    UserToken.objects.create(user=user, token = long_token, shortened_token = short_token)
    return short_token