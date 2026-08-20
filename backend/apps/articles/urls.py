from django.urls import path

from . import views


urlpatterns = [
    path("", views.list_articles),
    path("<int:pk>/", views.article_detail),
    path("<int:pk>/export-word/", views.export_article_word),
    path("directions/", views.generate_directions),
    path("manual-hotspots/", views.generate_manual_hotspot_directions),
    path("titles/", views.generate_titles),
    path("draft/", views.generate_draft),
    path("draft/export-word/", views.export_draft_word),
    path("manual-prompt/", views.generate_manual_prompt),
    path("import-draft/", views.import_draft_from_paste),
    path("quality-check/", views.quality_check),
    path("render/", views.render_template),
    path("save/", views.save_article),
]
