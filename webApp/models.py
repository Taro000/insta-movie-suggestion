from django.db import models
import uuid

# Create your models here.


class Notice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('タイトル', max_length=64)
    content = models.TextField('内容')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SiteConfig(models.Model):
    title = models.CharField('Title', max_length=64)
    keyword = models.CharField('Keyword', max_length=256)
    description = models.TextField('Description')
    Agreements = models.TextField('利用規約')
    PrivacyPolicy = models.TextField('プライバシーポリシー')
    AboutMe = models.TextField('サイト説明')
    updated_at = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField('タイトル', max_length=128)
    title_ja = models.CharField('日本語タイトル', max_length=128)
    year = models.CharField('公開年', max_length=16)
    imdb_id = models.CharField('IMDb ID', max_length=32)
    img_path = models.ImageField('ポスター画像Path', upload_to='poster')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
