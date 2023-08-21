from django.shortcuts import render
from django.views import View
from .models import SiteConfig


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, "main/main.html")


class DefaultView(View):
    template_name = "main/main.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LogoView(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        site_config = SiteConfig.objects.first()
        return render(request, self.template_name, {"site_config": site_config})
