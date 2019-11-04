from django.core.mail import send_mail
from django.template import loader


def send_notification(heading, tasks):
    email = tasks[0].user.email
    html_message = loader.render_to_string(
        'tasks/notif_email_template.html',
        {"heading": heading, 'tasks': tasks}
    )
    send_mail(heading, "", "'Vemama' <vemama@pancho.cz>", [email, ], fail_silently=False,
              html_message=html_message)
    return "Done"
