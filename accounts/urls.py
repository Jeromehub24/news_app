from django.urls import path

from .views import DashboardView, GuidedLoginView, GuidedLogoutView, SignUpView


app_name = "accounts"

urlpatterns = [
    path("login/", GuidedLoginView.as_view(), name="login"),
    path("logout/", GuidedLogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
