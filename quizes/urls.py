from django.urls import path
from . import views

app_name = 'quizes'
urlpatterns = [
    path('', views.index, name='index'),
    path('platform', views.platform, name='enter_platform'),
    path('start', views.start_quiz, name='start'),
    path('preparation', views.preparation, name='preparation'),
    path('simulation_a', views.simulation_a, name='sim_a'),
    path('simulation_b', views.simulation_b, name='sim_b'),
    path('<int:category_id>/<int:question_id>', views.category, name='category'),
    path('save_quiz', views.save_quiz, name='save_quiz'),
    path('save_quiz_details', views.save_quiz_details, name='save_quiz_details'),
    path('sima-start-test', views.sima_start_test, name='sima-start-test'),
    path('sima-start-test/<int:question_id>', views.sima_start_test, name='sima-start-test'),
]
