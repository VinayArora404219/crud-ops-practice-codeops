import csv
from io import TextIOWrapper, StringIO

from django import forms
import pandas as pd
from django.core.exceptions import ValidationError

from practice_app.models import MuseumAPICSV


class UploadCSVFileForm(forms.Form):
    """
    Form that allows the user to upload CSV file.
    """
    csv_file = forms.FileField(label='Upload CSV File')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UploadCSVFileForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UploadCSVFileForm, self).clean()
        f = TextIOWrapper(self.request.FILES['csv_file'].file, encoding='utf-8')
        f.seek(0)

        csv_data = StringIO(f.read())

        df = pd.read_csv(csv_data, sep=",")
        # validate_csv(df)

        # first line (only) contains additional information about the event
        # let's validate that against its form definition

        return cleaned_data


class EditOrCreateCSVRowForm(forms.ModelForm):
    class Meta:
        model = MuseumAPICSV
        fields = '__all__'
