"""Views that power the public site, publishing tools, and review queue."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from accounts.constants import Roles

from .forms import ArticleForm, NewsletterForm, PublisherForm
from .models import Article, Newsletter, Publisher
from .services import approve_article


class RoleRequiredMixin(UserPassesTestMixin):
    """Restrict a view to signed-in users with one of the required roles."""

    required_roles = ()

    def test_func(self):
        """Return ``True`` when the current user satisfies the role check."""
        user = self.request.user
        return user.is_authenticated and user.role in self.required_roles

    def handle_no_permission(self):
        """Redirect signed-in users to the dashboard with an error message."""
        if self.request.user.is_authenticated:
            messages.error(self.request, "You do not have access to that page.")
            return redirect("accounts:dashboard")
        return super().handle_no_permission()


class HomePageView(TemplateView):
    """Show a landing page with recent approved articles and publishers."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        """Add homepage content blocks used by the landing page template."""
        context = super().get_context_data(**kwargs)
        context["latest_articles"] = (
            Article.objects.filter(approved=True)
            .select_related("author", "publisher")
            .order_by("-published_at", "-created_at")[:5]
        )
        context["publishers"] = Publisher.objects.order_by("name")[:5]
        return context


class ArticleListView(ListView):
    """List approved articles for readers and anonymous visitors."""

    model = Article
    template_name = "core/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        """Return the published articles ordered by most recent activity."""
        return (
            Article.objects.filter(approved=True)
            .select_related("author", "publisher")
            .order_by("-published_at", "-created_at")
        )


class ArticleDetailView(DetailView):
    """Display an article while honoring role-based visibility rules."""

    model = Article
    template_name = "core/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        """Allow editors to see all drafts and journalists to see their own."""
        queryset = Article.objects.select_related("author", "publisher")
        user = self.request.user
        if user.is_authenticated and user.role == Roles.EDITOR:
            return queryset
        if user.is_authenticated and user.role == Roles.JOURNALIST:
            return queryset.filter(Q(approved=True) | Q(author=user))
        return queryset.filter(approved=True)

    def get_context_data(self, **kwargs):
        """Expose edit, delete, and approve permissions to the template."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_edit"] = user.is_authenticated and (
            user.role == Roles.EDITOR or self.object.author_id == user.id
        )
        context["can_delete"] = context["can_edit"]
        context["can_approve"] = (
            user.is_authenticated
            and user.role == Roles.EDITOR
            and not self.object.approved
        )
        return context


class JournalistRequiredMixin(RoleRequiredMixin):
    """Limit a view to newsroom users with the journalist role."""

    required_roles = (Roles.JOURNALIST,)


class EditorRequiredMixin(RoleRequiredMixin):
    """Limit a view to newsroom users with the editor role."""

    required_roles = (Roles.EDITOR,)


class EditorOrJournalistRequiredMixin(RoleRequiredMixin):
    """Allow access to either editors or journalists."""

    required_roles = (Roles.EDITOR, Roles.JOURNALIST)


class ArticleCreateView(LoginRequiredMixin, JournalistRequiredMixin, CreateView):
    """Create a new article draft for the authenticated journalist."""

    model = Article
    form_class = ArticleForm
    template_name = "core/article_form.html"

    def get_form_kwargs(self):
        """Pass the current user into the form for publisher scoping."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Attach the current user as author before saving the article."""
        form.instance.author = self.request.user
        messages.success(self.request, "Article saved and sent to the review queue.")
        return super().form_valid(form)


class ArticleEditorAccessMixin(
    LoginRequiredMixin,
    EditorOrJournalistRequiredMixin,
):
    """Allow editors to access all articles and journalists to access their own."""

    def get_queryset(self):
        """Restrict journalists to their own articles while editors see all."""
        queryset = Article.objects.select_related("author", "publisher")
        if self.request.user.role == Roles.EDITOR:
            return queryset
        return queryset.filter(author=self.request.user)


class ArticleUpdateView(ArticleEditorAccessMixin, UpdateView):
    """Edit an existing article."""

    model = Article
    form_class = ArticleForm
    template_name = "core/article_form.html"

    def get_form_kwargs(self):
        """Pass the current user into the form for publisher scoping."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Save article changes and confirm the update to the user."""
        messages.success(self.request, "Article updated.")
        return super().form_valid(form)


class ArticleDeleteView(ArticleEditorAccessMixin, DeleteView):
    """Delete an article after a confirmation step."""

    model = Article
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("core:article-list")

    def get_context_data(self, **kwargs):
        """Describe the article being deleted in the shared confirmation template."""
        context = super().get_context_data(**kwargs)
        context["item_type"] = "article"
        context["item_name"] = self.object.title
        return context

    def form_valid(self, form):
        """Delete the article and show a success message."""
        self.object = self.get_object()
        messages.success(self.request, f'"{self.object.title}" was deleted.')
        return super().form_valid(form)


class NewsletterListView(ListView):
    """List newsletters ordered by most recently updated first."""

    model = Newsletter
    template_name = "core/newsletter_list.html"
    context_object_name = "newsletters"

    def get_queryset(self):
        """Return newsletters with related author and publisher records loaded."""
        return (
            Newsletter.objects.select_related("author", "publisher")
            .order_by("-updated_at", "-created_at")
        )


class NewsletterCreateView(LoginRequiredMixin, JournalistRequiredMixin, CreateView):
    """Create a newsletter draft for the authenticated journalist."""

    model = Newsletter
    form_class = NewsletterForm
    template_name = "core/newsletter_form.html"
    success_url = reverse_lazy("core:newsletter-list")

    def get_form_kwargs(self):
        """Pass the current user into the form for publisher scoping."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Attach the current user as author before saving the newsletter."""
        form.instance.author = self.request.user
        messages.success(self.request, "Newsletter draft saved.")
        return super().form_valid(form)


class NewsletterEditorAccessMixin(
    LoginRequiredMixin,
    EditorOrJournalistRequiredMixin,
):
    """Allow editors to access all newsletters and journalists only their own."""

    def get_queryset(self):
        """Restrict journalists to their own newsletters while editors see all."""
        queryset = Newsletter.objects.select_related("author", "publisher")
        if self.request.user.role == Roles.EDITOR:
            return queryset
        return queryset.filter(author=self.request.user)


class NewsletterUpdateView(NewsletterEditorAccessMixin, UpdateView):
    """Edit an existing newsletter draft."""

    model = Newsletter
    form_class = NewsletterForm
    template_name = "core/newsletter_form.html"
    success_url = reverse_lazy("core:newsletter-list")

    def get_form_kwargs(self):
        """Pass the current user into the form for publisher scoping."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Persist newsletter changes and confirm the update."""
        messages.success(self.request, "Newsletter updated.")
        return super().form_valid(form)


class NewsletterDeleteView(NewsletterEditorAccessMixin, DeleteView):
    """Delete a newsletter after a confirmation step."""

    model = Newsletter
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("core:newsletter-list")

    def get_context_data(self, **kwargs):
        """Describe the newsletter being deleted in the shared confirmation view."""
        context = super().get_context_data(**kwargs)
        context["item_type"] = "newsletter"
        context["item_name"] = self.object.subject
        return context

    def form_valid(self, form):
        """Delete the newsletter and show a success message."""
        self.object = self.get_object()
        messages.success(self.request, f'"{self.object.subject}" was deleted.')
        return super().form_valid(form)


class ReviewQueueView(LoginRequiredMixin, EditorRequiredMixin, ListView):
    """List unapproved articles that still need editorial review."""

    model = Article
    template_name = "core/article_review_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        """Return the pending article queue ordered by newest first."""
        return (
            Article.objects.filter(approved=False)
            .select_related("author", "publisher")
            .order_by("-created_at")
        )


class ApproveArticleView(LoginRequiredMixin, EditorRequiredMixin, View):
    """Approve a pending article and trigger downstream notifications."""

    def post(self, request, pk):
        """Approve the selected article and return the editor to the review queue."""
        article = get_object_or_404(Article, pk=pk, approved=False)
        approve_article(article, editor=request.user)
        messages.success(request, f'"{article.title}" was approved.')
        return redirect("core:review-queue")


class PublisherListView(ListView):
    """List publishers together with membership counts and join state."""

    model = Publisher
    template_name = "core/publisher_list.html"
    context_object_name = "publishers"

    def get_queryset(self):
        """Annotate publishers with editor and journalist totals for display."""
        return (
            Publisher.objects.annotate(
                editor_total=Count("editors", distinct=True),
                journalist_total=Count("journalists", distinct=True),
            )
            .order_by("name")
        )

    def get_context_data(self, **kwargs):
        """Expose membership actions and counts tailored to the current user."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_create_publishers"] = (
            user.is_authenticated and user.role == Roles.EDITOR
        )
        context["can_manage_membership"] = (
            user.is_authenticated and user.role in {Roles.EDITOR, Roles.JOURNALIST}
        )
        if user.is_authenticated and user.role == Roles.EDITOR:
            context["joined_publisher_ids"] = set(
                user.editor_publications.values_list("id", flat=True)
            )
            context["membership_role_label"] = "Editor"
        elif user.is_authenticated and user.role == Roles.JOURNALIST:
            context["joined_publisher_ids"] = set(
                user.journalist_publications.values_list("id", flat=True)
            )
            context["membership_role_label"] = "Journalist"
        else:
            context["joined_publisher_ids"] = set()
            context["membership_role_label"] = ""
        return context


class PublisherCreateView(LoginRequiredMixin, EditorRequiredMixin, CreateView):
    """Create a new publisher and add the creator as its first editor."""

    model = Publisher
    form_class = PublisherForm
    template_name = "core/publisher_form.html"
    success_url = reverse_lazy("core:publisher-list")

    def form_valid(self, form):
        """Save the publisher and grant the creator editor membership."""
        response = super().form_valid(form)
        # The creator becomes the first editor so the new publisher is usable.
        self.object.editors.add(self.request.user)
        messages.success(self.request, "Publisher created.")
        return response


class PublisherMembershipToggleView(
    LoginRequiredMixin,
    EditorOrJournalistRequiredMixin,
    View,
):
    """Join or leave a publisher as either an editor or journalist."""

    def post(self, request, pk):
        """Toggle the current user's membership in the selected publisher."""
        publisher = get_object_or_404(Publisher, pk=pk)
        membership_manager = self.get_membership_manager(publisher)
        action = request.POST.get("action", "join")

        # Editors and journalists join their own side of the publisher team.
        if action == "leave":
            membership_manager.remove(request.user)
            messages.success(request, f"You left {publisher.name}.")
        else:
            membership_manager.add(request.user)
            messages.success(request, f"You joined {publisher.name}.")

        return redirect("core:publisher-list")

    def get_membership_manager(self, publisher):
        """Return the correct many-to-many manager for the user's role."""
        if self.request.user.role == Roles.EDITOR:
            return publisher.editors
        return publisher.journalists
