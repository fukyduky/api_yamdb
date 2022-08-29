import csv
from unicodedata import category

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from reviews.models import Category

from . import serializers, views
from rest_framework.decorators import action
from rest_framework.response import Response


fs = FileSystemStorage(location='static/data/')


@action(detail=False, methods=['POST'])
def upload_data(self, request):
    file = request.FILES['file']
    content = file.read()
    file_content = ContentFile(content)
    file_name = fs.save(
        'tmp.csv', file_content
    )
    tmp_file = fs.path(file_name)

    csv_file = open(tmp_file, errors='ignore')
    reader = csv.reader(csv_file)
    next(reader)

    product_list = []
    for id_, row in enumerate(reader):
        (
            name,
            slug,
        ) = row
        product_list.append(
            Category(
                name=name,
                slug=slug,
            )
        )

    Category.objects.bulk_create(product_list)
    return Response('Данные загружены успешно')