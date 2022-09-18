from django.shortcuts import render, redirect 
from .models import Record, Genre, Review, User, Track, Photo
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from .forms import AirPlayForm, ReviewForm, ReviewEditForm, AddTrackForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from django.http import HttpResponse



def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



def about(request):
   return render(request, 'about.html')


def home(request):
    records = Record.objects.all()
    return render(request, 
                  'home.html', 
                  {'records': records})

@login_required 
def records_index(request):
    records = Record.objects.filter(user=request.user)
    return render(request, 
                  'records/index.html', 
                  {'records': records})

def new_record(request): 
  return render(request, 'records/new_record_form.html')

class RecordCreate(LoginRequiredMixin,CreateView):
  model = Record
  fields = ['title', 'artist', 'label', 'year', 'description']
  success_url = '/records/'
  def form_valid(self, form):
    # form.istance represents the cat
    #form.instance.user represents the user col of the cat
    #self.request.user is the currently logged-in user
    form.instance.user = self.request.user 
    return super().form_valid(form)

class RecordDelete(DeleteView):
  model = Record
  success_url = '/records/'
  fields = '__all__'

class RecordUpdate(UpdateView):
  model = Record
  success_url = '/records/'
  fields = ['title', 'artist', 'label', 'year', 'description']



S3_BASE_URL = "https://s3.us-east-2.amazonaws.com/"
BUCKET = 'catcollector-tatyana-1984'

def add_photo(request, record_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    #store the file in s3
    filename = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
     s3 = boto3.client('s3')
     s3.upload_fileobj(photo_file, BUCKET, filename)
    #create a DB entry in photo table with url
     url = f"{S3_BASE_URL}{BUCKET}/{filename}"
     Photo.objects.create(url=url, record_id=record_id)
     return redirect(f'/records/{record_id}')
    except: 
      return HttpResponse("something went wrong with uploading to amazon s3")
  else:
    return HttpResponse("no photos were received")
    

def records_detail(request, record_id):
  record = Record.objects.get(id=record_id)
  reviews = Review.objects.filter(record=record_id)
  tracks = Track.objects.filter(record=record_id)
  genres = Genre.objects.all()
  airplay_form= AirPlayForm()
  review_form = ReviewForm()
  add_track_form = AddTrackForm()
  print(tracks)
  if record.user.id == request.user.id: 
    return render(request, 'records/detail.html', { 
    'record': record, 'airplay_form': airplay_form, 'review_form': review_form, 
    'add_track_form': add_track_form, 'genres': genres, 'reviews': reviews, 'tracks': tracks, 
})
  else: 
    return render(request, 'records/public-detail.html', { 
    'record': record, 'review_form': review_form, 'genres': genres, 'reviews': reviews, 'tracks': tracks
})




# add_airplay
@login_required
def add_airplay(request, record_id):
  #create the ModelForm using the data in request.POST
  form = AirPlayForm(request.POST)
  #validate the form
  if form.is_valid():
    #don't save form to db until it has the cat_id assigned 
    new_airplay = form.save(commit=False)
    new_airplay.record_id = record_id 
    new_airplay.save()
  return redirect('detail', record_id=record_id)


@login_required
def assoc_genre(request, record_id, genre_id):
  r = Record.objects.get(id=record_id)
  r.genres.add(genre_id)
  return redirect('detail', record_id=record_id)

class GenreList(ListView):
  model = Genre

class GenreDetail(DetailView):
  model = Genre
  # records = Genre.objects.filter()
  # a2 = Article.objects.filter(reporter__username='John')


def genre_detail(request, genre_id):
  genre = Genre.objects.get(id=genre_id)
  print(genre_id)
  records = Record.objects.filter(genres = genre_id)
  print(records)
  return render(request, 'main_app/genre_detail.html', {'genre': genre, 'records': records} )






  # class SomeView(generic.TemplateView):
  #   var1 = 0
  #   var2 = 1 
  #   template_name = 'some_template.html'

  #   def get_context_data(self, **kwargs):
  #       context = super(SomeView, self).get_context_data(**kwargs)
  #       context.update({'var1': self.var1, 'var2': self.var2})
  #       return context

class GenreCreate(CreateView):
  model = Genre
  fields = ['genre']

class GenreUpdate(UpdateView):
  model = Genre
  fields = ['genre']

class GenreDelete(DeleteView):
  model = Genre
  success_url = '/genres/'



@login_required
def add_review(request, record_id):

   Review.objects.create(
    review = request.POST['review'],
    record = Record.objects.get(id = record_id),
    user = User.objects.get(id = request.user.id)
  )

   return redirect('detail', record_id=record_id)



@login_required
def review_delete(request, review_id, record_id):
  review = Review.objects.get(id = review_id)
  if review.user.id == request.user.id: 
    record = Record.objects.get(id = record_id),
    Review.objects.get(id=review_id).delete()
    return redirect('detail', record_id=record_id)



@login_required
def review_edit(request, review_id, record_id ):
  review = Review.objects.get(id = review_id)
  record = Record.objects.get(id = record_id)
  print(record_id)
  print(review_id)
  review_edit_form = ReviewEditForm()
  return render(request, 
                  'records/editform.html', { 
                  'record': record,
                  'review_edit_form': review_edit_form, 
                  'review': review
  })


@login_required
def review_submit_edit(request, review_id, record_id):
    # record = Record.objects.get(id = record_id)
    review = Review.objects.get(id = review_id)
    if review.user.id == request.user.id: 
     review.review = request.POST['review']
     review.save()
     return redirect('detail', record_id=record_id)


@login_required
def add_track(request, record_id):

   Track.objects.create(
    title = request.POST['title'],
    number = request.POST['number'],
    record = Record.objects.get(id = record_id)
  )

   return redirect('detail', record_id=record_id)








  









  
  
  
  
 

