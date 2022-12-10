from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date
import datetime
from random import randint
from sklearn.preprocessing import LabelEncoder

def index(request):
    return render(request, "College/menu.html",{})
def createStud(request):
    if request.method == "POST":
      
        n=Students(phone_number= request.POST['phone_number'],email= request.POST['email'], Name=request.POST['Name'],rollno= request.POST['rollno'])
        n.StudID=request.POST['ID']
        n.save()
        b=batch.objects.get(batch_id=request.POST['batch'])
        b.studs.add(n)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "College/createStud.html",{'s':batch.objects.all()})
def createcourse(request):
    if request.method == "POST":
       
        n=course(Name= request.POST['Name'])
        n.course_id=request.POST['ID']
        n.save()
        for a in request.POST:
            if a not in ['csrfmiddlewaretoken','ID','Name']:
               
                b=batch.objects.get(batch_id=a)
                b.courses.add(n)
                b.save()
            
            
        return HttpResponseRedirect(reverse("index"))
      
    else:
        return render(request, "College/createcourse.html",{'batch':batch.objects.all()})
def createbatch(request):
    if request.method == "POST":
     
       n=batch(name=request.POST['Name'])
       n.batch_id=request.POST['ID']
       d=dept.objects.get(dept_id=request.POST['dept'])
       n.dept_name=d.name
       n.save()
       d.batches.add(n)
     
       return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "College/createbatch.html",{'s':dept.objects.all(),
                                                            'course':course.objects.all(),
                                                            'stud':Students.objects.all()})
        
    
def menu(request,name):
    return render(request,f"College/{name}.html")
def listStud(request):
    return render(request,"College/list.html",{'stud':Students.objects.all()})
def updateStud(request,i):
    if request.method == "POST":
        print(request.POST)
        n=Students.objects.get(StudID=i)
        for a in batch.objects.all():
            if n in a.studs.all():
                a.studs.remove(n)
                break
      
        n.StudID=request.POST['ID']
        n.phone_number=request.POST['phone_number']
        n.email=request.POST['email']
        n.Name=request.POST['Name']
        n.rollno=request.POST['rollno']
        n.save()
        b=batch.objects.get(batch_id=request.POST['batch'])
        b.studs.add(n)
        return HttpResponseRedirect(reverse("index"))
    else:
        b=None
        for a in batch.objects.all():
            if Students.objects.get(StudID=i) in a.studs.all():
                b=a
        return render(request, "College/updateStud.html",{'stud':Students.objects.get(StudID=i),
                                                          'batch':b.batch_id,
                                                          's':batch.objects.all()})
def deleteStud(request,i):
    instance = Students.objects.get(StudID=i)
    instance.delete()    
    return HttpResponseRedirect(reverse("listStud"))

def listbatch(request,i):
    b=batch.objects.get(batch_id=i)
    return render(request,"College/list.html",{'stud':b.studs.all()})
def batchlist(request):    
    return render(request,"College/batchlist.html",{'batch':batch.objects.all()})
def listcourse(request,i):
    
    return render(request,"College/listcourse.html",{'course':batch.objects.get(batch_id=i).courses.all()})
def listcourse2(request):
    
    return render(request,"College/listexam.html",{'course':course.objects.all()})

def createExam(request,i):
    q=course.objects.get(course_id=i)
    
    b=[]
    for t in batch.objects.all():
        if q in t.courses.all():
            
            for s1 in t.studs.all():
                b.append({'StudID':s1.StudID})
            
            
    
    if request.method=='POST':
        
        for a in b:
            l= int(request.POST[a['StudID']])
            m=Marks.objects.create(mark=l)
            m.student.add(Students.objects.get(StudID=a['StudID']))
            if(l>=90):
                m.grade='A'
            elif(l>=80):
                m.grade='B'
            elif(l>=70):
                m.grade='C'
            elif(l>=60):
                m.grade='D'
            elif(l>=50):
                m.grade='E'
            else:
                m.grade='F'
            
            m.save()
            
            q.Marks_Obtained.add(m)
    
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"College/createExam.html",{'stud':b,
                                                         'i':i})
def reportcard(request,i):
    a=Students.objects.get(StudID=i)
    filename = f"{a.Name}.txt"
    s=0
    c=0
    content = f"Name: {a.Name} Student ID:{a.StudID}\n"
    content+="Course Name\t Course ID \t Marks \t Grade \t Pass or Fail\n"
    for q in course.objects.all():
     for w in  q.Marks_Obtained.all():
         if a in w.student.all():
           print(w)
           mark=w.mark
           s+=w.mark
           c+=1
           if(w.mark>=90):
               content+=f"{q.Name}  \t  {q.course_id}   \t   {w.mark}      \t   A     \tPass\n"
           elif(w.mark>=80):
               content+=f"{q.Name}  \t  {q.course_id}   \t   {w.mark}      \t   B     \tPass\n"
           elif(w.mark>=70):
               content+=f"{q.Name}  \t  {q.course_id}   \t   {w.mark}      \t   C     \tPass\n"
           elif(w.mark>=60):
               content+=f"{q.Name}  \t  {q.course_id}   \t   {w.mark}      \t   D    \tPass\n"
           elif(w.mark>=50):
               content+=f"{q.Name}  \t  {q.course_id}   \t   {w.mark}      \t   E    \tPass\n"
           else:
               content+=f"{q.Name}  \t  {q.course_id}   \t   {w.mark}      \t   F     \tFail\n"
    try:
        content+=f"Average Marks : {s/c}"  
    except:
        content+="Average Marks : 0"
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
def listdept(request,i):
    q=dept.objects.get(dept_id=i)
   
    return render(request,"College/batchlist.html",{'batch':q.batches.all()})
def department(request):
    avg=[]
    for a in dept.objects.all():
     q={'dept_id':a.dept_id,'name':a.name}
     tot=0
     count=0
     for l in a.batches.all(): 
        for b in l.courses.all():
            
            for c in b.Marks_Obtained.all():
                 tot+=c.mark
                 count+=1
     try:
         q['avg']=tot/count
     except:
         q['avg']=tot
     avg.append(q)
    return render(request,"College/listdept.html",{'dept':avg})
def createdept(request):
    if request.method == "POST":
       print(request.POST)
       n=dept(name= request.POST['Name'])
       n.dept_id=request.POST['ID']
       n.save()
       
   
       return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "College/createdept.html")
def courseperform(request,i):
    m=[]
    q=course.objects.get(course_id=i)
    for a in q.Marks_Obtained.all():
        m.append({'StudID':a.student.all()[0].StudID,'Name':a.student.all()[0].Name,'mark':a.mark})
    print(m)
    return  render(request, "College/performlist.html",{'mark':m})
def courselist(request):
    return render(request,"College/listcourse.html",{'course':course.objects.all()})
def chart(request,i):
    return render(request,"College/coursechart.html",{'i':i})
def coursechart(request,i):
    labels = ['A','B','C','D','E','F']
    data = [0,0,0,0,0,0]
    q=course.objects.get(course_id=i)
    queryset=[]
    for a in q.Marks_Obtained.all():
        data[labels.index(a.grade)]+=1
            
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
def unique(l):
    frequency = {}

# iterating over the list
    for item in l:
   # checking the element in dictionary
       if item in frequency:
      # incrementing the counr
          frequency[item] += 1
       else:
      # initializing the count
          frequency[item] = 1
    return frequency


def piechart(request):
    percent=[]
    for a in Students.objects.all():
        tot=0
        c=0
        for q in Marks.objects.filter(student=a):
            tot+=q.mark
            c+=1
        percent.append(tot/c)
    freq=unique(percent)
    a=[]
    b=[]
    for i in frequency.keys():
        a.append(i)
        b.append(frequency[i])
    return JsonResponse(data={
        'labels': a,
        'data': b,
    })
def percent(i):
    l=list()
    for a in batch.objects.get(batch_id=i).studs.all():
        b={'rollno':a.rollno,'Name':a.Name}
        tot=0
        c=0
        for q in Marks.objects.filter(student=a):
            tot+=q.mark
            c+=1
        b['avg']=tot/c
   
        l.append(b)
    return l

def pchart(request,i):
    q=percent(i)
    d=[]
    for a in q:
        d.append(a['avg'])
    l=unique(d)
    data=[]
    labels=[]
    for a in l.keys():
       labels.append(a)
       data.append(l[a])
    
    return render(request,"College/pie_chart.html",{'d':q,'data':data,'labels':labels})
def lchart(request,i):
    return  render(request, "College/deptchart.html",{'i':i})
def linechart(request,i):
    a= dept.objects.get(dept_id=i)
    q=[]
    labels=[]
    for c in a.batches.all():
        for a in c.studs.all():
            tot=0
            c=0
            mks=[]
            for d in Marks.objects.filter(student=a):
                tot+=d.mark
                c+=1
                mks.append(d.mark)
            q.append(tot/c)
      
    print(mks)
    print(labels)
    return JsonResponse(data={
        'labels': labels,
        'data': q,
    })
def demo_scatterchart(request):  
   data=[]
   legend=[]
   le=LabelEncoder()
  
   le.fit(list(a.name for a in batch.objects.all()))
   for a in batch.objects.all():
       legend.append([[a.name],le.transform([a.name])[0]])
   for a in course.objects.all():
       p=[]
       for b in batch.objects.filter(courses=a).all():
          
          for t in b.studs.all():
           for c in a.Marks_Obtained.filter(student=t).all():
               p.append({'x':c.mark,'y':le.transform([b.name])[0]})
          
       data.append([a.Name,p])
   print(data)
   
       
   return render(request,'College/scatter.html', {'data':data,'legend':legend})
def p(request):
    return render(request,"College/list2.html",{'stud':percent()})



    
            
            