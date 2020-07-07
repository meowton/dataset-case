## Data Matching Case

Data Matching project for Festo BigData Intern case presentation 2020. It consists in a working application to match records between data sets and the internal database.  

### Installation
With Python 3 installed, in the project root folder run:  
```
python -m venv ./venv  
source venv/bin/activate  
pip install -r requirements.txt  
```  
And then:
```    
python manage.py makemigrations DataMatcher  
python manage.py sqlmigrate DataMatcher 0001  
python manage.py migrate  
python manage.py createsuperuser --username admin  
python manage.py runserver
```  