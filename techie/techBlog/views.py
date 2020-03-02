from django.views import generic
from .models import Post, Profile, Category
from .forms import CommentForm, ContactForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.http import HttpResponse


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    #context['categories'] = Category.objects.all()
    template_name = "techBlog/index.html"
    paginate_by = 4
    


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'



def post_detail(request, slug):
    template_name = "techBlog/post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
            "post_list" : Post.objects.all()[:5],
        },
    )

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"Message from {form.cleaned_data['name']}"
            message = form.cleaned_data['message']
            sender =form.cleaned_data['email']
            recipients = ['startstartapp@gmail.com']

            try:
               send_mail(subject, message, sender, recipients, fail_silently=True)
            except BadHeaderError:
               messages.warning(' Invalid Header Found')

            messages.success(request,' Message sent')
            return redirect('contact')
                    

    return render(request, 'techBlog/contact.html', {'form':form})