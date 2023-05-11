from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from articles import views

# url패턴 변경
urlpatterns = [
    path("", views.HomeView.as_view(), name="home_view"),
    path("write/", views.ArticleWriteView.as_view(), name="article_write_view"),
    path(
        "<int:article_id>/",
        views.ArticleDetailView.as_view(),
        name="article_detail_view",
    ),
    path("<int:article_id>/like/", views.LikeView.as_view(), name="like_view"),
    path(
        "<int:article_id>/comments/", views.CommentView.as_view(), name="comment_view"
    ),
    path(
        "<int:article_id>/comments/<int:comment_id>/",
        views.CommentDetailView.as_view(),
        name="comment_view",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
