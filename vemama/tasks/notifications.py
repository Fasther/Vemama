from django.core.mail import send_mail
from django.template import loader
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


def send_notification(heading, tasks):
    email = tasks[0].user.email
    html_message = loader.render_to_string(
        'tasks/notif_email_template.html',
        {"heading": heading, 'tasks': tasks}
    )
    send_mail(heading, "", "'Vemama' <vemama@pancho.cz>", [email, ], fail_silently=False,
              html_message=html_message)
    return "Done"


def summary_notification(heading, duedatedays):  # sending email with all tasks ending in due date days period
    users = get_user_model().objects.filter(is_active__exact=1)
    send_emails = 0
    for user in users:  # get user, get their tasks and send them
        tasks = user.tasks.filter(completed=False, due_date__lte=timezone.now() + timedelta(days=duedatedays)).order_by(
            "due_date")
        send_notification(heading, tasks)
        send_emails += 1
    return send_emails
