from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    TemplateView, ListView,
    DetailView, CreateView,
    UpdateView, DeleteView,
)
from blog.models import Post, Comment
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy, reverse


#####################################
# Class based views for posts
#####################################

class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post
    # template_name = ".html"

    def get_queryset(self):
        # Field Quries Used
        # __lte is a field query which means "less than or equal to"
        # the - before published date is to order recent first
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    

class PostDetailView(DetailView):
    model = Post


# Decorators only work with function based views
# for classes, we use mixins (equivalent)
# these areessentially classes thar mixed in with the classes we inherit

class PostCreateView(LoginRequiredMixin, CreateView):
    # Below use methods from mixin class
    login_url = 'login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post
    
    # template_name = ".html"
    # def get_success_url(self):
    #     return reverse('post_detail', kwargs={'pk' : self.object.pk})



class PostUpdateView(LoginRequiredMixin, UpdateView):
    
    # Below use methods from mixin class
    login_url = 'login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post
    # template_name = ".html"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # reverse lazt waits for thing to be deleted before directing to new url
    success_url = reverse_lazy('blog:post_list')
    # template_name = "TEMPLATE_NAME"


class DraftListView(LoginRequiredMixin, ListView):
    model = Post

    # Below use methods from mixin class
    login_url = 'login/'
    redirect_field_name = 'blog/post_draft_list.html'

    def get_queryset(self):
        # Field Queries Used
        # __isnull is a field query which means "is the field null"
        # the - before created date is to order recent first
        return Post.objects.filter(published_date__isnull=True).order_by('-date')


#####################################
# Function based views for comments
#####################################


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method=="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/comment_form.html', context={'form':form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect(request, 'post_detail.comment.post.pk')


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk

    comment.delete()

    return redirect('blog:post_detail', pk=post_pk)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()

    return redirect('blog:post_detail', pk=post.pk)