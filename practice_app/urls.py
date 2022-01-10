from django.urls import path, include
from practice_app.views import csv_file_upload_view, list_csv_content_view, csv_row_delete_view, CSVEditRowView, \
    CSVAddNewRowView, backup_to_s3_view, restore_from_s3_view

app_name = 'practice_app'
urlpatterns = [
    path('', list_csv_content_view, name='index'),
    path('upload_csv/', csv_file_upload_view, name='upload_csv'),
    path('add_new_row/', CSVAddNewRowView.as_view(), name='add_new_row'),
    path('backup_to_s3/', backup_to_s3_view, name='backup_to_s3'),
    path('restore_from_s3/', restore_from_s3_view, name='restore_from_s3'),
    path('<int:objectId>/', include([
        path('edit/', CSVEditRowView.as_view(), name='edit_row'),
        path('delete/', csv_row_delete_view, name='delete_row'),
    ]))
]
