from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import psycopg2 as postgre



# Create your views here.

# wyswietl wszytskie gry
def getAllGames(request):
    # stri="hello world. You are at the polls index"+str(request)
    postgre_connection = postgre.connect(database='djangoCourseDB', user='postgres',
                                         password='admin', host='127.0.0.1', port='5432')
    postgr_cur = postgre_connection.cursor()
    postgr_cur.execute('select * from t_game where id < 50')
    jsone = {}
    j = 0
    for i in postgr_cur.fetchall():
        print(i)
        jsone[j] = i
        j += 1
    # jsone={"wszystkie":"gry"}
    return JsonResponse(jsone)  # HttpResponse(stri)

def testing():
    pass
