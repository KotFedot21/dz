from redminelib import Redmine
import PySimpleGUI as sg
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta
from asyncio import tasks
plt.rcdefaults()
import numpy as np
from multiprocessing import Pool
URL='http://red.eltex.loc'
KEY='08c017a3b50e09357a72e4448cc1aa6f09271755'
redmine = Redmine(URL, key=KEY)




userlist = [
        69,
        1027,
        1125
    ]



'''69 - Алексей Глебко
1027 - Игорь Быков
1125 - Алена Новобранова'''

'''Статусы тикетов
New - 1
Re-opened - 8
In Progress - 2
Feedback - 13
Resolved - 3
Testing - 9
Closed - 5
Pending - 4
Wait Release - 10
'''
statuslist = [
    5
]

tasks=[]
matrix1=[]

def information_for_the_week():
    d=[]   ### для повторного использования
    current_date = date.today()## дата сегодня
    print(current_date)
    current_d = current_date.weekday()
    print(current_date.weekday())##номер дня, 0-понедельник
    num = current_date.weekday()
    monday_date = current_date - timedelta(days=num)##получаем дату понедельника
    print(monday_date)

    j=0

    current_date2=[]
    while j <= 4: # создает список из дат недели

        current_date1 = str(monday_date)
        current_date2.append(current_date1)
        monday_date = monday_date + timedelta(days=1)

        j+=1
    monday_date = current_date - timedelta(days=num)  ##получаем дату понедельника
    print (current_date2)
    return current_date2

def information_for_the_week2():
    d=[]   ### для повторного использования
    current_date = date.today()## дата сегодня
    print(current_date)
    current_d = current_date.weekday()
    print(current_date.weekday())##номер дня, 0-понедельник
    num = current_date.weekday()
    monday_date = current_date - timedelta(days=num)##получаем дату понедельника
    print(monday_date)
    i = 0

    current_date2=[]
    while i <= 4 : # создает список из дней недели для графика
        d.append(monday_date.day)
        monday_date = monday_date + timedelta(1)
        i += 1
        

    print(d)
    return d

def egjstgh(userid):
    
    
    for current_dateid in information_for_the_week() :

        th=[]
        ms = redmine.user.get(userid, include='memberships')
        prjc = 0
        
        for msp in ms.memberships:
            try:
            
                issues = redmine.issue.filter(project_id=msp.project.id, status_id=5,updated_on=current_dateid, cf_2=userid)

                
                for issue in issues:

                    print(redmine.user.get(userid).firstname, redmine.user.get(userid).lastname)
                    print('\tPROJECT NAME:', msp.project.name, 'ID:', msp.project.id)
                    print('\t\tНомер:', issue.id, 'Статус:', issue.status.name, 'Версия:', issue.fixed_version.name, 'Тема:', issue.subject)
                    th.append(issue.id)
                    
                th1 = list(set(th))
                
            except:
                print('\tPROJECT NAME:', msp.project.name, 'ID:', msp.project.id)
                print("Доступ к проекту запрещен")

            prjc=len(th1)
            
            

        matrix1.append(prjc)
        print(matrix1)
    #tasks.append(matrix1)
    return matrix1

def GetAllIssuesInAllProjects(redmine, userlist,tasks):

    

    agents = 3
    chunksize = 1
    with Pool(processes=agents) as pool:
        result = pool.map(egjstgh, userlist, chunksize)
        
    print(result)
    return result



def statistics_for_the_week():
    
    s=information_for_the_week2()
    h=GetAllIssuesInAllProjects(redmine, userlist,tasks)

    
    lin=['r','b','k']
    for hi, us, li in zip(h, userlist, lin):
            plt.plot(s, hi, li, label=redmine.user.get(us).firstname)
    #plt.figure(figsize=(10, 10))#в дюймах
    plt.xlim([0,29])
    plt.ylim([0, 9])
    plt.legend(fontsize=14)
    plt.show()

    
statistics_for_the_week()    
    
