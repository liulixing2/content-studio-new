from rest_framework import serializers

from .models import Article, ArticleVersion


class ArticleVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleVersion
        fields = ["id", "version", "note", "created_at"]


class ArticleSerializer(serializers.ModelSerializer):
    versions = ArticleVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "summary",
            "keywords",
            "article_type",
            "status",
            "body_json",
            "rendered_html",
            "rendered_text",
            "created_at",
            "updated_at",
            "versions",
        ]
