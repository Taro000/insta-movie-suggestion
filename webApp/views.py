from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from .forms import *
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.db.models import Q
from .image_edit import *
from django.utils import timezone
from django.http import HttpResponse, QueryDict
import requests
from django.conf import settings

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
        context['num_movie'] = Movie.objects.count()
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
        context['keyword'] = self.request.GET.get('keyword')
        context['aws_access_key_id'] = 'AKIARW3444BOGVVUBZHP'
        context['signature'] = 'eIK3c1ps48Kf9w08Snhc1hjwA%2Fo%3D'
        context['expires'] = '1611750685'
        return context

    def form_valid(self, form):
        sent_keyword = form.data['keyword']
        self.success_url = reverse_lazy('searched_movies') + f'?keyword={sent_keyword}'
        return super().form_valid(form)


class StoryMovieView(DetailView):
    model = Movie
    template_name = 'webApp/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movie = Movie.objects.get(id=self.kwargs['pk'])
        context['base64_img'] = make_normal_story(movie.img_path, movie.title, movie.year)
        context['keyword'] = self.request.GET.get('keyword')
        return context

    # def post(self, request, *args, **kwargs):
    #     return self.ajax_response(request.body.decode('utf-8'), self.kwargs['pk'])
    #
    # def ajax_response(self, story_code, movie_id):
    #     movie = Movie.objects.get(id=movie_id)
    #     base64_img = ''
    #     if story_code == 'normal':
    #         base64_img = make_normal_story(movie.img_path, movie.title, movie.year)
    #     elif story_code == 'cover':
    #         base64_img = make_cover_story(movie.img_path, movie.title, movie.year)
    #     elif story_code == 'black':
    #         base64_img = make_black_story(movie.img_path, movie.title, movie.year)
    #     elif story_code == 'white':
    #         base64_img = make_white_story(movie.img_path, movie.title, movie.year)
    #     # return render(self.request, 'webApp/movie_detail.html', {'base64_img': base64_img})
    #     print(base64_img)
    #     return HttpResponse(base64_img, content_type='image/PNG')


class StoryMovieCoverView(DetailView):
    model = Movie
    template_name = 'webApp/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movie = Movie.objects.get(id=self.kwargs['pk'])
        context['base64_img'] = make_cover_story(movie.img_path, movie.title, movie.year)
        context['keyword'] = self.request.GET.get('keyword')
        return context


class StoryMovieBlackView(DetailView):
    model = Movie
    template_name = 'webApp/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movie = Movie.objects.get(id=self.kwargs['pk'])
        context['base64_img'] = make_black_story(movie.img_path, movie.title, movie.year)
        context['keyword'] = self.request.GET.get('keyword')
        return context


class StoryMovieWhiteView(DetailView):
    model = Movie
    template_name = 'webApp/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movie = Movie.objects.get(id=self.kwargs['pk'])
        context['base64_img'] = make_white_story(movie.img_path, movie.title, movie.year)
        context['keyword'] = self.request.GET.get('keyword')
        return context


# notices.html
class NoticeListView(ListView):
    template_name = 'webApp/notices.html'
    paginate_by = 30
    model = Notice


class NoticeDetailView(DetailView):
    model = Notice


URL = "https://movies-tvshows-data-imdb.p.rapidapi.com/"
HEADERS = {
    'x-rapidapi-host': "movies-tvshows-data-imdb.p.rapidapi.com",
    'x-rapidapi-key': "a2e6923e42mshe46d641ef91af7cp1282bdjsn5a245a9c582c"
    }


# for Movie Model
class MovieView(CreateView):
    model = Movie
    form_class = MovieForm

    def post(self, request, *args, **kwargs):
        request.POST.get['created_at'] = timezone.datetime.now()
        request.POST.get['updated_at'] = timezone.datetime.now()

        querystring = {"imdb": f"{request.POST['imdb_id']}", "type": "get-movies-images-by-imdb"}
        response = requests.request("GET", URL, headers=HEADERS, params=querystring)
        request.data['img_path'] = response.content
        request.data['img_path'].name = os.path.join(os.path.join(settings.MEDIA_ROOT, 'image'), f'{uuid.uuid4()}.png')
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()


class ContactUsView(FormView):
    template_name = 'webApp/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
