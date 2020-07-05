import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from django_pandas.io import read_frame

from DataMatcher import match
from DataMatcher.models import DataTable, FileUpload, FileUploadForm


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
            messages.info(request, "File uploaded successfully!")
            return redirect('/upload/')
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
            table_delete = request.POST.get('delete')
            left_columns = request.POST.get('left_cols')
            right_columns = request.POST.get('right_cols')

            if len(table_list_form) > 0 and table_delete == 'true':
                for table in table_list_form:
                    file = FileUpload.objects.get(file=table.replace('/media/', ''))
                    file.delete()
                return redirect('/compare/')

            if len(table_list_form) == 1:
                table_df_1 = query_to_dataframe(DataTable)
                table_df_2 = pd.read_csv(f'.{table_list_form[0]}')

            elif len(table_list_form) > 2:
                messages.error(request, "Select at most two tables!")
                return redirect('/compare/')

            else:
                table_df_1 = pd.read_csv(f'.{table_list_form[0]}')
                table_df_2 = pd.read_csv(f'.{table_list_form[1]}')

            default_columns = list(set(table_df_1.columns) &
                                   set(table_df_2.columns))

            if left_columns == '':
                left_table = default_columns
            else:
                left_table = left_columns.replace(' ', '').split(',')

            if right_columns == '':
                right_table = default_columns
            else:
                right_table = right_columns.replace(' ', '').split(',')

            do_match = match.Matcher(table_df_1,
                                     table_df_2,
                                     left_table,
                                     right_table)

            response = {'file_list': query_objects(FileUpload),
                        'table_matches':
                            do_match.dataset_filter().to_html(classes=[
                                'table', 'is-bordered', 'is-striped',
                                'is-narrow', 'is-hoverable', 'is-fullwidth'],
                                header=True,
                                index=False)}

        except FileNotFoundError:
            messages.error(request, "It seems the file was not found...")
            return redirect('/compare/')
        except IndexError:
            messages.error(request, "You need to select at least one table!")
            return redirect('/compare/')
        except KeyError:
            messages.error(request, "Invalid column(s) name(s)!")
            return redirect('/compare/')
        except pd.errors.ParserError:
            messages.error(request, "Invalid table(s) format(s)!")
            return redirect('/compare/')
        except ValueError:
            messages.error(request, 'You must provide column(s) '
                                    'name(s) for both tables!')
            return redirect('/compare/')

        return render(request, 'results.html', response)
