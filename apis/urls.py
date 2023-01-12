from django.urls import path, include

from .views_author import AuthorView
from .views_book import BookView
from .views_configuration import ConfigurationView
from .views_member import MemberView
from .views_transaction import TransactionView
# from .views import BookView, MemberView, AuthorView, TransactionView, ConfigurationView

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'authors', AuthorView)
router.register(r'books', BookView)
router.register(r'members', MemberView)
router.register(r'transactions', TransactionView)
router.register(r'configurations', ConfigurationView)

urlpatterns = router.urls