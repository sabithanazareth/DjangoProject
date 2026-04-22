from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Loginify.models import UserDetails
from.serializers import UserSerializer
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def login(request):
  return HttpResponse("Hello, world!")

@csrf_exempt
def get_all_users(request):
  if request.method == 'GET':
    users = UserDetails.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)
  if request.method == 'POST':
    try:
      input_data = json.loads(request.body)
      print("INPUT",input_data)
      serializer = UserSerializer(data = input_data)
      if serializer.is_valid():
        serializer.save()
        return JsonResponse({
          "message": "Data created successfully",
          "data": serializer.data
        }, status= 201)
      else:
        print(serializer.errors)  # ← add this to see WHY it's invalid
        return JsonResponse({
            "error": serializer.errors
        }, status=400)
    except Exception as e:
      return JsonResponse({
        "error": str(e)
      }, status=400)
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
