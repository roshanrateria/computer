
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views



urlpatterns = [
    path('pie-chart/', views.piechart, name='pie-chart'),
    path("",views.index,name="index"),
    path('menu/<str:name>',views.menu,name="Menu"),
    path('createStudent',views.createStud,name="createStud"),
    path('updateStud/<str:i>',views.updateStud,name="updateStud"),
    path('listStudent',views.listStud,name="listStud"),
    path('listbatch/<str:i>',views.listbatch,name="listbatch"),
    path('batchlist',views.batchlist,name="batchlist"),
    path('listcourse/<str:i>',views.listcourse,name="listcourse"),
    path('deleteStudent/<str:i>',views.deleteStud,name="deleteStud"),
    path('createExam/<str:i>',views.createExam,name="createExam"),
    path('reportcard/<str:i>',views.reportcard,name="reportcard"),
    path('department',views.department,name='department'),
    path('listcourse2',views.listcourse2,name="listcourse2"),
    path('createcourse',views.createcourse,name="createcourse"),
    path('department/<str:i>',views.listdept,name='listdept'),
    path('createbatch',views.createbatch,name="createbatch"),
    path('courseperform/<str:i>',views.courseperform,name="cperform"),
    path('createdept',views.createdept,name="createdept"),
    path('clist',views.courselist,name="clist"),
    path('coursechart/<str:i>', views.coursechart, name='coursechart'),
    path('chart/<str:i>',views.chart,name='chart'),
    path('scatterchart',views.demo_scatterchart,name='scatterplot'),
    path('all',views.p,name='p'),
    path('pchart/<str:i>',views.pchart,name='pchart'),
    path('lchart/<str:i>',views.lchart,name='lchart'),
    path('linechart/<str:i>',views.linechart,name='linechart')
  
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# -*- coding: utf-8 -*-

