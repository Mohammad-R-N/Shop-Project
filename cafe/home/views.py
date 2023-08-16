from django.shortcuts import render
from django.views import View
from .models import SiteConfig
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "main/main.html"

    


class DefaultView(TemplateView):
    template_name = "main/main.html"


class LogoView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_config = SiteConfig.objects.first()
        context["site_config"] = site_config
        return context
