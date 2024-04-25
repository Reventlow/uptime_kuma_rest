from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required, name='dispatch')
class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages_app/about.html')