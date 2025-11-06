from django.shortcuts import render
from django.http import  HttpResponse
from .models import Question,userData,Result
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import userDataSerializers

# Create your views here.
next =-1

                   # rest api part 


@api_view(['GET'])
def sendData(request):
    return HttpResponse("{'s.no': 1,'name':'jamal'}")


@api_view(['GET'])
def getUser(request, uname):
    try:
        userdb = userData.objects.get(username=uname)
        response = Response({
            'username': userdb.username,
            'password': userdb.password,
            'phno': userdb.phno
        })
        return response
    except userData.DoesNotExist:
        return Response({"error": "User not found"})
    
@api_view(['GET'])
def getUserDetails(request,uname):
    try:
        userdb = userData.objects.get(username = uname)
        response = Response({
            'username':userdb.username,
            'password': userdb.password,
            'phno': userdb.phno
                
        })
        
        return response
    except userData.DoesNotExist:
        return Response({'error':"user not found"})
    
@api_view(['GET'])
def getUserDetails2(request,uname):
    try:
        userdb = userData.objects.get(username = uname)
        usersr = userDataSerializers(userdb)
        response = Response(usersr.data)
        return response
    except userData.DoesNotExist:
        return Response({'error':"user not found"})  
    
    
    
    
@api_view(['POST'])
def addUser(request):
    userobj = request.data
    userData.objects.create(username = userobj['username'],password = userobj['password'],phno = userobj["phno"])
    # response= Response("data inserted")
    response = Response(userobj)
    
    return response


@api_view(['PUT'])
def updateUSer(request):
    userobj = request.data # jo data pahle se tha usko uthaya 
    userdb = userData.objects.get(username = userobj['username'])  
    userdb.password = userobj['password']
    userdb.phno = userobj['phno']
    userdb.save()  
    # Response = Response(userobj)
    
    return Response('updated succesful')



@api_view(['DELETE'])
def deleteUser(request,uname):
    userobj = userData.objects.filter(username = uname)
    userobj.delete()
    
    return Response("Data deleted")



@api_view(['GET'])
def getAllUser(request):
    userdb = userData.objects.all().values()
    return Response(list(userdb))
    
    
    
    
    
    
    
    




def homepage(request):
    return render(request,'home.html')

def registerationform(request):
    return render(request,'registeration.html')

def registeration(request):
    uname = request.GET.get('username')
    pswd = request.GET.get('password')
    phno = request.GET.get('phoneno')
    userdb = userData.objects.create(username = uname,password = pswd,phno = phno)
    
    return render(request,'login.html')

def loginform(request):
    return render(request,"login.html")

def login(request):
    uname = request.GET.get('username')
    pswd = request.GET.get('password')
    request.session['usrname']= uname
    
    
    try:
        userdb =userData.objects.get(username = uname)
    
    except Exception as e:
        return render(request,'login.html',{'message':'wrong username '})
    
    if userdb.password == pswd:
        request.session['answer']= {}
        request.session['score']= 0
        request.session['qno'] = 0
        # querylist= Question.objects.filter(subject  = 'maths').values()
        # listOfQuestions= list(querylist)
        # request.session['listOfQuestions'] =  listOfQuestions
        return render(request,'subject.html',{'message': 'you have succesfully login ' +  uname })
    else:
        return render(request,'login.html',{'message' :'wrong password ' })
    


def showForm(request):
    return render(request,'questions.html')

def viewquestions(request):
    qno = request.GET.get('qno')
    try :
        userobj = Question.objects.get(qno = qno )
        
    except Exception as e:
        return render (request,'questions.html',{'message': 'question not found  '})
    
    
    return render(request,'questions.html',{'userobj': userobj})

    


def addquestions(request):
    qno = request.GET.get('qno')
    qtx = request.GET.get('qtext')
    ans=request.GET['answer']
    op1=request.GET['op1']
    op2=request.GET['op2']
    op3=request.GET['op3']
    op4=request.GET['op4']
    subject=request.GET['subject']
    Question.objects.create(qno = qno,qtext = qtx,answer = ans ,op1 = op1,op2= op2,op3= op3,op4 = op4,subject = subject)
    return render(request,'questions.html',{'message': 'questions added successfully'})


def updatequestion(request):
    qno = request.GET.get('qno')
    qtx = request.GET.get('qtext')
    ans=request.GET['answer']
    op1=request.GET['op1']
    op2=request.GET['op2']
    op3=request.GET['op3']
    op4=request.GET['op4']
    subject=request.GET['subject']
    
    userobj = Question.objects.filter(qno = qno,subject = subject)
    userobj.update(qno = qno,qtext = qtx,answer = ans ,op1 = op1,op2= op2,op3= op3,op4 = op4,subject = subject)
    
    return render(request,'questions.html',{'message': 'question updated '})


def deletequestion(request):
    qno = request.GET.get('qno')
    
    Question.objects.filter(qno = qno).delete()
    
    return render(request,'questions.html',{'message': 'question delete successfully '})

  
  
def nextQuestion(request):
        allquestions=request.session['listofquestions']
        questionindex=request.session['qno']
        if 'op' in request.GET:
            allanswers=request.session['answer']
            allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        #allanswer[1]=[1,2+2,4,6]
        #{1:[1,2+2,4,6],2:[2,9-4,5,2]}

        if (questionindex<len(allquestions) - 1):
            request.session['qno']=request.session['qno']+1
            quesstion=allquestions[request.session['qno']]
        else:
            return render(request,'questionnavigation.html',{'message':'Click on previous or end test'})
        return render(request,'questionnavigation.html',{'question':quesstion})
    
    
    

def previousQuestion(request):
    allquestions=request.session['listofquestions']
    questionindex=request.session['qno']

    if 'op' in request.GET:
        allanswers=request.session['answer']
        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        #allanswer[1]=[1,2+2,4,6]
        #{1:[1,2+2,4,6],2:[2,9-4,5,2]}

    if (questionindex>0):
        request.session['qno']=request.session['qno']-1
        quesstion=allquestions[request.session['qno']]
    else:
        return render(request,'questionnavigation.html',{'message':'Click on Next or end test'})
    return render(request,'questionnavigation.html',{'question':quesstion})
    
    
def startTest(request):
    subj = request.GET.get('subject')
    quesrySet= Question.objects.filter(subject  = subj ).values()
    listofquestions = list(quesrySet)
    request.session['listofquestions'] = listofquestions
    request.session['subject']=request.GET['subject']
    
    return render(request,'questionnavigation.html',{'question': listofquestions[0]})



def endExam(request):
    if 'op' in request.GET:
        allanswers=request.session['answer']
        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        #allanswer[1]=[1,2+2,4,6]
        #{1:[1,2+2,4,6],2:[2,9-4,5,2]}

    responses=request.session['answer']
    allresponses=responses.values()

    for i in allresponses:
        print(f'The correct answer is {i[2]} and the given answer is {i[3]}')
        if i[2]==i[3]:
            request.session['score']=request.session['score']+1

        finalscore=request.session['score']
    try:
        Result.objects.create(username=request.session['usrname'],subject=request.session['subject'],marks=request.session['score'])
        return render(request,'score.html',{'finalscore':finalscore,'responses':allresponses})
    except:
        return render(request,'login.html',{'message':'Login throught different'})
    
@api_view(['GET'])
def getUser(request,uname):
    userdb = userData.objects.get(username = uname)
    response = Response({'username'  : userdb.username,'password': userdb.password,'phnono': userdb.phno})
    return response
