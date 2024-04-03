from django.contrib import admin
from .models import notesTable,booksTable,notesDraftTable,bookPaymentTable,userProfileTable,privateNoteTable,assignmentTable

# Register your models here.
admin.site.register(notesTable)
admin.site.register(notesDraftTable)
admin.site.register(booksTable)
admin.site.register(bookPaymentTable)
admin.site.register(userProfileTable)
admin.site.register(assignmentTable)
admin.site.register(privateNoteTable)
