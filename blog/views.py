from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms import Create_accountForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponseRedirect

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_user(request, pk):
    author = Post.objects.get(pk=pk).author
    posts = Post.objects.filter(author_id=author.id).order_by('published_date')
    return render(request, 'blog/post_user.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post' : post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form' : form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    current_user = request.user
    if post.author.username != current_user.username:
        return redirect('post_detail', pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    current_user = request.user
    if post.author.id != current_user.id:
        return redirect('post_detail', pk=pk)
    post.delete()
    return redirect('post_list')


def create_account(request):
    if request.method == "POST":
        form = Create_accountForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_user)
            return redirect('post_list')

    else:
        form = Create_accountForm()
        return render(request, 'registration/create_account.html', {'form': form})