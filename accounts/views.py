from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .constants import Roles
from .forms import CustomUserCreationForm, ReaderSubscriptionForm


class GuidedLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class GuidedLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = ()

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role in self.required_roles
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "You do not have access to that page.")
            return redirect("accounts:dashboard")
        return super().handle_no_permission()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created. You can sign in now.")
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.role == Roles.READER:
            context["publisher_subscription_count"] = (
                user.subscribed_publishers.count()
            )
            context["journalist_subscription_count"] = (
                user.subscribed_journalists.count()
            )
        elif user.role == Roles.JOURNALIST:
            context["publisher_membership_count"] = (
                user.journalist_publications.count()
            )
        elif user.role == Roles.EDITOR:
            context["publisher_membership_count"] = user.editor_publications.count()
        return context


class ReaderRequiredMixin(RoleRequiredMixin):
    required_roles = (Roles.READER,)


class ReaderSubscriptionUpdateView(
    LoginRequiredMixin,
    ReaderRequiredMixin,
    UpdateView,
):
    form_class = ReaderSubscriptionForm
    template_name = "accounts/subscriptions.html"
    success_url = reverse_lazy("accounts:dashboard")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your subscriptions were updated.")
        return super().form_valid(form)
