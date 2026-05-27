import os

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from config.celery import app

from apps.users.roles_and_account_type import Role

UserModel = get_user_model()


class EmailService:
    @staticmethod
    def _get_admins_and_managers():
        return UserModel.objects.filter(role__in=[Role.ADMIN, Role.MANAGER], is_active=True).values_list('email', flat=True)

    @staticmethod
    @app.task
    def __send_email(to: list[str], template_name: str, context: dict, subject: str):
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(
            to=to,
            from_email=os.environ.get('EMAIL_HOST_USER'),
            subject=subject
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def send_car_request(cls, user, data):

        cls.__send_email.delay(
            to=list(cls._get_admins_and_managers()),
            template_name='request_car.html',
            context={'user': user.email, 'brand': data['brand'], 'models': data['models']},
            subject='New Car Request'
        )

    @classmethod
    def send_profanity_error_emai(cls, listing):
            cls.__send_email.delay(
                to=list(cls._get_admins_and_managers()),
                template_name='profanity_list.html',
                context={'id': listing.id,   'title': listing.title, 'description': listing.description},
                subject='Profanity detected'
            )

            




