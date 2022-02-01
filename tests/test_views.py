"""
    Contains tests for views.py
"""

import csv
import json
import logging
import os
import sys

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from practice_app.models import MuseumAPICSV

logging.basicConfig(
    filename='tests/logs/test_views_error.log',
    level=logging.ERROR,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


def populate_tmp_data(csv_file_path):
    """
    Populates temporary data to test database from specified csv file

    :param csv_file_path: path of the csv file from which data needs to be populated
    """

    with open(csv_file_path, 'r', encoding='utf-8') as file_ptr:
        csv_content = file_ptr.read()

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


class TestListCSVContentView(TestCase):
    """
    Tests the functionality of list_csv_content_view function.
    """
    base_dir = os.path.abspath('tests/Truth/')
    @classmethod
    def setUpTestData(cls):
        """
        Sets up temporary data in the test database for testing.
        """
        populate_tmp_data(os.path.join(cls.base_dir, 'museum_data.csv'))

    def test_url_exists(self):
        """
        Tests whether the url exists and is a valid url.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        """
        Tests whether the url is accessible by name.
        """
        response = self.client.get(reverse('practice_app:index'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        """
        Tests whether the view is using correct template.
        """
        response = self.client.get(reverse('practice_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practice_app/index.html')

    def test_list_all_rows(self):
        """
        Tests whether the view lists all the rows correctly.
        """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # getting all the headings from the model
        headings = [f.name for f in MuseumAPICSV._meta.get_fields()]

        # fetching all the objects from MuseumAPICSV model.
        museum_api_csv_objs = MuseumAPICSV.objects.all()

        self.assertTrue(response.context['headings'], headings)
        self.assertTrue(response.context['csv_objs'], museum_api_csv_objs)

    def test_response_invalid_for_disallowed_methods(self):
        """
        Tests whether the response is not ok when request method is
        not get.
        """
        endpoint = '/'
        response = self.client.post(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.put(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(endpoint)
        self.assertNotEqual(response.status_code, 200)


class TestCSVRowDeleteView(TestCase):
    """
    Tests functionality of csv_row_delete_view function.
    """
    obj_id = 1
    base_dir = os.path.abspath('tests/Truth/')

    @classmethod
    def setUpTestData(cls):
        """
        Sets up temporary data in the test database for testing.
        """

        populate_tmp_data(os.path.join(cls.base_dir, 'museum_data.csv'))

    def test_url_exists(self):
        """
        Tests whether the url exists and is a valid url.
        """
        response = self.client.get(f'/{self.obj_id}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        """
        Tests whether the url is accessible by name.
        """
        response = self.client.get(
            reverse('practice_app:delete_row', kwargs={'objectId': self.obj_id})
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_existing_row(self):
        """
        Tests the functionality of deleting an existing row.
        """
        response = self.client.post(f'/{self.obj_id}/delete/')
        self.assertEqual(response.status_code, 302)
        try:
            obj = MuseumAPICSV.objects.get(objectId=self.obj_id)
        except MuseumAPICSV.DoesNotExist:
            obj = None

        self.assertIsNone(obj)

    def test_delete_non_existent_row(self):
        """
        Tests whether the server raises an exception when trying to delete
        a non-existent row.
        """
        response = self.client.post(f'/{86754301}/delete/')
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.context['exception'])
        self.assertEqual(
            response.context['exception'],
            'No MuseumAPICSV matches the given query.'
        )

    def test_response_invalid_for_disallowed_methods(self):
        """
        Tests whether the response is not ok when request method is
        not post.
        """
        endpoint = f'/{self.obj_id}/delete/'
        response = self.client.put(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(endpoint)
        self.assertNotEqual(response.status_code, 200)


class TestCSVUploadFileView(TestCase):
    """
    Tests functionality of csv_file_upload_view function.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Sets up temporary data in the test database for testing.
        """
        cls.base_dir = os.path.abspath('tests/Truth/')
        populate_tmp_data(os.path.join(cls.base_dir, 'museum_data.csv'))

    def test_url_exists(self):
        """
        Tests whether the url exists and is a valid url.
        """
        response = self.client.get('/upload_csv/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        """
        Tests whether the url is accessible by name.
        """
        response = self.client.get(reverse('practice_app:upload_csv'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        """
        Tests whether the view is using correct template.
        """
        response = self.client.get(reverse('practice_app:upload_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practice_app/csv_upload.html')

    def test_upload_csv_file(self):
        """
        Tests the functionality of uploading CSV file.
        """
        file_obj = None
        try:
            with open(
                    os.path.join(
                        self.base_dir,
                        'museum_data.csv',
                    ),
                    'r',
                    encoding='utf-8'
            ) as file_ptr:
                file_obj = SimpleUploadedFile('museum_data.csv', file_ptr.read().encode())

        except FileNotFoundError as fn_fe:
            logging.error('File not found %s:', {fn_fe.args[-1]})

        response = self.client.post(reverse('practice_app:upload_csv'), data={
            'csv_file': [file_obj]
        })
        self.assertEqual(response.status_code, 302)

    def test_upload_non_csv(self):
        """
        Test whether the view raises ValidationError when user tries to upload a
        non CSV file.
        """
        file_obj = SimpleUploadedFile(
            'museum_data.java',
            "Not a csv".encode()
        )

        with self.assertRaises(ValidationError):
            self.client.post(
                reverse('practice_app:upload_csv'),
                data={'csv_file': [file_obj]}
            )

    def test_response_invalid_for_disallowed_methods(self):
        """
        Tests whether the response is not ok when request method is
        not post.
        """
        endpoint = '/upload_csv/'
        response = self.client.put(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(endpoint)
        self.assertNotEqual(response.status_code, 200)


class TestCSVEditRowView(TestCase):
    """
    Tests functionality of CSVEditRowView class.
    """
    base_dir = os.path.abspath('tests/Truth/')
    obj_id = 1

    @classmethod
    def setUpTestData(cls):
        """
        Sets up temporary data in the test database for testing.
        """
        populate_tmp_data(os.path.join(cls.base_dir, 'museum_data.csv'))

    def test_url_exists(self):
        """
        Tests whether the url exists and is a valid url.
        """
        response = self.client.get(f'/{self.obj_id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        """
        Tests whether the url is accessible by name.
        """
        response = self.client.get(reverse('practice_app:edit_row', kwargs={'objectId': 1}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        """
        Tests whether the view is using correct template.
        """
        response = self.client.get(reverse('practice_app:edit_row', kwargs={'objectId': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practice_app/edit_or_create_csv_row.html')

    def test_edit_row(self):
        """
        Testing the edit functionality of the view.
        """
        row_data = None
        try:
            with open(
                    os.path.join(self.base_dir, 'csv_edit_row_data.json'),
                    'r',
                    encoding='utf-8'
            ) as file_ptr:
                row_data = json.load(file_ptr)
        except FileNotFoundError as fn_fe:
            logging.error('File not found %s:', {fn_fe.args[-1]})

        for key, value in row_data.items():
            if value is None:
                row_data[key] = ''

        response = self.client.post(f'/{self.obj_id}/edit/', row_data)
        self.assertEqual(response.status_code, 302)

        obj = MuseumAPICSV.objects.get(objectId=self.obj_id)

        # checking whether isHighlight property of the object is edited properly.
        self.assertEqual(obj.isHighlight, row_data['isHighlight'])

    def test_edit_non_existent_row(self):
        """
        Test if it raises DoesNotExist Exception when trying to update a non-existing row.
        """
        row_data = {"objectID": 4536540963, "isHighlight": False, "accessionNumber": "1979.486",
                    "accessionYear": "1979", "isPublicDomain": False,
                    }

        response = self.client.post(f'/{4536540963}/edit/', row_data)
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.context['exception'])
        self.assertEqual(
            response.context['exception'],
            'No museum apicsv found matching the query'
        )

    def test_response_invalid_for_disallowed_methods(self):
        """
        Tests whether the response is not ok when request method is
        not post.
        """
        endpoint = f'/{self.obj_id}/edit/'
        response = self.client.put(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(endpoint)
        self.assertNotEqual(response.status_code, 200)


class TestCSVAddNewRowView(TestCase):
    """
    Tests functionality of CSVAddNewRowView class.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Sets up temporary data in the test database for testing.
        """
        cls.base_dir = os.path.abspath('tests/Truth/')
        populate_tmp_data(os.path.join(cls.base_dir, 'museum_data.csv'))

    def test_url_exists(self):
        """
        Tests whether the url exists and is a valid url.
        """
        response = self.client.get('/add_new_row/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        """
        Tests whether the url is accessible by name.
        """
        response = self.client.get(reverse('practice_app:add_new_row'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        """
        Tests whether the view is using correct template.
        """
        response = self.client.get(reverse('practice_app:add_new_row'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practice_app/edit_or_create_csv_row.html')

    def test_add_new_row(self):
        """
        Test functionality of adding a new row to CSV file.
        """
        row_data = None
        try:
            with open(
                    os.path.join(self.base_dir, 'csv_add_row_data.json'),
                    'r',
                    encoding='utf-8'
            ) as file_ptr:
                row_data = json.load(file_ptr)
        except FileNotFoundError as fn_fe:
            logging.error('File not found %s:', {fn_fe.args[-1]})

        for key, value in row_data.items():
            if value is None:
                row_data[key] = ''
        response = self.client.post('/add_new_row/', row_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MuseumAPICSV.objects.last().objectId, 16)

    def test_add_existing_row(self):
        """
        Test if the view raises error if the user tries to add an existing row.
        """
        try:
            with open(
                os.path.join(self.base_dir, 'csv_add_existing_row.json'),
                'r',
                encoding='utf-8'
            ) as file_ptr:
                csv_row_content = json.load(file_ptr)

        except FileNotFoundError as fn_fe:
            logging.error('File not found %s:', {fn_fe.args[-1]})
            sys.exit(1)

        for key, value in csv_row_content.items():
            if value is None:
                csv_row_content[key] = ''
        response = self.client.post('/add_new_row/', csv_row_content)
        self.assertEqual(response.status_code, 200)

        # check if the form is raising errors.

        self.assertEqual(
            response.context['form'].errors['objectId'][0],
            'Museum apicsv with this ObjectId already exists.'
        )

    def test_response_invalid_for_disallowed_methods(self):
        """
        Tests whether the response is not ok when request method is
        not post.
        """
        endpoint = '/add_new_row/'
        response = self.client.put(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.delete(endpoint)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.patch(endpoint)
        self.assertNotEqual(response.status_code, 200)
