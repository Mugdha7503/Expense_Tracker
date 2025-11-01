from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib import messages
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import SignupForm

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)

            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # (Optional) Store token in session for later use
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token

            # ✅ Redirect to dashboard or transactions page
            return redirect("transactions-list")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")




def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("login")
