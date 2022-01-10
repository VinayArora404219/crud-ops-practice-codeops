from io import TextIOWrapper, StringIO

import pandas as pd
from django import forms

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


class EditCSVRowForm(forms.ModelForm):
    class Meta:
        model = MuseumAPICSV
        exclude = ('objectId', )

    def clean(self):
        cleaned_data = super(EditCSVRowForm, self).clean()
        for key, value in cleaned_data.items():
            if value is None:
                cleaned_data[key] = ''

        return cleaned_data


class CreateCSVRowForm(forms.ModelForm):
    class Meta:
        model = MuseumAPICSV
        fields = '__all__'

    def clean(self):
        cleaned_data = super(CreateCSVRowForm, self).clean()
        for key, value in cleaned_data.items():
            if value is None:
                cleaned_data[key] = ''
            if key == 'galleryNumber' or key == 'constituentID':
                cleaned_data[key] = -1

        return cleaned_data
