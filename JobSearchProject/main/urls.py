from django.urls import path
from .views import (EntryCreateView,
				 EntryUpdateView, 
				 EntryDeleteView, 
				 UserEntryListView,
				 LandingView)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', LandingView.as_view(), name="main-home"),
    path('user/<str:username>', login_required(UserEntryListView.as_view()), name="user-entries"),
    path('entry/new/', EntryCreateView.as_view(), name="entry-create"),
    path('entry/<int:pk>/update/', EntryUpdateView.as_view(), name="entry-update"),
    path('entry/<int:pk>/delete/', EntryDeleteView.as_view(), name="entry-delete"),


]
