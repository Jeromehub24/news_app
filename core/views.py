from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from accounts.constants import Roles

from .forms import ArticleForm, NewsletterForm
from .models import Article, Newsletter, Publisher
from .services import approve_article


class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = ()

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.role in self.required_roles

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "You do not have access to that page.")
            return redirect("accounts:dashboard")
        return super().handle_no_permission()


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_articles"] = (
            Article.objects.filter(approved=True)
            .select_related("author", "publisher")
            .order_by("-published_at", "-created_at")[:5]
        )
        context["publishers"] = Publisher.objects.order_by("name")[:5]
        return context


class ArticleListView(ListView):
    model = Article
    template_name = "core/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return (
            Article.objects.filter(approved=True)
            .select_related("author", "publisher")
            .order_by("-published_at", "-created_at")
        )


class ArticleDetailView(DetailView):
    model = Article
    template_name = "core/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        queryset = Article.objects.select_related("author", "publisher")
        user = self.request.user
        if user.is_authenticated and user.role == Roles.EDITOR:
            return queryset
        if user.is_authenticated and user.role == Roles.JOURNALIST:
            return queryset.filter(Q(approved=True) | Q(author=user))
        return queryset.filter(approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_edit"] = user.is_authenticated and self.object.author_id == user.id
        context["can_approve"] = (
            user.is_authenticated
            and user.role == Roles.EDITOR
            and not self.object.approved
        )
        return context


class JournalistRequiredMixin(RoleRequiredMixin):
    required_roles = (Roles.JOURNALIST,)


class EditorRequiredMixin(RoleRequiredMixin):
    required_roles = (Roles.EDITOR,)


class ArticleCreateView(LoginRequiredMixin, JournalistRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "core/article_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Article saved and sent to the review queue.")
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, JournalistRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "core/article_form.html"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).select_related("publisher")

    def form_valid(self, form):
        messages.success(self.request, "Article updated.")
        return super().form_valid(form)


class NewsletterListView(ListView):
    model = Newsletter
    template_name = "core/newsletter_list.html"
    context_object_name = "newsletters"

    def get_queryset(self):
        return Newsletter.objects.select_related("author", "publisher").order_by("-created_at")


class NewsletterCreateView(LoginRequiredMixin, JournalistRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = "core/newsletter_form.html"
    success_url = reverse_lazy("core:newsletter-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Newsletter draft saved.")
        return super().form_valid(form)


class ReviewQueueView(LoginRequiredMixin, EditorRequiredMixin, ListView):
    model = Article
    template_name = "core/article_review_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return (
            Article.objects.filter(approved=False)
            .select_related("author", "publisher")
            .order_by("-created_at")
        )


class ApproveArticleView(LoginRequiredMixin, EditorRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk, approved=False)
        approve_article(article, editor=request.user)
        messages.success(request, f'"{article.title}" was approved.')
        return redirect("core:review-queue")


class PublisherListView(ListView):
    model = Publisher
    template_name = "core/publisher_list.html"
    context_object_name = "publishers"

    def get_queryset(self):
        return Publisher.objects.order_by("name")
