from django.urls import path
from .views import (EntryListView,
				 EntryCreateView,
				 EntryUpdateView, 
				 EntryDeleteView, 
				 UserEntryListView)
from . import views

urlpatterns = [
    path('', EntryListView.as_view(), name="main-home"),
    path('user/<str:username>', UserEntryListView.as_view(), name="user-entries"),
    path('entry/new/', EntryCreateView.as_view(), name="entry-create"),
    path('entry/<int:pk>/update/', EntryUpdateView.as_view(), name="entry-update"),
    path('entry/<int:pk>/delete/', EntryDeleteView.as_view(), name="entry-delete"),


]
