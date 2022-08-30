from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from .models import Category, Comment, Genre, Review, Title, User


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == 'POST':
            csv_file = request.FILES['csv_upload']

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Неправильный тип файла!')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode('utf-8')
            csv_data = file_data.split("\n")

            for x in csv_data[1:]:
                fields = x.split(',')
                created = Category.objects.update_or_create(
                    name=fields[1],
                    slug=fields[2],
                )
                created.save()
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {'form': form}
        return render(request, 'admin/csv_upload.html', data)


admin.site.register(Category, CategoryAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == 'POST':
            csv_file = request.FILES['csv_upload']

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Неправильный тип файла!')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode('utf-8')
            csv_data = file_data.split("\n")

            for x in csv_data[1:]:
                fields = x.split(',')
                created = Genre.objects.update_or_create(
                    name=fields[1],
                    slug=fields[2],
                )
                created.save()
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {'form': form}
        return render(request, 'admin/csv_upload.html', data)


admin.site.register(Genre, GenreAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'role', 'bio', 'first_name', 'last_name')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == 'POST':
            csv_file = request.FILES['csv_upload']

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Неправильный тип файла!')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode('utf-8')
            csv_data = file_data.split("\n")

            for x in csv_data[1:]:
                fields = x.split(',')
                created = User.objects.update_or_create(
                    username=fields[1],
                    email=fields[2],
                    role=fields[3],
                    bio=fields[4],
                )
                created.save()
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {'form': form}
        return render(request, 'admin/csv_upload.html', data)


admin.site.register(User, UserAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == 'POST':
            csv_file = request.FILES['csv_upload']

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Неправильный тип файла!')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode('utf-8')
            csv_data = file_data.split("\n")

            for x in csv_data[1:]:
                fields = x.split(',')
                created = Title.objects.update_or_create(
                    name=fields[1],
                    year=fields[2],
                )
                created.save()
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {'form': form}
        return render(request, 'admin/csv_upload.html', data)


admin.site.register(Title, TitleAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'text', 'author', 'score', 'pub_date')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == 'POST':
            csv_file = request.FILES['csv_upload']

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Неправильный тип файла!')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode('utf-8')
            csv_data = file_data.split("\n")

            for x in csv_data[1:]:
                fields = x.split(',')
                created = Title.objects.update_or_create(
                    title_id=fields[1],
                    text=fields[2],
                    author=fields[3],
                    score=fields[4],
                    pub_date=fields[5],
                )
                created.save()
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {'form': form}
        return render(request, 'admin/csv_upload.html', data)


admin.site.register(Review, ReviewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review_id', 'text', 'author', 'pub_date')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == 'POST':
            csv_file = request.FILES['csv_upload']

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Неправильный тип файла!')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode('utf-8')
            csv_data = file_data.split("\n")

            for x in csv_data[1:]:
                fields = x.split(',')
                created = Comment.objects.update_or_create(
                    review_id=fields[1],
                    text=fields[2],
                    author=fields[3],
                    pub_date=fields[4],
                )
                created.save()
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {'form': form}
        return render(request, 'admin/csv_upload.html', data)


admin.site.register(Comment, CommentAdmin)
