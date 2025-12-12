from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import SignUpForm, UserForm, ProfileForm, PostForm, CommentForm


class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'blog/logged_out.html'

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:profile')
    else:
        form = SignUpForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile
    except Exception:
        profile = None

    if request.method == 'POST':
        uform = UserForm(request.POST, instance=user)
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            return redirect('blog:profile')
    else:
        uform = UserForm(instance=user)
        pform = ProfileForm(instance=profile)

    return render(request, 'blog/profile.html', {
        'uform': uform,
        'pform': pform,
    })

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(published=True)

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    templte_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = ctx.get('comment form') or CommentForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect(f"{reverse_lazy('login')}?next={requst.path}")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            return redirect(self.object.get_absolute_url())
        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form): # where to rediredt on success
        form.instance.author = self.request.user # set the author from logged in user
        return super().form_valid(form)

class AuthoreditPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        ob = self.get_object()
        return obj.author == self.request.user

class PostUpdateView(LoginRequiredMixin, AuthorEditPermissionMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

class PostDeleteView(LoginRequiredMixin, AuthorEditPermissionMixin, Deleteview):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html/'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_objects_or_404(Post, pk=kwargs.get('post_pk') or kwargs.get('pk'))
        return super().form_valid(form)

class CommentUpdateDeletePermissionMixin(UserPassesTextMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class CommentUpdateView(LoginRequiredMixin, CommentUpdateDeletePermissionMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, CommentUpdateDeletePermissionMixin, DeleteView):
    model= Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()
