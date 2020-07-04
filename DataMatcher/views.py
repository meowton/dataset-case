from django.shortcuts import render, redirect
from django_pandas.io import read_frame

from DataMatcher import match
from DataMatcher.forms import FileUploadForm
from DataMatcher.models import DataTable, FileUpload

# Columns to compare values
left_table = ['first_name', 'last_name', 'cpf', 'credit_card']
right_table = ['first_name', 'last_name', 'cpf', 'credit_card']


# Export results to csv
# new_match.export_to_csv(new_match.read_filtered_dataset(), 'exported')


# Test
# print(new_match.dataset_filter())
# print(new_match.read_filtered_dataset())


# Create your views here.
def tables(request):
    query_table = DataTable.objects.all()
    table_dataframe = read_frame(query_table)

    # query_to_df.to_csv('test.csv')

    # Matcher class instance
    try:
        new_match = match.Matcher(table_dataframe,
                                  './car-db.csv',
                                  left_table,
                                  right_table)

        response = {
            'table_from_db': table_dataframe.to_html(header=True,
                                                     index=False),
            'table_matches': new_match.dataset_filter().to_html(header=True,
                                                                index=False)}
    except FileNotFoundError:
        response = {
            'table_from_db': table_dataframe.to_html(header=True,
                                                     index=False),
            'table_matches': ''}

    return render(request, "tables.html", response)


def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/tables/')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {
        'form': form
    })


def compare(request):
    query_files = FileUpload.objects.all()
    response = {'file_list': query_files}
    return render(request, 'compare.html', response)


def submit_comparison(request):
    if request.method == "POST":
        title = request.POST.getlist('table')
        print(title)
        pass
