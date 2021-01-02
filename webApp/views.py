from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from .forms import *
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.db.models import Q

# Create your views here.


# index.html
class IndexView(TemplateView, FormView):
    template_name = 'webApp/index.html'
    form_class = SearchMovieForm
    success_url = reverse_lazy('searched_movies')

    def form_valid(self, form):
        sent_keyword = form.data['keyword']
        self.success_url = reverse_lazy('searched_movies') + f'?keyword={sent_keyword}'
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['notice_list'] = Notice.objects.order_by('-updated_at')[:5]
        return context


# searched_movies.html
class SearchedMovieView(ListView, FormView):
    template_name = 'webApp/searched_movies.html'
    form_class = SearchMovieForm
    paginate_by = 20
    model = Movie

    success_url = reverse_lazy('searched_movies')

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(title__icontains=self.request.GET.get('keyword')) | Q(title_ja__contains=self.request.GET.get('keyword'))
        ).all().order_by('-updated_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['media_url'] = settings.MEDIA_URL
        return context

    def form_valid(self, form):
        sent_keyword = form.data['keyword']
        self.success_url = reverse_lazy('searched_movies') + f'?keyword={sent_keyword}'
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     application_id = '1053227171354478236'
    #     keyword = request.GET.get('keyword')
    #     if request.GET.get('page'):
    #         page = request.GET.get('page')
    #         api_url = f'https://app.rakuten.co.jp/services/api/BooksDVD/Search/20170404?format=json&title={keyword}&booksGenreId=003&applicationId={application_id}&page={page}'
    #     else:
    #         api_url = f'https://app.rakuten.co.jp/services/api/BooksDVD/Search/20170404?format=json&title={keyword}&booksGenreId=003&applicationId={application_id}'
    #     response = requests.get(api_url)
    #     res_json = response.json()
    #     print(keyword)
    #
    #     movies = []
    #     for item in res_json['Items']:
    #         item_body = item['Item']
    #         movie = {
    #             'title': item_body['title'],
    #             'imageUrl': item_body['largeImageUrl'],
    #             'derector': item_body['artistName'].split('/')[-1],
    #             'jancode': item_body['jan'],
    #         }
    #         movies.append(movie)
    #     print(movies)
    #     return render(request, 'webApp/searched_movies.html', {
    #         'movies': movies,
    #         'keyword': keyword,
    #         'count': res_json['count'],
    #         'page': res_json['page'],
    #         'pageCount': res_json['pageCount'],
    #         'form': self.form_class,
    #     })


# notices.html
class NoticeListView(ListView):
    template_name = 'webApp/notices.html'
    paginate_by = 30
    model = Notice


class NoticeDetailView(DetailView):
    model = Notice
