from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomRegisterForm(UserCreationForm):
    """Form to Create new User"""

    # Remove that password authentication section
    usable_password = None

    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        # create a user form and display it the signup page
        form = CustomRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})
