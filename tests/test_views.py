import json
import logging
import sys

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from django.db import IntegrityError
from django.urls import reverse

from practice_app.models import MuseumAPICSV
import os
import csv

logging.basicConfig(
     filename='tests/logs/test_views_error.log',
     level=logging.ERROR,
     format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )


class TestListCSVContentView(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.base_dir = os.path.abspath('tests/tmp_data/')

        with open(os.path.join(cls.base_dir, 'museum_data.csv'), 'r') as f:
            csv_content = f.read()

        list_of_dicts = list(csv.DictReader(csv_content.split('\n')))
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('practice_app:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('practice_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practice_app/index.html')

    def test_lists_all_rows(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        headings = [f.name for f in MuseumAPICSV._meta.get_fields()]
        museum_api_csv_objs = MuseumAPICSV.objects.all()
        self.assertTrue(response.context['headings'], headings)
        self.assertTrue(response.context['csv_objs'], museum_api_csv_objs)

    def test_response_is_not_ok_when_request_method_is_not_get(self):
        url = '/'
        response = self.client.post(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.put(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(url)
        self.assertNotEqual(response.status_code, 200)


class TestCSVRowDeleteView(TestCase):
    obj_id = 1

    @classmethod
    def setUpTestData(cls):
        cls.base_dir = os.path.abspath('tests/tmp_data/')
        csv_content = None

        with open(os.path.join(cls.base_dir, 'museum_data.csv'), 'r') as f:
            csv_content = f.read()

        list_of_dicts = list(csv.DictReader(csv_content.split('\n')))
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/{self.obj_id}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('practice_app:delete_row', kwargs={'objectId': self.obj_id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_existing_row(self):
        response = self.client.post(f'/{self.obj_id}/delete/')
        self.assertEqual(response.status_code, 302)
        try:
            obj = MuseumAPICSV.objects.get(objectId=self.obj_id)
        except MuseumAPICSV.DoesNotExist:
            obj = None

        self.assertIsNone(obj)

    def test_delete_non_existent_row(self):
        response = self.client.post(f'/{86754301}/delete/')
        self.assertEqual(response.status_code, 404)

    def test_response_is_not_ok_when_request_method_is_not_post(self):
        url = f'/{self.obj_id}/delete/'
        response = self.client.put(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(url)
        self.assertNotEqual(response.status_code, 200)


class TestCSVUploadFileView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_dir = os.path.abspath('tests/tmp_data/')

        with open(os.path.join(cls.base_dir, 'museum_data.csv'), 'r') as f:
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/upload_csv/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('practice_app:upload_csv'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('practice_app:upload_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practice_app/csv_upload.html')

    def test_csv_file_upload_when_file_is_csv(self):
        file_obj = None
        try:
            with open(os.path.join(self.base_dir, 'museum_data.csv'), 'r') as f:
                file_obj = SimpleUploadedFile('museum_data.csv', f.read().encode())

        except FileNotFoundError as fn_fe:
            logging.error(f'File not found :{fn_fe.args[-1]}')

        response = self.client.post(reverse('practice_app:upload_csv'), data={
            'csv_file': [file_obj]
        })
        self.assertEqual(response.status_code, 302)

    def test_csv_file_upload_when_file_uploaded_is_not_csv(self):
        file_obj = SimpleUploadedFile('museum_data.java', "Not a csv".encode())
        with self.assertRaises(ValidationError):
            response = self.client.post(reverse('practice_app:upload_csv'), data={'csv_file': [file_obj]})

    def test_response_is_not_ok_when_request_method_is_not_post(self):
        url = '/upload_csv/'
        response = self.client.put(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(url)
        self.assertNotEqual(response.status_code, 200)


class TestCSVEditRowView(TestCase):
    obj_id = 1

    @classmethod
    def setUpTestData(cls):
        cls.base_dir = os.path.abspath('tests/tmp_data/')
        csv_content = None

        with open(os.path.join(cls.base_dir, 'museum_data.csv'), 'r') as f:
            csv_content = f.read()

        list_of_dicts = list(csv.DictReader(csv_content.split('\n')))
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/{self.obj_id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('practice_app:edit_row', kwargs={'objectId': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('practice_app:edit_row', kwargs={'objectId': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practice_app/edit_or_create_csv_row.html')

    def test_edit_row(self):
        row_data = None
        try:
            with open(os.path.join(self.base_dir, 'csv_edit_row_data.json'), 'r') as f:
                row_data = json.load(f)
        except FileNotFoundError as fn_fe:
            logging.error(f'Error file not found :{fn_fe.args[-1]}')

        for key, value in row_data.items():
            if value is None:
                row_data[key] = ''

        response = self.client.post(f'/{self.obj_id}/edit/', row_data)
        self.assertEqual(response.status_code, 200)
        try:
            obj = MuseumAPICSV.objects.get(objectId=1)
        except MuseumAPICSV.DoesNotExist:
            obj = None
        self.assertIsNotNone(obj)

    def test_edit_non_existent_row(self):
        row_data = None
        try:
            with open(os.path.join(self.base_dir, 'csv_edit_row_data.json'), 'r') as f:
                row_data = json.load(f)
        except FileNotFoundError as fn_fe:
            logging.error(f'Error file not found :{fn_fe.args[-1]}')

        for key, value in row_data.items():
            if value is None:
                row_data[key] = ''

        response = self.client.post(f'/{4536540963}/edit/', row_data)
        self.assertEqual(response.status_code, 404)

    def test_response_is_not_ok_when_request_method_is_not_post(self):
        url = f'/{self.obj_id}/edit/'
        response = self.client.put(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(url)
        self.assertNotEqual(response.status_code, 200)


class TestCSVAddNewRowView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_dir = os.path.abspath('tests/tmp_data/')

        with open(os.path.join(cls.base_dir, 'museum_data.csv'), 'r') as f:
            csv_content = f.read()

        list_of_dicts = list(csv.DictReader(csv_content.split('\n')))
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/add_new_row/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('practice_app:add_new_row'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('practice_app:add_new_row'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practice_app/edit_or_create_csv_row.html')

    def test_add_new_row(self):
        row_data = None
        try:
            with open(os.path.join(self.base_dir, 'csv_add_row_data.json'), 'r') as f:
                row_data = json.load(f)
        except FileNotFoundError as fn_fe:
            logging.error(f'Error file not found :{fn_fe.args[-1]}')

        for key, value in row_data.items():
            if value is None:
                row_data[key] = ''
        response = self.client.post('/add_new_row/', row_data)
        self.assertEqual(response.status_code, 200)

    def test_response_is_not_ok_when_request_method_is_not_post(self):
        url = '/add_new_row/'
        response = self.client.put(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(url)
        self.assertNotEqual(response.status_code, 200)






