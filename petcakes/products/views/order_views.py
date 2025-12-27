from django.http import HttpResponse

def confirm_order(request):
    return HttpResponse("Confirm order works")
