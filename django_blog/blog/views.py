from django.shortcuts import render, redirect, get_object_or_404  # For rendering templates and redirecting
from django.contrib import messages   # Django's framework for flash notifications
from django.contrib.auth.decorators import login_required  # Restrict views to-logged in users
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm   # Import our custom forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Mixins for authentication & permission checks
from django.urls import reverse_lazy   # Lazy reverse for module-level URLs
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # Generic CBVs for common CRUD patterns
from .models import Post
from .models import Comment
from .forms import PostForm
from .forms import CommentForm



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # Bind form with POST data
        if form.is_valid():  # Validate form data
            user = form.save()  # Save new User (handles password hashing)
            username = form.cleaned_data.get('username')  # Get username for message
            messages.success(request, f'Account created for {username}. You can log in now.')  # Flash success message
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()  # Instantiate empty form for GET request
    return render(request, 'blog/register.html', {'form': form})  # Render registration page with form

@login_required  # User must be logged in to access this view
def profile(request):
    if request.method == 'POST':
        # Bind forms with POST data and files, linked to current user instances
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():  # Validate both forms
            u_form.save()  # Save updated user info
            p_form.save()  # Save updated profile info (including avatar)
            messages.success(request, 'Your profile was updated successfully.')  # Flash success message
            return redirect('profile')  # Redirect to profile page to prevent resubmission
    else:
        # For GET requests, pre-populate forms with current user data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}  # Context dictionary to pass to template
    return render(request, 'blog/profile.html', context)  # Render profile page with forms
    
class PostListView(ListView):
    model = Post                               # queryset = Post.objects.all by default
    template_name = 'blog/post_list.html'      # Template to render 
    context_object_name = 'posts'   # Context variable in template
    paginate_by = 5                 # Automatic pagination
class PostDetailView(DetailView):
    model = Post     # Auto fetch Post by pk from URL
    template_name = 'blog/post_detail.html'
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'   # Reused for create & update

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   # Save object & redirect
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    def test_func(self):
        return self.get_object().author == self.request.user
@login_required
def add_comment(request, post_id):
    """Handle adding a new comment to a specific post.
       Only logged-in users can comment.
    """
    post = get_object_or_404(Post, pk='post_id')  # Get the post or 404
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Create comment object without saving yet.
            comment.author = request.user      # Assign current user as author
            comment.post = post                # Link comment to the post
            comment.save()                     # save to database
            return redirect(post.get_absolute_url()) # Go back to post detail
        else:
            form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form':form})
def edit_comment(request,comment_id):
    # Allow the author to edit their comment
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return redirect(comment.post.get_absolute_url())  # Prevent editing by others
    
    if request.method == 'POST':
        form = CommentForm(request.post, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(comment.post.get_absolute_url())
        else:
            form = CommentForm(instance=comment)
        return render(request, 'blog/comment_form.html', {'form':form})
@login_required
def delete_comment(request, comment_id):
    # Allow the author to delete their comment
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect(comment.post.get_absolute_url())

        
 




    


        
    

