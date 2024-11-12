from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage




def register(request):
    
    if request.method=='POST':
        
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        Confirm_password=request.POST.get("Confirm_password")
        contact_no=request.POST.get("contact_no")
        Profile_Pic=request.FILES.get("Profile_Pic")
        age = request.POST.get('age')
        gender = request.POST.get('gender')
    
        
        if password==Confirm_password:
            
            
            user=CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                profile_pic=Profile_Pic,
                contact_no=contact_no,
                age=age,
                gender=gender,
            )
            messages.success(request, "User Created Success, Please login for entring to your profile")
            return redirect("loginPage")
            
    return render(request,"common/register.html")


def loginPage(request):
    if request.method == 'POST':
        
        user_name=request.POST.get("username")
        pass_word=request.POST.get("password")

        try:
            user = authenticate(request, username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                messages.success(request, "Profile Login Success")
                return redirect('profile') 
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect('loginPage')

        except CustomUser.DoesNotExist:
            messages.error(request, "Not a User created on that Username")
            return redirect('register')

    return render(request, 'common/login.html')



def home(req):
    post = Post.objects.filter(is_trashed=False)
# Get the page number from the request, default to 1 if not provided or invalid
    page_number = req.GET.get('page', 1)
    
    try:
        # Ensure the page number is a valid integer
        page_number = int(page_number)
    except ValueError:
        # If page number is not a valid integer, set it to 1
        page_number = 1

    # Ensure the page number is at least 1
    page_number = max(page_number, 1)

    # Set up pagination, you can change the number of posts per page as needed
    paginator = Paginator(post, 2)  # Show 2 posts per page

    try:
        # Get the posts for the current page
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        # If the page number is out of range, return the last page
        page_obj = paginator.get_page(paginator.num_pages)
    categories = Category.objects.annotate(post_count=Count('post'))
    return render(req, "common/index.html", {'post':post, 'categories':categories, 'page_obj':page_obj})

def contact(req):
    return render(req, "common/contact.html")

@login_required
def profilePage(request):
    
    return render(request,"common/profile.html")

@login_required
def editProfile(request):

    if request.method=='POST':
        
        current_user = request.user
        
        current_user.first_name=request.POST.get("first_name")
        current_user.last_name=request.POST.get("last_name")
        current_user.username=request.POST.get("username")
        current_user.email=request.POST.get("email")
        current_user.contact_no=request.POST.get("contact_no")
        current_user.age=request.POST.get("age")

        new_image = request.FILES.get("new_profile_pic")
        old_image = request.POST.get('old_profile_pic')
        if new_image:
            current_user.profile_pic = new_image
        else:
            current_user.profile_pic = old_image
        current_user.save()
        return redirect("profile")
    
    return render(request,"common/editProfile.html")

@login_required
def logoutPage(request):
    
    logout(request)
    messages.success(request, "Profile Logout Success")
    return redirect('loginPage')

#  change_password functionality in changePassword method
@login_required
def changePassword(req):
    current_user = req.user
    if req.method == "POST":
        old_password = req.POST.get('old_password')
        new_password = req.POST.get('new_password')
        confirm_password = req.POST.get('confirm_password')

        if check_password(old_password, current_user.password):
            if new_password != confirm_password:
                messages.error(req, "New Password And Confirm Password Doesn't Match.")
                return render(req,  "common/change_password.html")
            elif old_password == new_password or old_password == confirm_password:
                messages.error(req, "Old Password And New Password Can't Be Same.")
                return render(req,  "common/change_password.html")
            else:
                current_user.set_password(confirm_password)
                current_user.save()
                messages.success(req, "Password Reset Success")
                return redirect('profile')

    return render(req,  "common/change_password.html")


# Add Post View
@login_required
def add_post(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        keywords = request.POST.get('keywords')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        post_image = request.FILES.get('post_image')

        category = Category.objects.get(id=category_id) if category_id else None

        post = Post.objects.create(
            title=title,
            keywords=keywords,
            content=content,
            category=category,
            post_image=post_image,
            author=request.user
        )
        messages.success(request, "Post added successfully!")
        return redirect('manage_post')

    return render(request, 'common/add_post.html', {'categories': categories})


# Manage Post View
@login_required
def manage_post(request):
    posts = Post.objects.filter(author=request.user, is_trashed=False)
    return render(request, 'common/manage_post.html', {'posts': posts})


# Edit Post View
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    categories = Category.objects.all()

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.keywords = request.POST.get('keywords')
        post.content = request.POST.get('content')
        category_id = request.POST.get('category')
        post.category = Category.objects.get(id=category_id) if category_id else None

        if request.FILES.get('post_image'):
            post.post_image = request.FILES.get('post_image')
        post.save()
        
        messages.success(request, "Post updated successfully!")
        return redirect('manage_post')

    return render(request, 'common/edit_post.html', {'post': post, 'categories': categories})


# Trash Post View
@login_required
def trash_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_trashed = True
    post.save()
    messages.success(request, "Post moved to trash!")
    return redirect('view_trashed_posts')

# View to show all trashed posts
@login_required
def view_trashed_posts(request):
    trashed_posts = Post.objects.filter(author=request.user, is_trashed=True)
    return render(request, 'common/trash_post.html', {'trashed_posts': trashed_posts})

# View to restore a trashed post
@login_required
def restore_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_trashed = False
    post.save()
    messages.success(request, 'Post restored successfully.')
    return redirect('manage_post')

# View to permanently delete a post
@login_required
def delete_post_permanently(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted permanently.')
    return redirect('view_trashed_posts')


# search_content
def search_content(req):
    query = req.GET.get('search')
    if query: 
        post = Post.objects.filter(Q(title__icontains = query)|Q(content__icontains = query)|Q(keywords__icontains = query)|Q(content__icontains=query)|Q(category__name__icontains = query))
        
    else:
        post = Post.objects.none()
        
    context = {
        'post':post,
        'query':query
    } 
    
    return render(req, 'common/search_content.html', context)    

def blog(req):
    post = Post.objects.filter(is_trashed=False)
    categories = Category.objects.annotate(post_count=Count('post'))
    return render(req, 'common/blog.html', {"post":post, "categories":categories})

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get("content")
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        parent_comment_id = request.POST.get("parent_id")
        parent_comment = None
        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, id=parent_comment_id)

        comment = Comment.objects.create(
            post=post,
            user=user,
            content=content,
            parent=parent_comment,
        )
        return JsonResponse({
            'content': comment.content,
            'username': comment.user.username,
            'created_at': comment.created_at.strftime('%b %d, %Y %I:%M %p')
        })
    
    # return redirect("single_post" , post_id=post_id)
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Ensure the user deleting the comment is the owner of the comment
    if comment.user == request.user:
        comment.delete()
        messages.success(request, "Your comment has been deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this comment.")
    
    return redirect("single_post" , post_id=comment.post.id)  # Redirect to the post page or comment section
@login_required
def delete_reply(request, comment_id):
    # Get the comment object (which is acting as a reply)
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the logged-in user is the owner of the comment (reply)
    if comment.user == request.user:
        comment.delete()  # Delete the comment (reply)
    else:
        # Optionally: If the user is not the owner, redirect to error or handle the case
        return redirect('error_page')  # Replace with your error page or another action

    # Redirect to the previous page or the post's comment section
    return redirect(request.META.get('HTTP_REFERER', 'redirect_to_some_page'))


# Single Post View
def single_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_trashed=False)
    categories = Category.objects.annotate(post_count=Count('post'))
    comments = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_at')  # Parent comments only
    return render(request, 'common/single_post.html', {'post': post, 'categories':categories, 'comments':comments})
