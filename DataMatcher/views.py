from django.shortcuts import render
from django_pandas.io import read_frame

from DataMatcher import match
from DataMatcher.models import DataTable

# Columns to compare values
left_table = ['first_name', 'last_name', 'cpf', 'credit_card']
right_table = ['first_name', 'last_name', 'cpf', 'credit_card']

# Matcher class instance
new_match = match.Matcher(
    "./bank-db.csv", "./car-db.csv", left_table, right_table)

# Export results to csv
new_match.export_to_csv(new_match.read_filtered_dataset(), 'exported')


# Test
# print(new_match.dataset_filter())
# print(new_match.read_filtered_dataset())


# Create your views here.
def tables(request):
    query_table = DataTable.objects.all()
    query_to_df = read_frame(query_table).to_html(header=True, index=False)
    matching = new_match.read_filtered_dataset().to_html(header=True, index=False)
    response = {'table_data': query_to_df, 'tables': matching}
    return render(request, "tables.html", response)
