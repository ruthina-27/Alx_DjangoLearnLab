from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def index(request):
    """Display the blog homepage with recent posts."""
    posts = Post.objects.all()[:5]  # Get the 5 most recent posts
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, post_id):
    """Display a single blog post."""
    try:
        post = Post.objects.get(id=post_id)
        return render(request, 'blog/post_detail.html', {'post': post})
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)
