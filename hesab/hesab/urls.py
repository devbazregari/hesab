
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path("admin/", admin.site.urls),

    #API PATH

    path("api/user/",include('user.userApi.urls'))
]
