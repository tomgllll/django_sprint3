from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post

POSTS_PER_PAGE = 5


def get_base_post_queryset():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).select_related('author', 'category', 'location')


def index(request):
    template_name = 'blog/index.html'
    posts = get_base_post_queryset()[:POSTS_PER_PAGE]
    context = {'posts': posts}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_base_post_queryset().filter(category=category)
    context = {'category': category, 'posts': posts}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        get_base_post_queryset(),
        id=post_id
    )
    context = {'post': post}
    return render(request, template_name, context)
