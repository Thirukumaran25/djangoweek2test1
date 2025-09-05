

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.db.models import Q
from .models import Book, Review
from .forms import ReviewForm, SearchForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET or None)
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        form.instance.book = book
        form.instance.user = self.request.user
        messages.success(self.request, 'Your review has been added!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.kwargs['pk']})

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def form_valid(self, form):
        messages.success(self.request, 'Your review has been updated!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.get_object().book.pk})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.is_staff

    def get_success_url(self):
        messages.success(self.request, 'Review successfully deleted.')
        return reverse_lazy('book-detail', kwargs={'pk': self.get_object().book.pk})
    

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')


def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login') 
    return redirect('/') 