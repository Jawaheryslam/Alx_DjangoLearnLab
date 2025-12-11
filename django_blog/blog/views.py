from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import SignUpForm, UserForm, ProfileForm, Postorm


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
