from django.shortcuts import render, reverse, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views import View




class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    # queryset = Post.objects.order_by('-post_data')
    ordering = ['-post_data']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        context['category'] = Category.objects.values_list()
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categorys'
    queryset = Category.objects.order_by('news_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)

        return context

def subscribe_to_category(request):
    category = Category.objects.get(pk=request.GET.get('category'))
    category.subscribers.add(request.user)
    category.save()
    return redirect(f'/news/category/{category.pk}')

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-post_data']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'onenews'
    queryset = Post.objects.all()

    subscribe_to_category

class CategoryDetailView(DetailView):
    template_name = 'category.html'
    queryset = Category.objects.all()

def mail_post(heading, text, category):
    cats = Category.objects.filter(news_category=category)
    for cat in cats:
        subscbrs = Category.subscribers.all()
        for subscbr in subscbrs:
            send_mail(
                subject=heading,
                # имя клиента и дата записи будут в теме для удобства
                message=f'Вы подписались в NewsPaper на категорию {cat.news_category}. Создана новая запись \
                            {heading} со следующим содержимым: {text[:100]}. \
                            Вы можете прочесть запись по ссылке: ?',  # сообщение с кратким описанием проблемы
                from_email='sample417@yandex.ru',
                # здесь указываете почту, с которой будете отправлять (об этом попозже)
                recipient_list=[subscbr.user.email, ]
                # здесь список получателей. Например, секретарь, сам врач и т. д.
            )

class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    mail_post(form_class.Meta.model.heading,
              form_class.Meta.model.content,
              form_class.Meta.model.category)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'category.html', {})


class CategoriesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'categories.html', {})

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        Author.objects.create(author=user)
    return redirect('/news/')
