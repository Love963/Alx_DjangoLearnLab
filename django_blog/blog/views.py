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
from django.db.models import Q
from taggit.models import Tag


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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        # Attach author and post before saving
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the related post after creating a comment
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        # Only allow the author of the comment to update it
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        # Only allow the author of the comment to delete it
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
   

def search_posts(request):

    query = request.GET.get('q')  # Get the search query from the URL (?q=...)
    results = Post.objects.none()  # Default empty queryset

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()
        return render(request, 'blog/search_results.html', {'posts': results, 'query': query})

    
class PostByTagListView(ListView):
    model = Post                         # Model to fetch objects from
    template_name = 'blog/posts_by_tag.html'  # Template to render
    context_object_name = 'posts'        # Variable name for template
    paginate_by = 5                       # Optional: pagination

    def get_queryset(self):
        """
        Returns the list of posts filtered by the tag slug in the URL.
        """
        tag_slug = self.kwargs.get('tag_slug')           # Get slug from URL
        tag = get_object_or_404(Tag, slug=tag_slug)     # Fetch the Tag object or return 404
        return Post.objects.filter(tags__in=[tag])      # Filter posts by tag

    def get_context_data(self, **kwargs):
        """
        Add extra context to the template.
        """
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))  # Pass tag object
        return context


    
        



        
 




    


        
    

