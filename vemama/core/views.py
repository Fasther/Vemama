from django.views.generic import TemplateView
from tasks.models import Task
from django.utils import timezone


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['tasks_num'] = Task.objects.filter(user=self.request.user, completed=False).count()
            context['tasks_num_over'] = Task.objects.filter(user=self.request.user, completed=False,
                                                            due_date__lte=timezone.now()).count()
            return context
        else:
            return super().get_context_data(**kwargs)
