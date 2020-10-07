from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone


def offline_stores_report_email(offline_stores):
    if not offline_stores:
        return

    context = {
        "report_time": timezone.localtime().strftime("%c"),
        "offline_stores": offline_stores
    }

    send_mail(
        subject='Stores Offline',
        message="",
        from_email=None,
        html_message=get_template("audit_email.html").render(context),
        recipient_list=['edchapman88@gmail.com']
    )
