
import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Blog, Blogger, Comment


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_blogs = Blog.objects.all().count()  # Общее количество блогов
    num_bloggers = Blogger.objects.count()  # Количество блогеров
    
    # Количество комментариев
    num_comments = sum(blog.comment_set.count() for blog in Blog.objects.all())
    
    # Количество блогов с определенным словом в названии (например, "интерес")
    search_word = "интерес" 
    num_blogs_with_word = Blog.objects.filter(title__icontains=search_word).count()

    # Подсчет количества просмотров на странице
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри переменной контекста
    return render(
        request,
        'index.html',
        context={
            'num_blogs': num_blogs,  # Общее количество блогов
            'num_bloggers': num_bloggers,  # Количество блогеров
            'num_comments': num_comments,  # Количество комментариев
            'num_blogs_with_word': num_blogs_with_word,  # Количество блогов с определенным словом
            'num_visits': num_visits,  # Количество посещений
        },
    )


class BlogListView(ListView):
    model = Blog
    paginate_by = 5


class BlogDetailView(DetailView):
    model = Blog


class BloggerListView(ListView):
    model = Blogger


class BloggerDetailView(DetailView):
    model = Blogger


class CommentAdd(CreateView):
    model = Comment
    fields = ['comment']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        form.instance.post_date = datetime.datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse_lazy('blog_detail', kwargs={
                                   'pk': self.kwargs['pk']})
        return success_url
