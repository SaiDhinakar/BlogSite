# home/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
# Import for AJAX rendering
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth import get_user_model

def home(request):
    # Get latest published posts
    posts = Post.objects.filter(is_published=True)
    
    # Get featured categories
    categories = Category.objects.all()[:5]
    
    # Get popular posts from the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    popular_posts = Post.objects.filter(
        is_published=True,
        created_at__gte=thirty_days_ago
    ).order_by('-views', '-created_at')[:3]
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'popular_posts': popular_posts,
    }
    
    return render(request, 'home/index.html', context)

def load_more_posts(request):
    page = request.GET.get('page', 1)
    posts = Post.objects.filter(is_published=True)
    paginator = Paginator(posts, 6)
    
    try:
        posts_page = paginator.page(page)
    except:
        return JsonResponse({'data': '', 'end_pagination': True})
    
    posts_html = ''
    for post in posts_page:
        posts_html += render_to_string('home/includes/post_card.html', {'post': post})
    
    data = {
        'data': posts_html,
        'end_pagination': not posts_page.has_next(),
    }
    
    return JsonResponse(data)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    post.increment_views()
    
    # Related posts
    related_posts = Post.objects.filter(
        categories__in=post.categories.all()
    ).exclude(id=post.id).distinct()[:3]
    
    # Comments
    comments = post.comments.filter(is_approved=True)
    
    # Comment form
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(request, 'home/post_detail.html', context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category, is_published=True)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'home/category_posts.html', context)

def search_posts(request):
    query = request.GET.get('q', '')
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |  
            Q(author__username__icontains=query),
            is_published=True
        ).distinct()
    else:
        posts = Post.objects.none()
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'total_results': posts.count(),
    }
    
    return render(request, 'home/search_results.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Generate slug from title
            post.slug = slugify(post.title)
            post.save()
            form.save_m2m()  # Save categories
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()
    
    return render(request, 'home/post_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'home/post_form.html', {'form': form, 'action': 'Edit'})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
    return render(request, 'home/post_confirm_delete.html', {'post': post})

@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'comment': {
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime("%b %d, %Y, %H:%M"),
                    'id': comment.id
                }
            })
        messages.success(request, 'Comment added successfully.')
    else:
        messages.error(request, 'Error adding comment. Please try again.')
    
    return redirect('post_detail', slug=post.slug)

@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'home/user_posts.html', {'posts': posts})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'home/category_list.html', {'categories': categories})

def author_posts(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    posts = Post.objects.filter(author=author, is_published=True)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    
    return render(request, 'home/author_posts.html', context)