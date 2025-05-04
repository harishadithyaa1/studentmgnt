from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Create a basic view for the homepage
def homepage(request):
    return render(request, 'base/home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', include('base.urls')),
    path('', homepage, name='home'),  # Root URL points to homepage view
]
