from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from .models import Post, Tag


class SearchResultsView(ListView):
    """Display search results for posts based on title, content, or tags."""
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct().order_by('-published_date')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_results'] = self.get_queryset().count()
        return context


class PostsByTagView(ListView):
    """Display posts filtered by a specific tag."""
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name=tag_name).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs.get('tag_name')
        context['tag'] = get_object_or_404(Tag, name=tag_name)
        context['total_posts'] = self.get_queryset().count()
        return context


def tag_list(request):
    """Display all available tags with post counts."""
    tags = Tag.objects.all().order_by('name')
    tag_data = []
    for tag in tags:
        tag_data.append({
            'tag': tag,
            'post_count': tag.posts.count()
        })
    return render(request, 'blog/tag_list.html', {'tag_data': tag_data})
