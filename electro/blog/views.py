from django.db.models import Q
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Post, Category


class Posts(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostsByCategory(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'], is_published=True)


class BlogSearch(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(
            Q(title__icontains=self.request.GET.get('search')) |
            Q(short_description__icontains=self.request.GET.get('search')),
            is_published=True)

    # нужен чтобы пагинация работала при поиске
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f'search={self.request.GET.get("search")}&'
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
