from django.shortcuts import render
from django.http import HttpResponse

# def home_view(request):
#     board = [
#         [{"class": "light" if (i+j)%2==0 else "dark"} for i in range(8)]
#         for j in range(8)
#     ]
#     return render(request, 'chessgame/home.html', {"board": board})


def home_view(request):
    context = {
        "range_64": range(64)  # This creates a list [0, 1, 2, ..., 63]
    }
    return render(request, 'chessgame/home.html', context)


# Create your views here.
