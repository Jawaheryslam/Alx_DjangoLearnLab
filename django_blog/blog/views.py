from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, UserForm, ProfileForm


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
