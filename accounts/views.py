"""Views for authentication, dashboards, and reader subscriptions."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .constants import Roles
from .forms import CustomUserCreationForm, ReaderSubscriptionForm


class GuidedLoginView(LoginView):
    """Render the custom login template for the newsroom site."""

    template_name = "registration/login.html"
    redirect_authenticated_user = True


class GuidedLogoutView(LogoutView):
    """Log users out and return them to the homepage."""

    next_page = reverse_lazy("core:home")


class RoleRequiredMixin(UserPassesTestMixin):
    """Restrict a view to authenticated users with one of the allowed roles."""

    required_roles = ()

    def test_func(self):
        """Return ``True`` when the current user has an allowed newsroom role."""
        return (
            self.request.user.is_authenticated
            and self.request.user.role in self.required_roles
        )

    def handle_no_permission(self):
        """Redirect signed-in users back to the dashboard with a helpful message."""
        if self.request.user.is_authenticated:
            messages.error(self.request, "You do not have access to that page.")
            return redirect("accounts:dashboard")
        return super().handle_no_permission()


class SignUpView(CreateView):
    """Register a new user account for the News App."""

    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        """Show a success message after the account has been created."""
        response = super().form_valid(form)
        messages.success(self.request, "Account created. You can sign in now.")
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    """Display role-specific account summaries for the signed-in user."""

    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        """Add role-based counts that drive the dashboard summary cards."""
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
    """Limit a view to users who have the reader role."""

    required_roles = (Roles.READER,)


class ReaderSubscriptionUpdateView(
    LoginRequiredMixin,
    ReaderRequiredMixin,
    UpdateView,
):
    """Update the publishers and journalists followed by a reader."""

    form_class = ReaderSubscriptionForm
    template_name = "accounts/subscriptions.html"
    success_url = reverse_lazy("accounts:dashboard")

    def get_object(self, queryset=None):
        """Edit the currently authenticated reader instead of a URL-selected user."""
        return self.request.user

    def form_valid(self, form):
        """Persist subscription changes and show a confirmation message."""
        messages.success(self.request, "Your subscriptions were updated.")
        return super().form_valid(form)
