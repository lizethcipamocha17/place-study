# Django
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Django rest framework
from rest_framework.exceptions import ParseError


def get_site_domain(request):
    """This function returns the domain"""
    current_site = get_current_site(request).domain
    return f'{current_site}'


def send_email(subject, from_email, to, template, context):
    """This function is used to send email to users"""
    content = render_to_string(template, context)
    msg = EmailMultiAlternatives(subject, content, from_email, [to])
    msg.attach_alternative(content, "text/html")
    return msg.send()


def parse_int(str_value):
    """This function is used to warn the user that he is making an incorrect request."""
    try:
        return int(str_value)
    except Exception:
        raise ParseError(detail='Solicitud con formato incorrecto.')



