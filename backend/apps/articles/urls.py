from django.urls import path

from . import views


urlpatterns = [
    path("", views.list_articles),
    path("<int:pk>/", views.article_detail),
    path("directions/", views.generate_directions),
    path("titles/", views.generate_titles),
    path("draft/", views.generate_draft),
    path("render/", views.render_template),
    path("save/", views.save_article),
]
