from django.shortcuts import render
from django.views import View
from .models import SiteConfig
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "main/main.html"

    


class DefaultView(TemplateView):
    template_name = "main/main.html"


class LogoView(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        site_config = SiteConfig.objects.first()
        return render(request, self.template_name, {"site_config": site_config})
