from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AiTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("task_type", models.CharField(max_length=50)),
                ("provider", models.CharField(default="mock", max_length=50)),
                ("prompt", models.TextField(blank=True)),
                ("result_json", models.JSONField(default=dict)),
                ("status", models.CharField(default="created", max_length=30)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("summary", models.TextField(blank=True)),
                ("keywords", models.CharField(blank=True, max_length=500)),
                ("article_type", models.CharField(default="wechat", max_length=50)),
                ("status", models.CharField(default="saved", max_length=30)),
                ("body_json", models.JSONField(default=dict)),
                ("rendered_html", models.TextField(blank=True)),
                ("rendered_text", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-updated_at"]},
        ),
        migrations.CreateModel(
            name="ArticleVersion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("version", models.PositiveIntegerField()),
                ("body_json", models.JSONField(default=dict)),
                ("rendered_html", models.TextField(blank=True)),
                ("rendered_text", models.TextField(blank=True)),
                ("note", models.CharField(blank=True, max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("article", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="versions", to="articles.article")),
            ],
            options={"ordering": ["-version"], "unique_together": {("article", "version")}},
        ),
    ]
