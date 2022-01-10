"""
    Contains all the views for performing CRUD operations.
"""

import csv
from io import TextIOWrapper

from botocore.exceptions import ClientError
from django.conf import settings
from museum_api.utils import Converter

from .utils import get_s3_client
from django.forms.models import model_to_dict

from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import UpdateView, CreateView

from practice_app.forms import UploadCSVFileForm, CreateCSVRowForm, EditCSVRowForm
from practice_app.models import MuseumAPICSV
from django.shortcuts import get_object_or_404


@require_http_methods(["GET"])
def list_csv_content_view(request):
    """
    Homepage of the website. Displays uploaded CSV file in table form.
    :param request: HTTPRequest object
    :return: HttpResponse object
    """
    if request.method == 'GET':
        headings = [f.name for f in MuseumAPICSV._meta.get_fields()]
        museum_api_csv_objs = MuseumAPICSV.objects.all()

        return render(request, 'practice_app/index.html', {
            'headings': headings,
            'csv_objs': museum_api_csv_objs,
            })

def csv_to_museum_api_objects(csv_content):
    list_of_dicts = list(csv.DictReader(csv_content.split('\n')))
    rows = [x.values() for x in list_of_dicts]
    objects = []

    for row in rows:
        columns = []
        for column in row:
            columns.append(column)
        objects.append(MuseumAPICSV(
            pk=columns[0],
            isHighlight=columns[1],
            accessionNumber=columns[2],
            accessionYear=columns[3],
            isPublicDomain=columns[4],
            primaryImage=columns[5],
            primaryImageSmall=columns[6],
            additionalImages=columns[7] or '',
            department=columns[8] or '',
            objectName=columns[9] or '',
            title=columns[10] or '',
            culture=columns[11] or '',
            period=columns[12] or '',
            dynasty=columns[13] or '',
            reign=columns[14] or '',
            portfolio=columns[15] or '',
            artistRole=columns[16] or '',
            artistPrefix=columns[17] or '',
            artistDisplayName=columns[18] or '',
            artistDisplayBio=columns[19] or '',
            artistSuffix=columns[20] or '',
            artistAlphaSort=columns[21] or '',
            artistNationality=columns[22] or '',
            artistBeginDate=columns[23] or '',
            artistEndDate=columns[24] or '',
            artistGender=columns[25] or 'm',
            artistWikidata_URL=columns[26] or '',
            artistULAN_URL=columns[27] or '',
            objectDate=columns[28] or '',
            objectBeginDate=columns[29] or '',
            objectEndDate=columns[30] or '',
            medium=columns[31] or '',
            dimensions=columns[32] or '',
            measurements=columns[33] or '',
            creditLine=columns[34] or '',
            geographyType=columns[35] or '',
            city=columns[36] or '',
            state=columns[37] or '',
            county=columns[38] or '',
            country=columns[39] or '',
            region=columns[40] or '',
            subregion=columns[41] or '',
            locale=columns[42] or '',
            locus=columns[43] or '',
            excavation=columns[44] or '',
            river=columns[45] or '',
            classification=columns[46] or '',
            rightsAndReproduction=columns[47],
            linkResource=columns[48] or '',
            metadataDate=columns[49] or '',
            repository=columns[50] or '',
            objectURL=columns[51] or '',
            tags=columns[52] or '',
            objectWikidata_URL=columns[53] or '',
            isTimelineWork=columns[54] or '',
            galleryNumber=columns[55] or -1,
            constituentID=columns[56] or -1,
            role=columns[57] or '',
            name=columns[58] or '',
            constituentULAN_URL=columns[59] or '',
            constituentWikidata_URL=columns[60] or '',
            gender=columns[61] or 'male',
        ))
    return objects

class CSVEditRowView(UpdateView):
    """
    View that allows the user to edit a CSV row.
    """
    queryset = MuseumAPICSV.objects.all()
    pk_url_kwarg = 'objectId'
    form_class = EditCSVRowForm
    template_name = 'practice_app/edit_or_create_csv_row.html'
    success_url = reverse_lazy('practice_app:index')
    required_css_class = 'required'

    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CSVAddNewRowView(CreateView):
    """
     View that allows the user to add new row to the CSV.
    """
    queryset = MuseumAPICSV.objects.all()
    form_class = CreateCSVRowForm
    template_name = 'practice_app/edit_or_create_csv_row.html'
    success_url = reverse_lazy('practice_app:index')
    required_css_class = 'required'

    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@require_http_methods(["GET", "POST"])
def csv_row_delete_view(request, objectId):
    """
    View that allows the user to upload CSV file to the server.
    :param request: HTTPRequest object
    :param objectId: id of the row to be deleted.
    :return: HttpResponse object
    """
    if request.method == 'GET':
        return HttpResponse(status=200)

    if request.method == 'POST':
        row_obj = get_object_or_404(MuseumAPICSV, pk=objectId)

        row_obj.delete()
        return redirect('practice_app:index')


@require_http_methods(["POST"])
def backup_to_s3_view(request):
    if request.method == 'POST':
        # MuseumAPICSV.
        file_name = 'museum_data.csv'
        list_of_dicts = []
        if MuseumAPICSV.objects.all().count() != 0:
            for obj in MuseumAPICSV.objects.all():
                list_of_dicts.append(model_to_dict(obj))
            Converter.convert_to_csv(list_of_dicts, file_name)
            try:
                s3 = get_s3_client('default')
                bucket_name = settings.BACKUP_BUCKET_NAME

                s3.upload_file(file_name, bucket_name, file_name)

                return JsonResponse({
                    'success': 'Backup Completed successfully'
                })
            except ClientError as c_e:
                return JsonResponse({
                    'error': f'Backup failed :{c_e.args[-1]}'
                })
        else:
            return JsonResponse({
                'error': 'Nothing to backup'
            })


def restore_from_s3_view(request):
    if request.method == 'POST':
        file_name = 'museum_data.csv'
        bucket_name = settings.BACKUP_BUCKET_NAME

        try:
            s3 = get_s3_client('default')
            s3.download_file(bucket_name, file_name, file_name)
        except ClientError as cl_e:
            if int(cl_e.response['Error']['Code']) == 404:
                return JsonResponse({
                    'error': 'Nothing to restore'
                })

        try:
            with open(file_name, 'r') as file:
                objects = csv_to_museum_api_objects(file.read())
                MuseumAPICSV.objects.bulk_create(
                    objects,
                    ignore_conflicts=True
                )
                return JsonResponse({
                    'success': 'Backup restored successfully'
                })

        except FileNotFoundError as fn_fe:
            return JsonResponse({
                'error': f'{file_name} not found'
            })

        except ClientError as cl_e:
            return JsonResponse({
                'error': f'Error :{cl_e.args[-1]}'
            })


@require_http_methods(["GET", "POST"])
def csv_file_upload_view(request):
    """
    View that allows the user to upload CSV file to the server.
    :param request: HTTPRequest object
    :return: HttpResponse object
    """
    if request.method == 'GET':
        form = UploadCSVFileForm()
        if MuseumAPICSV.objects.filter(objectId=1).exists() is not None:
            pass
            # return render(request, 'practice_app/csv_upload.html')

        return render(request, 'practice_app/csv_upload.html', {'form': form})

    if request.method == 'POST':
        form = UploadCSVFileForm(request.POST, request.FILES, request=request)
        file_name = str(request.FILES['csv_file'])

        file_name_split = file_name.split('.')
        extension = file_name_split[-1].lower()
        if extension != 'csv':
            raise ValidationError("Not a valid csv file")

        f = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')

        csv_content = f.read()
        objects = csv_to_museum_api_objects(csv_content)

        MuseumAPICSV.objects.bulk_create(
            objects,
            ignore_conflicts=True
        )

        return redirect('practice_app:index')
