"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from questionnaire.views import questionnaireView, resultView, homeView, personalView, chartsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baecke/info/', personalView, name='personal'),
    path('baecke/questionnaire/', questionnaireView, name='questionnaire-view'),
    path('baecke/questionnaire/<uuid:uuid>/', questionnaireView, name='questionnaire-view-uuid'),
    path('baecke/result/<uuid:uuid>/', resultView, name='result'),
    
    path('baecke/graficos/', chartsView, name='charts'),
    
    path('', homeView, name="home")
]
