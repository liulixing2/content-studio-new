from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article, ArticleVersion
from .serializers import ArticleSerializer
from .services import (
    build_article_docx,
    build_directions_from_manual_hotspots,
    build_manual_prompt,
    check_article_quality,
    import_pasted_article,
    mock_article,
    mock_directions,
    mock_titles,
    render_article_template,
)

MAX_ARTICLE_COUNT = 20


def trim_article_library(max_count=MAX_ARTICLE_COUNT):
    old_ids = list(Article.objects.order_by("-updated_at").values_list("id", flat=True)[max_count:])
    if old_ids:
        Article.objects.filter(id__in=old_ids).delete()
    return len(old_ids)


@api_view(["POST"])
def generate_directions(request):
    keywords = request.data.get("keywords", "")
    return Response({"mode": "mock", "directions": mock_directions(keywords)})


@api_view(["POST"])
def generate_manual_hotspot_directions(request):
    keywords = request.data.get("keywords", "")
    pasted_text = request.data.get("pasted_text", "")
    result = build_directions_from_manual_hotspots(keywords, pasted_text)
    return Response(result)


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
def generate_manual_prompt(request):
    stage = request.data.get("stage") or "draft"
    context = request.data.get("context") or {}
    return Response({"prompt": build_manual_prompt(stage, context)})


@api_view(["POST"])
def import_draft_from_paste(request):
    title = request.data.get("title") or "未命名公众号文章"
    pasted_text = request.data.get("pasted_text") or ""
    keywords = request.data.get("keywords") or ""
    body = import_pasted_article(title, pasted_text, keywords)
    rendered = render_article_template(body)
    return Response({"draft": body, "rendered": rendered, "saved": False})


@api_view(["POST"])
def quality_check(request):
    body = request.data.get("draft") or {}
    return Response({"report": check_article_quality(body), "saved": False})


@api_view(["POST"])
def render_template(request):
    body = request.data.get("draft") or {}
    return Response({"rendered": render_article_template(body)})


def _docx_response(filename, docx_bytes):
    response = HttpResponse(
        docx_bytes,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response["Content-Disposition"] = 'attachment; filename="%s"' % filename
    return response


@api_view(["POST"])
def export_draft_word(request):
    body = request.data.get("draft") or {}
    if not body.get("title"):
        return Response({"ok": False, "error": "缺少文章标题，不能导出 Word。"}, status=400)
    docx_bytes = build_article_docx(body)
    return _docx_response("wechat-draft.docx", docx_bytes)


@api_view(["GET"])
def list_articles(_request):
    queryset = Article.objects.all()[:MAX_ARTICLE_COUNT]
    return Response({"articles": ArticleSerializer(queryset, many=True).data, "limit": MAX_ARTICLE_COUNT})


@api_view(["GET", "DELETE"])
def article_detail(_request, pk):
    article = get_object_or_404(Article, pk=pk)
    if _request.method == "DELETE":
        article.delete()
        return Response({"ok": True, "deleted_id": pk})
    return Response({"article": ArticleSerializer(article).data})


@api_view(["GET"])
def export_article_word(_request, pk):
    article = get_object_or_404(Article, pk=pk)
    docx_bytes = build_article_docx(article.body_json)
    return _docx_response("wechat-article-%s.docx" % article.pk, docx_bytes)


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
        removed_count = trim_article_library()
    return Response({"ok": True, "article": ArticleSerializer(article).data, "limit": MAX_ARTICLE_COUNT, "removed_count": removed_count})
