from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import notesTable,booksTable,notesDraftTable,bookPaymentTable,userProfileTable,assignmentTable,privateNoteTable

# Create your views here.
def index(request):
    notes = notesTable.objects.all()
    return render(request, 'index.html', {'notes':notes})

def loginPage(request):
    global newUser
    if request.method == 'POST':
        uname = request.POST['username']
        password = request.POST['password']

        newUser = auth.authenticate(username=uname,password=password)
        if newUser is not None:
            print(newUser.email)
            auth.login(request,newUser)
            return redirect(userHome)
        else:
            return render(request, './screens/login.html', {'failed': 'User Not Found!!!'})
        
    return render(request, './screens/login.html')

def registerPage(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        userExitst = User.objects.filter(username=uname)
        emailExists = User.objects.filter(email=email)

        if password == confirmpassword:
            if userExitst:
                return render(request, './screens/register.html', {'failed':'User with name already exists!'})
            else:
                if emailExists:
                    return render(request, './screens/register.html', {'failed':'User with email already exists!'})
                else:
                    User.objects.create_user(username=uname,email=email,password=password).save()
                    return render(request, './screens/register.html', {'success':'User Created Successfully!'})


        else:
            return render(request, './screens/register.html', {'failed':'Passwords don\'t match!'})

    return render(request, './screens/register.html')
    


def logoutUser(request):
    logout(request)
    return redirect(loginPage)


@login_required
def userHome(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        image = request.FILES['image']
        note = request.POST['note']
        author = newUser.username

        notesDraftTable(subject=subject,image=image,note=note,author=author).save()

        notes = notesTable.objects.all()[:10][::-1]
        books = booksTable.objects.all()[:3][::-1]

        return render(request, './screens/userhome.html', {'user':newUser,'success':'note drafted successfully, go to drafts to save','notes':notes,'books':books})

    notes = notesTable.objects.all()[:10][::-1]
    books = booksTable.objects.all()[:3][::-1]
    
    return render(request, './screens/userhome.html', {'user':newUser, 'notes':notes,'books':books})


@login_required
def viewNote(request,pk):
    note = notesTable.objects.get(id=pk)

    makeNotePrivate = True
    try:
        profile = userProfileTable.objects.get(user=note.author)
    except userProfileTable.DoesNotExist:
        profile = {'isPrivate': False}

    # print(profile.isPrivate)

    
    noteIsPrivate = False
    try:
        if profile.isPrivate:
            noteIsPrivate = True
    except AttributeError:
        if profile['isPrivate']:
            noteIsPrivate = True
        


    try:
        currentNote = privateNoteTable.objects.get(user=newUser.username,uploadedBy=note.author,note=note.subject)
    except privateNoteTable.DoesNotExist:
        currentNote = None
    
    return render(request, './screens/viewnote.html', {'user':newUser,'note':note,'noteIsPrivate':noteIsPrivate,'requestMade':currentNote})

def viewPublicNote(request,pk):
    note = notesTable.objects.get(id=pk)
    return render(request, './screens/viewpublicnote.html', {'note':note})

@login_required
def allNotes(request):
    try:
        profile = userProfileTable.objects.get(user=newUser.username)
    except userProfileTable.DoesNotExist:
        profile = None

    if request.method == 'POST':
        keyword = request.POST['notesearch']

        if(keyword == ''):
            notes = notesTable.objects.all()
        elif notesTable.objects.filter(author__icontains=keyword):
            notes = notesTable.objects.filter(author__icontains=keyword)
        elif notesTable.objects.filter(subject__icontains=keyword):
            notes = notesTable.objects.filter(subject__icontains=keyword)
        else:
            notes = {}

        return render(request, './screens/allnotes.html', {'notes':notes,'profile':profile})



    notes = notesTable.objects.all()
    return render(request, './screens/allnotes.html', {'notes':notes,'profile':profile})

@login_required
def deleteNote(request,pk):
    note = notesTable.objects.get(id=pk)
    note.delete()
    return redirect(allNotes)

@login_required
def viewDrafts(request):
    notes = notesDraftTable.objects.all()
    return render(request, './screens/notedrafts.html', {'notes':notes})

@login_required
def editDraft(request,pk):
    row = notesDraftTable.objects.get(id=pk)

    if request.method == 'POST':
        row.subject = request.POST['subject']
        row.image = request.FILES['image']
        row.note = request.POST['note']
        row.author = newUser.username

        row.save()

        notes = notesTable.objects.all()[:10][::-1]
        books = booksTable.objects.all()[:3][::-1]

        return render(request, './screens/userhome.html', {'user':newUser,'success':'note drafted successfully, go to drafts to save','notes':notes,'books':books})

    notes = notesTable.objects.all()[:10][::-1]
    books = booksTable.objects.all()[:3][::-1]

    return render(request, './screens/userhome.html', {'draft':row,'notes':notes,'books':books})

@login_required
def saveDraft(requst,pk):
    row = notesDraftTable.objects.get(id=pk)
    row.saved = True
    row.save()

    notesTable(subject=row.subject,image=row.image,note=row.note,author=row.author).save()
    return redirect(viewDrafts)

@login_required
def deleteDraft(request,pk):
    row = notesDraftTable.objects.get(id=pk)
    row.delete()
    return redirect(viewDrafts)

@login_required
def allBooks(request):    
    if request.method == 'POST':
        keyword = request.POST['booksearch']

        if(keyword == ''):
            books = booksTable.objects.all()
        elif booksTable.objects.filter(title__icontains=keyword):
            books = booksTable.objects.filter(title__icontains=keyword)
        elif booksTable.objects.filter(author__icontains=keyword):
            books = booksTable.objects.filter(author__icontains=keyword)
        else:
            books = {}
        
        return render(request, './screens/allbooks.html', {'books':books})

    books = booksTable.objects.all()
    return render(request, './screens/allbooks.html', {'books':books})

@login_required
def uploadBook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        uploadedBy = newUser.username
        image = request.FILES['image']
        price = request.POST['price']
        book = request.FILES['book']

        if price == '':
            price = 0

        booksTable(title=title,author=author,uploadedBy=uploadedBy,coverImage=image,price=price,book=book).save()

        return render(request, './screens/uploadbook.html', {'success':'book saved successfully'})
    
    return render(request, './screens/uploadbook.html')

@login_required
def viewBook(request,pk):
    book = booksTable.objects.get(id=pk)
    try:
        bookPurchased = bookPaymentTable.objects.get(user=newUser.username, book=book.title)
    except bookPaymentTable.DoesNotExist:
        bookPurchased = {'approved': False}
    return render(request, './screens/viewbook.html', {'book':book,'user':newUser,'purchase':bookPurchased})

@login_required
def deleteBook(request,pk):
    book = booksTable.objects.get(id=pk)
    book.delete()
    return redirect(allBooks)

def publicNotes(request):
    notes = notesTable.objects.all()
    return render(request, './screens/publicnotes.html', {'notes':notes})

@login_required
def userProfile(request):
    if request.method == 'POST':
        user = newUser.username
        college = request.POST['college']
        designation = request.POST['designation']
        try:
            isPrivate = request.POST['isPrivate']
        except KeyError:
            isPrivate = False

        userProfileTable(user=user,college=college,designation=designation,isPrivate=isPrivate).save()

        return redirect(userProfile)


    notes = notesTable.objects.filter(author=newUser.username)
    books = booksTable.objects.filter(uploadedBy=newUser.username)
    try:
        profileDetails = userProfileTable.objects.get(user=newUser.username)
    except userProfileTable.DoesNotExist:
        profileDetails = {}
    return render(request, './screens/userprofile.html',{'notes':notes,'books':books,'profileDetails':profileDetails})

@login_required
def payForBook(request,pk):
    userBook = booksTable.objects.get(id=pk)

    if request.method == 'POST':
        user = newUser.username
        book = userBook.title
        amount = userBook.price

        bookPaymentTable(user=user,uploadedBy=userBook.uploadedBy,book=book,amount=amount).save()
        return render(request, './screens/payforbook.html',{'success':True})



    return render(request, './screens/payforbook.html')


def bookPaymentRequests(request):
    requests = bookPaymentTable.objects.filter(uploadedBy=newUser.username)
    return render(request, './screens/bookpaymentrequests.html', {'requests':requests})

def acceptBookPayment(request,pk):
    req = bookPaymentTable.objects.get(id=pk)
    req.approved = True
    req.save()
    return redirect(bookPaymentRequests)

def rejectBookPayment(request,pk):
    req = bookPaymentTable.objects.get(id=pk)
    req.approved = False
    req.save()
    return redirect(bookPaymentRequests)

def updateUserProfile(request, pk):
    try:
        profile = userProfileTable.objects.get(user=pk)
    except userProfileTable.DoesNotExist:
        profile = None

    if request.method == 'POST':
        profile.college = request.POST['college']
        profile.designation = request.POST['designation']

        try:
            profile.isPrivate = request.POST['isPrivate']
        except KeyError:
            profile.isPrivate = False

        profile.save()

        return redirect(userProfile)

    return render(request, './screens/updateuserprofile.html', {'userProfile':profile})

def uploadAssignment(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        assignment = request.FILES['assignment']

        assignmentTable(user=newUser.username,subject=subject,assignment=assignment).save()
        return redirect(allAssignments)

    return render(request, './screens/uploadassignment.html')

def allAssignments(request):
    assignments = assignmentTable.objects.all()

    if request.method == 'POST':
        keyword = request.POST['searchassignment']

        if keyword == '':
            assignments = assignmentTable.objects.all()
        elif assignmentTable.objects.filter(user__icontains=keyword):
            assignments = assignmentTable.objects.filter(user__icontains=keyword)
        elif assignmentTable.objects.filter(subject__icontains=keyword):
            assignments = assignmentTable.objects.filter(subject__icontains=keyword)
        elif assignmentTable.objects.filter(time__icontains=keyword):
            assignments = assignmentTable.objects.filter(time__icontains=keyword)
        else:
            assignments = {}

        return render(request, './screens/allassignments.html',{'assignments':assignments})

    return render(request, './screens/allassignments.html',{'assignments':assignments})

def noteViewRequest(request,pk):
    currentNote = notesTable.objects.get(id=pk)
    user = newUser.username
    author = currentNote.author
    note = currentNote.subject

    if privateNoteTable(user=user,uploadedBy=author,note=note):
        return redirect(allNotes)

    privateNoteTable(user=user,uploadedBy=author,note=note).save()

    return redirect(allNotes)

def noteRequests(request):
    req = privateNoteTable.objects.filter(uploadedBy=newUser.username)
    return render(request,'./screens/noterequests.html', {'requests':req})

def acceptNoteRequest(request,pk):
    req = privateNoteTable.objects.get(id=pk)
    req.approved = True
    req.save()
    return redirect(noteRequests)

def rejectNoteRequest(request,pk):
    req = privateNoteTable.objects.get(id=pk)
    req.approved = False
    req.save()
    return redirect(noteRequests)