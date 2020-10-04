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
        html_message=get_template("offline_stores_report.html").render(context),
        from_email='no-reply@store-supervisor.website',
        recipient_list=['edchapman88@gmail.com']
    )
