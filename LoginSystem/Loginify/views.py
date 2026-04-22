from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from Loginify.models import UserDetails
from.serializers import UserSerializer
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import SignupForm, LoginForm

# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == 'POST':
      form = SignupForm(request.POST)
      if form.is_valid():
        form.save()
        messages.success(request, "Signup successful! Please log in.")
        return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'Loginify/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
          user = UserDetails.objects.get(email=email)
          if user.password == password:
              return render(request, 'Loginify/success.html', {'username': user.username})
          else:
              form.add_error('password', 'Incorrect password.')
        except UserDetails.DoesNotExist:
          form.add_error('email', 'No account found with this email.')
    else:
        form = LoginForm()
    return render(request, 'Loginify/login.html', {'form': form})

@csrf_exempt
def get_all_users(request):
  if request.method == 'GET':
    users = UserDetails.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)
  return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def get_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def update_user(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        print("User", user)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    if request.method == 'PUT':
        try:
            input_data = json.loads(request.body)
            serializer = UserSerializer(user, data=input_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    "message": "User updated successfully",
                    "data": serializer.data
                }, status=200)
            else:
                return JsonResponse({"error": serializer.errors}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def delete_user(request, email):
    try:
        user = UserDetails.objects.get(email=email)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    if request.method == 'DELETE':
        user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=200)

    return JsonResponse({"error": "Method not allowed"}, status=405)
