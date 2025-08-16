from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileForm


def index(request):
    posts = Post.objects.all()[:5]
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        return render(request, 'blog/post_detail.html', {'post': post})
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            login(request, user)
            return redirect('blog:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """View that allows authenticated users to view and edit their profile details.
    This view handles POST requests to update user information."""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('blog:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'registration/profile.html', context)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('blog:index')
    
    def form_valid(self, form):
        messages.success(self.request, 'You have been logged in successfully!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully!')
        return super().dispatch(request, *args, **kwargs)
