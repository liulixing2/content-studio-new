from django.contrib import admin

from .models import AiTask, Article, ArticleVersion


admin.site.register(Article)
admin.site.register(ArticleVersion)
admin.site.register(AiTask)
