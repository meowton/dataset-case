import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from django_pandas.io import read_frame

from DataMatcher import match
from DataMatcher.models import DataTable, FileUpload, FileUploadForm

# Columns to compare values
left_table = ['first_name', 'last_name', 'cpf', 'credit_card']
right_table = ['first_name', 'last_name', 'cpf', 'credit_card']


def query_objects(model):
    return model.objects.all()


def query_to_dataframe(model):
    query = DataTable.objects.all()
    return read_frame(query)


# Create your views here.
def index(request):
    return render(request, "index.html")


def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/tables/')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})


def compare(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/compare/')
    else:
        form = FileUploadForm()
    response = {'file_list': query_objects(FileUpload),
                'form': form}
    return render(request, 'compare.html', response)


def submit_comparison(request):
    if request.method == "POST":

        try:
            table_list_form = request.POST.getlist('table')

            if len(table_list_form) == 1:
                table_df_1 = query_to_dataframe(DataTable)
                table_df_2 = pd.read_csv(f'.{table_list_form[0]}')
            elif len(table_list_form) > 2:
                messages.error(request, "Select at most two!")
                return redirect('/compare/')
            else:
                table_df_1 = pd.read_csv(f'.{table_list_form[0]}')
                table_df_2 = pd.read_csv(f'.{table_list_form[1]}')

            do_match = match.Matcher(table_df_1,
                                     table_df_2,
                                     left_table,
                                     right_table)

            response = {'file_list': query_objects(FileUpload),
                        'table_matches':
                            do_match.dataset_filter().to_html(header=True,
                                                              index=False)}

        except FileNotFoundError:
            messages.error(request, "File not found.")
            return redirect('/compare/')
        except IndexError:
            messages.error(request, "You need to select at least one!")
            return redirect('/compare/')
        except KeyError:
            return redirect('/compare/')

        return render(request, 'results.html', response)
