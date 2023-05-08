from django.urls import path

from articles import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path('write/', views.ArticleWriteView.as_view(), name='article_write_view'),
    path('articles/<int:article_id>/', views.ArticleDetailView.as_view(), name='article_detail_view'),
    path('articles/<int:article_id>/like/', views.LikeView.as_view(), name='like_view'),
    path('comments/', views.CommentView.as_view(), name='comment_view'),
    path('comments/<int:comment_id>/', views.CommentView.as_view(), name='comment_view'),
]