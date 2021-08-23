from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreateView, PostUpdateView, PostDeleteView, CategoryListView, CategoryDetailView, subscribe_to_category
from .views import upgrade_me

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('search/', PostSearch.as_view()),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('category/', CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category'),
    path('category/subscribe/', subscribe_to_category, name='subscribe_to_category'),
]