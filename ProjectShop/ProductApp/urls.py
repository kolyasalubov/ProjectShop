from django.urls import path

from ProductApp.views import HomePageView, CategoriesView, SearchResultsListView


urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('', HomePageView.as_view(), name='home'),
]
