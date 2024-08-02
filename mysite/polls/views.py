from django.http import HttpResponse

# First view
def index(request):
    return HttpResponse("Hello, world")
