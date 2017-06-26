import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F
from .models import Post
from .forms import PostForm


def post_list(request):
    post_list = Post.objects.all()

    '''
    print('----')
    print(request.GET)
    print(request.GET['q'])
    print(request.GET.get('q'))
    print(request.GET.getlist('q'))  # MultiValueDict에서만 지원
    photo_list = request.FILES.getlist('photo')
    '''

    q = request.GET.get('q', '')
    if q:
        post_list = post_list.filter(title__icontains=q)

    return render(request, 'blog/post_list.html', {
        'q': q,
        'post_list': post_list,
    })


def post_detail(request, id):
    Post.objects.filter(id=id).update(hits=F('hits')+1)
    post = get_object_or_404(Post, id=id)
    next_post = Post.objects.filter(id__gt=post.id).order_by('id').first()
    prev_post = Post.objects.filter(id__lt=post.id).order_by('-id').first()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'next_post': next_post,
        'prev_post': prev_post,
    })


def archives(request):
    day_list = []

    start = datetime.datetime(2017, 1, 1)
    for i in range(365):
        delta = datetime.timedelta(days=i)
        day_list.append(start + delta)

    return render(request, 'blog/archives.html', {
        'day_list': day_list,
    })


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            print('VALID !!!')
            print(form.cleaned_data)  # dict
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {
        'form': form,
    })


