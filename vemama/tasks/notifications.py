from django.core.mail import send_mail
from django.template import loader
from tasks.models import Task
from django.contrib.auth.models import User


def send_notification():  # test will be not used
    heading = "Your tasks"
    tasks = Task.objects.filter(user=User.objects.get(pk=1), completed=False)
    html_message = loader.render_to_string(
        'tasks/notif_email_template.html',
        {"heading": heading, 'tasks': tasks}
    )
    send_mail(heading, "", "'Vemama' <vemama@pancho.cz>", ["pavel@pancocha.eu", ], fail_silently=False,
              html_message=html_message)
    return "Done"
