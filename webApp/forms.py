from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
import textwrap
from .models import *


CONTACT_FORM_CATEGORY = (
    ('AM', '作品追加の希望'),
    ('BM', '画像パターン(背景)追加の希望'),
    ('SP', 'バグ・システムの不具合'),
    ('OT', 'その他'),
)


class SearchMovieForm(forms.Form):
    keyword = forms.CharField(label='', max_length=256)


class MovieForm(forms.Form):
    model = Movie
    fields = ('id', 'title', 'title_ja', 'year', 'imdb_id', 'img_path', 'created_at', 'updated_at')


class ContactForm(forms.Form):
    subject = forms.CharField(label='件名', max_length=100)
    category = forms.ChoiceField(label='カテゴリー', choices=CONTACT_FORM_CATEGORY)
    sender = forms.EmailField(label='Email', help_text='※ご確認の上、正しく入力してください。')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def send_email(self):
        subject = self.cleaned_data['subject']
        category = self.cleaned_data['category']
        sender = self.cleaned_data['sender']
        message = self.cleaned_data['message']
        content = textwrap.dedent(
            f'''
            「{subject}」
            {category}
            {message}
            
            ('AM', '作品追加の希望'),
            ('BM', '画像パターン(背景)追加の希望'),
            ('SP', 'バグ・システムの不具合'),
            ('OT', 'その他')
            
            from {sender}
            '''
        )
        to_list = [sender]
        bcc_list = [settings.EMAIL_HOST_USER]
        try:
            message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
            message.send()
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")
