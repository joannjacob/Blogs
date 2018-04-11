from django.conf.urls import url,include
from rest_framework import routers
from blog.views import UserViewSet, BlogViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'blogs', BlogViewSet)


urlpatterns = router.urls
