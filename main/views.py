from django.shortcuts import get_list_or_404, render,redirect,get_object_or_404
from .models import Post, Comment
from django.utils import timezone

# Create your views here.
def showmainpage(request):
    return render(request, 'main/mainpage.html')

def showintroduction(request):
    return render(request, 'main/introduction.html')

def showshow(request):
    return render(request, 'main/show.html' )

def showpost(request):
    posts = Post.objects.all()
    return render(request, 'main/post.html',{'posts':posts})

def detail(request,id):
    post = get_object_or_404(Post, pk = id)
    all_comments = post.comments.all().order_by('-created_at')
    return render(request, 'main/detail.html',{'post':post , 'comments':all_comments})

def new(request):
    return render(request, 'main/new.html')

def create(request):
    new_post = Post()
    new_post.title = request.POST['title']
    new_post.writer = request.user
    new_post.pub_date = timezone.now()
    new_post.body = request.POST['body']
    new_post.image = request.FILES.get('image')
    new_post.save()
    return redirect('main:detail',new_post.id)

def edit(request,id):
    edit_post = Post.objects.get(id = id)
    return render(request, 'main/edit.html', {'post' : edit_post})

def update(request, id):
    update_post = Post.objects.get(id = id)
    update_post.title = request.POST['title']
    update_post.writer = request.user
    update_post.pub_date = timezone.now()
    update_post.body = request.POST['body']
    update_post.image = request.FILES.get('image')
    update_post.save()
    return redirect('main:detail',update_post.id)

def delete(request, id):
    delete_post = Post.objects.get(id = id)
    delete_post.delete()
    return redirect("main:post")

def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk = post_id)
        current_user = request.user
        comment_content = request.POST.get('content')
        Comment.objects.create(content = comment_content, writer=current_user, post=post)
    return redirect('main:detail', post_id)

def update_comment(request,comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)
    post = Post.objects.get(id = comment.post.id)
    if request.method == "POST":
        post_id = comment.post.id
        comment.content = request.POST.get('content')
        comment.save()
        return redirect('main:detail', post_id)
    return render(request, 'main/edit_comment.html',{"post":post,"comment": comment})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)
    post_id = comment.post.id
    comment.delete()
    return redirect("main:detail", post_id)
