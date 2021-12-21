from django.urls import path, include
from practice_app.views import csv_file_upload_view, index, csv_detail_view, csv_row_delete_view, CSVEditRowView, CSVAddNewRowView

app_name = 'practice_app'
urlpatterns = [
    path('', index, name='index'),
    path('upload_csv/', csv_file_upload_view, name='upload_csv'),
    path('add_new_row/', CSVAddNewRowView.as_view(), name='add_new_row'),
    path('<int:objectId>/', include([
        path('edit/', CSVEditRowView.as_view(), name='edit_row'),
        path('delete/', csv_row_delete_view, name='delete_row'),
    ]))
]
