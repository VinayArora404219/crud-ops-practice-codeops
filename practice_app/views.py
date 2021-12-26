import csv
from io import TextIOWrapper

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from practice_app.forms import UploadCSVFileForm, EditOrCreateCSVRowForm
from practice_app.models import MuseumAPICSV
from django.shortcuts import get_object_or_404


def index(request):
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


class CSVEditRowView(UpdateView):
    """
    Class that allows to edit a CSV row.
    """
    queryset = MuseumAPICSV.objects.all()
    pk_url_kwarg = 'objectId'
    form_class = EditOrCreateCSVRowForm
    template_name = 'practice_app/edit_or_create_csv_row.html'
    success_url = reverse_lazy('practice_app:index')
    required_css_class = 'required'


class CSVAddNewRowView(CreateView):
    """
     Class that allows to add new row to the CSV.
    """
    queryset = MuseumAPICSV.objects.all()
    form_class = EditOrCreateCSVRowForm
    template_name = 'practice_app/edit_or_create_csv_row.html'
    success_url = reverse_lazy('practice_app:index')
    required_css_class = 'required'


def csv_row_delete_view(request, objectId):
    """
        View that allows the user to upload CSV file to the server.
        :param request: HTTPRequest object
        :param objectId: id of the row to be deleted.
        :return: HttpResponse object
        """
    if request.method == 'GET':
        row_obj = get_object_or_404(MuseumAPICSV, pk=objectId)

        row_obj.delete()
        return redirect('practice_app:index')


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
        list_of_dicts = list(csv.DictReader(csv_content.split('\n')))
        headings = list_of_dicts[0].keys()
        rows = [x.values() for x in list_of_dicts]

        for row in rows:
            columns = []
            for column in row:
                columns.append(column)
            try:
                MuseumAPICSV.objects.create(
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

                )
            except IntegrityError:
                pass

        return redirect('practice_app:index')



