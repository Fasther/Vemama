from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.db.models import Sum
from cars.models import Car, City
from tasks.models import Task
from django.utils import timezone
from core.models import Profile


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['tasks_num'] = Task.objects.filter(user=self.request.user, completed=False).count()
            context['tasks_num_over'] = Task.objects.filter(user=self.request.user, completed=False,
                                                            due_date__lte=timezone.now()).count()
            context["total_tasks"] = Task.objects.all().count()
            context["total_tasks_completed"] = Task.objects.filter(completed=True).count()
            context["total_overdue"] = Task.objects.filter(
                completed=False, due_date__lte=timezone.now()).count()
            context["active_workers"] = Profile.objects.filter(user__is_active=True).count()

            context["inactive_cars"] = Car.objects.filter(is_active=False).count()
            context["active_cars"] = Car.objects.filter(is_active=True).count()
            context["cities"] = City.objects.filter()
            context["total_driven_km"] = f"""{Car.objects.all().aggregate(
                Sum("car_actual_driven_kms")
            ).get("car_actual_driven_kms__sum"):,}""".replace(",", " ")
            return context
        else:
            return super().get_context_data(**kwargs)


class ChangePasswordView(PasswordChangeView):
    template_name = "change-password.html"
    success_url = reverse_lazy("core:change_password")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:  # show message of what work have been done
            context["msg"] = self.request.session.pop("msg")
        except KeyError:
            pass
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session["msg"] = "Password updated successfully!"
        return response
