from django.forms import ModelForm
from django.forms import Form
from .models import Book
from .models import Author
from .models import Loan
from django.forms import IntegerField
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import BooleanField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BookForm (ModelForm):
    class Meta:
        model = Book
        fields = ['isbn',
            'title',
            'year',
            'edition',
            'pages',
            'author',
            'count',
        ]
        labels = {'isbn': 'ISBN',
            'title': 'Título',
            'year': 'Ano de Publicação',
            'edition': 'Edição',
            'pages': 'Número de Páginas',
            'author': 'Autor',
            'count': 'Quantidade',
        }
    
class RegisterUserForm(UserCreationForm):
    book_admin = BooleanField(required = False)
    author_admin = BooleanField(required = False)
    
    class Meta:
        model = User
        fields = [ 'username',
                'password1',
                'password2',
                'book_admin',
                'author_admin',
        ]
        labels = { 'username' : 'Usuário',
                'password1' : 'Senha',
                'password2' : 'Confirmação de Senha',
                'book_admin' : 'Administração de Livros',
                'author_admin' : 'Administração de Autores',
        }

class AuthorForm (ModelForm):
    class Meta:
        model = Author
        fields = ['name',]
        labels = {'name': 'Nome',}
        
class LoanForm (Form):
    count = IntegerField()
    
    
class SearchBookForm (Form):
    title = CharField(max_length = 100, required = False, label = 'Título')
    isbn = CharField(max_length = 50, required = False, label = 'ISBN')
    
            
