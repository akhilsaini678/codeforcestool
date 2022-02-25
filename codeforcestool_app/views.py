from django.shortcuts import render
from django.core.mail import send_mail
import re 
import requests
import json


class contest_details():
    "Stores name and place pairs"
    def __init__(self, problem_name, rating,rating_percent):
        self.problem_name = problem_name
        self.rating = rating
        self.rating_percent = rating_percent


# Create your views here.
def index(request):
    contest_ID = request.POST.get('contest_ID')
    if contest_ID != None and contest_ID != '' and int(contest_ID)>=1 and int(contest_ID)<=1642:
        response=requests.get("https://flaskapitesting.herokuapp.com/api/"+contest_ID)
    else:
        response=requests.get("https://flaskapitesting.herokuapp.com/api/100")
    print(response.status_code)
    # print(response.json())
    ls = response.json()
    lists = []
    for attribute, value in ls.items():
        varr = value
        varr = int(float(varr))
        lists.append(contest_details(attribute,value, (varr)//40))
    context = {
         "problem_name" : ['A','B','C','D','E', 'F', 'G', 'H', 'I', 'J'],
    }
    contest_name = 'Contest ID : '
    if contest_ID != None and contest_ID != '' and int(contest_ID)>=1 and int(contest_ID)<=1642:
        contest_name+=str(contest_ID)
    else:
        contest_name+='100'
    return render(request,'index.html',{'contest_name':contest_name,'lists':lists})

def profile(request):
    sign=0
    user_name=request.POST.get('username')
    if user_name != None and user_name != '' :
        user_details=requests.get("https://codeforces.com/api/user.info?handles="+user_name)
        ls=user_details.json() 
        
        if ls['status'] == "OK" :
            sign=1
            ls_main = ls['result']
            dict_data=ls_main[0]



            user_rating=requests.get("https://codeforces.com/api/user.rating?handle="+user_name)
            ls=user_rating.json()
            ls_main = ls['result']
            total_contests = len(ls_main)

            best_rank=1000000
            worst_rank=0
            max_up=0
            max_down=0
            new=0
            old=0
            for i in ls_main:
                best_rank=min(best_rank,i['rank'])
                worst_rank=max(worst_rank,i['rank'])
                old=i['oldRating']
                new=i['newRating']
                if old >= new :
                    max_down=max(max_down,old-new)
                else:
                    max_up=max(max_up,new-old)

            list_contest_stat = []
            list_contest_stat.append(total_contests)
            list_contest_stat.append(best_rank)
            list_contest_stat.append(worst_rank)
            list_contest_stat.append(max_up)
            list_contest_stat.append(max_down)
    


            # Submissions Details
            user_submissions=requests.get("https://codeforces.com/api/user.status?handle="+user_name+"&from=1&count=10000")
            ls=user_submissions.json()
            ls_main = ls['result']
            total_submissions = len(ls_main)

            # Dictonaries 
            dict_lang = {}
            dict_verdict = {}
            dict_tags = {}
            dict_index = {}
            dict_qrating = {}

            # Looping through all submissions of a user
            for i in ls_main:
                dict_lang[i['programmingLanguage']] = dict_lang[i['programmingLanguage']]+1 if i['programmingLanguage'] in dict_lang else 1
                dict_verdict[i['verdict']] = dict_verdict[i['verdict']]+1 if i['verdict'] in dict_verdict else 1
                val=i['problem']['index']
                dict_index[val] = dict_index[val]+1 if val in dict_index else 1
                if 'rating' in i['problem']:
                    val=i['problem']['rating']
                    dict_qrating[val] = dict_qrating[val]+1 if val in dict_qrating else 1
                for j in i['problem']['tags']:
                    dict_tags[j] = dict_tags[j]+1 if j in dict_tags else 1  
    
            # print(dict_qrating)
            # print(dict_index)
            # print(dict_tags)
            # print(dict_lang)
            # print(dict_verdict)
            # print(total_submissions)
            # dict_data=ls_main[0]
            # print(ls_main)
            # print(dict_data)
            # print(dict_data['firstName']+' '+dict_data['lastName'])
            return render(request,'profile.html',{'sign':sign,'data':dict_data,'ls_contest':list_contest_stat,'total_sub':total_submissions,'languages_used':dict_lang,'sol_res':dict_verdict})
        else:
            sign=2
    return render(request,'profile.html',{'sign':sign})

def ourteam(request):
    return render(request,'ourteam.html',{})

def register(request):
    msg = ''
    if request.method == 'POST':
        first = request.POST.get('First')
        last = request.POST.get('Last')
        codechef_id = request.POST.get('Codechef_ID')
        gender = request.POST.get('Gender')
        email = request.POST.get('Email')
        phone_no = request.POST.get('Phone')
        year = request.POST.get('Year')
        branch = request.POST.get('Branch')
        myemail = 'akhilsainiwork@gmail.com'

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        else:
            message = 'Name : '+ first+' '+last +'\nEmail : '+email+'\nCodechef ID : '+codechef_id+'\nGender : '+gender+'\nEmail : '+email+'\nPhone No. : '+phone_no+'\nBranch : '+branch+'\nYear : '+year 
            send_mail('Message From Codeforces Tool : Registration',message,'',[myemail])
            msg = 'You have been successfully registered. Thank You.'
    return render(request,'register.html',{'msg':msg})

def contactus(request):

    msg = ''
    if request.method == 'POST':
        first = request.POST.get('First')
        last = request.POST.get('Last')
        email = request.POST.get('Email')
        message = request.POST.get('Message')
        myemail = 'akhilsainiwork@gmail.com'

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        else:
            message = 'Name : '+ first+' '+last +'\nEmail : '+email+'\nMessage : '+message
            send_mail('Message From Codeforces Tool : Suggestion',message,'',[myemail])
            msg = 'Your message have been sent successfully. Thank You.'

    return render(request,'contactus.html',{'msg':msg})



def iccc2020(request):
    return render(request,'iccc2020.html',{})
    
