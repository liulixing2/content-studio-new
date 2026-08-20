from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article, ArticleVersion
from .serializers import ArticleSerializer
from .services import mock_article, mock_directions, mock_titles, render_article_template


@api_view(["POST"])
def generate_directions(request):
    keywords = request.data.get("keywords", "")
    return Response({"mode": "mock", "directions": mock_directions(keywords)})


@api_view(["POST"])
def generate_titles(request):
    direction = request.data.get("direction") or {}
    return Response({"mode": "mock", "titles": mock_titles(direction)})


@api_view(["POST"])
def generate_draft(request):
    title = request.data.get("title") or "未命名公众号文章"
    keywords = request.data.get("keywords", "")
    body = mock_article(title, keywords)
    rendered = render_article_template(body)
    # Drafts are intentionally not saved. The user must click save_article.
    return Response({"mode": "mock", "draft": body, "rendered": rendered, "saved": False})


@api_view(["POST"])
def render_template(request):
    body = request.data.get("draft") or {}
    return Response({"rendered": render_article_template(body)})


@api_view(["GET"])
def list_articles(_request):
    queryset = Article.objects.all()[:50]
    return Response({"articles": ArticleSerializer(queryset, many=True).data})


@api_view(["GET"])
def article_detail(_request, pk):
    article = get_object_or_404(Article, pk=pk)
    return Response({"article": ArticleSerializer(article).data})


@api_view(["POST"])
def save_article(request):
    body = request.data.get("draft") or {}
    if not body.get("title"):
        return Response({"ok": False, "error": "缺少文章标题，不能保存。"}, status=400)
    rendered = render_article_template(body)
    with transaction.atomic():
        article = Article.objects.create(
            title=body.get("title", ""),
            summary=body.get("summary", ""),
            keywords=request.data.get("keywords", ""),
            body_json=body,
            rendered_html=rendered["html"],
            rendered_text=rendered["text"],
        )
        ArticleVersion.objects.create(
            article=article,
            version=1,
            body_json=body,
            rendered_html=rendered["html"],
            rendered_text=rendered["text"],
            note="初次保存",
        )
    return Response({"ok": True, "article": ArticleSerializer(article).data})
