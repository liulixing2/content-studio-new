from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    article_type = models.CharField(max_length=50, default="wechat")
    status = models.CharField(max_length=30, default="saved")
    body_json = models.JSONField(default=dict)
    rendered_html = models.TextField(blank=True)
    rendered_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class ArticleVersion(models.Model):
    article = models.ForeignKey(Article, related_name="versions", on_delete=models.CASCADE)
    version = models.PositiveIntegerField()
    body_json = models.JSONField(default=dict)
    rendered_html = models.TextField(blank=True)
    rendered_text = models.TextField(blank=True)
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-version"]
        unique_together = [("article", "version")]


class AiTask(models.Model):
    task_type = models.CharField(max_length=50)
    provider = models.CharField(max_length=50, default="mock")
    prompt = models.TextField(blank=True)
    result_json = models.JSONField(default=dict)
    status = models.CharField(max_length=30, default="created")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
