from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, SignupForm, TaskForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth.models import User


#RESET PASS1
def send_password_reset_email(request, email):
    # Check if the email exists in the database
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Handle the case where the email does not exist
        messages.error(request, 'User with this email does not exist.')
        return None

    # Generate a password reset token
    token = default_token_generator.make_token(user)

    # Encode the user's ID and token to be included in the URL
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Construct the password reset URL
    reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))

    # Render the email template with the reset URL
    email_subject = 'Password Reset'
    email_body = render_to_string('password_reset_email.html', {'reset_url': reset_url})

    # Send the email
    send_mail(email_subject, email_body, 'enote7y@gmail.com', [email])

#SIGNINUP
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            # Process form submission
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            user.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
        

#LOGIN USER
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)  # Correct usage of login() function
                # Redirect to the page user was trying to access, or home page if no next parameter
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                form.add_error(None, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()

    # If the next parameter exists, pass it to the template to display a message
    next_param = request.GET.get('next')
    return render(request, 'login.html', {'form': form, 'next_param': next_param})


def logout_view(request):
    logout(request)
    return redirect('index')  

def index(request):
    return render(request, 'index.html')  

@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'home.html', {'tasks': tasks})

@login_required
def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_details.html', {'task': task})


#tasks mgt part
@login_required
def create_or_edit_task(request, task_id=None):
    if task_id:
        task = get_object_or_404(Task, pk=task_id)
    else:
        task = Task(user=request.user)  # Assign the current user to the task

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log out the user first
        user.delete()    # Delete the user account
        return redirect('index')  # Redirect to landing page after deletion
    return redirect('profile')  # Redirect to profile page if accessed via GET reques

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log out the user first

        User = get_user_model()
        user.delete()    # Delete the user account

        return redirect('index')  # Redirect to landing page after deletion
    return redirect('profile')  # Redirect to profile page if accessed via GET request

@login_required
def delete_task(request, task_id):
    # Retrieve the task object to be deleted
    task = get_object_or_404(Task, pk=task_id)
    
    # Ensure that the task belongs to the current user (if needed)
    # Add your authentication logic here
    
    # Delete the task object from the database
    task.delete()
    
    # Redirect the user to the appropriate page after deletion
    return redirect('home')  # Redirect to the dashboard page, for example

@login_required
def complete_task(request, task_id):
    # Retrieve the task object
    task = get_object_or_404(Task, pk=task_id)

    # Update the task status to 'Done'
    task.status = 'Done'
    task.save()

    # Redirect to the task details page
    return redirect('task_details', task_id=task.id)