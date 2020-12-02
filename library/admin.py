from django.contrib import admin
from .models import Book
from .models import Author
from .models import Loan
from .models import UserProfile

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(UserProfile)
