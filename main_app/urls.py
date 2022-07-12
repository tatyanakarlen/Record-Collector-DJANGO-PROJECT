from django.urls import path
from . import views 

urlpatterns = [
    #path('home/', views.home, name='home'), 
    path('', views.home, name='home'), 
    path('about/', views.about, name='about'), 
    path('records/', views.records_index, name='index'), 
    path('records/<int:record_id>', views.records_detail, name='detail'), 
    #shows user the form to create record 
    path('records/new_record/', views.RecordCreate.as_view(), name='record_create'),
    path('records/<int:pk>/update/', views.RecordUpdate.as_view(), name='record_update'), 
    path('records/<int:pk>/delete/', views.RecordDelete.as_view(), name='record_delete'), 
    path('records/<int:record_id>/add_airplay/', views.add_airplay, name='add_airplay'), 

    
    path('genres/', views.GenreList.as_view(), name='genres_index'), 
    path('genres/<int:pk>/', views.GenreDetail.as_view(), name='genres_detail'),
    path('genres/create/', views.GenreCreate.as_view(), name='genres_create'), 
    path('genres/<int:pk>/update/', views.GenreUpdate.as_view(), name='genres_update'),
    path('genres/<int:pk>/delete/', views.GenreDelete.as_view(), name='genres_delete'),
    path('records/<int:record_id>/assoc_genre/<int:genre_id>/', views.assoc_genre, name='assoc_genre'), 
    path('accounts/signup/', views.signup, name='signup'),
    path('posts/<int:record_id>/reviews/', views.add_review, name='add_review'), 
    path('posts/<int:record_id>/reviews/delete/<int:review_id>', views.review_delete, name='review_delete'),
]








