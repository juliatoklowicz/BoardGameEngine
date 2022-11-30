
from django.shortcuts import render

from rest_framework import viewsets
from .serializers import *
from .models import *

#from pickle import NONE
import BoardGamesAPI.models as table
import BoardGamesAPI.serializers as ser 
import BoardGamesAPI.scripts.populate_models as script

from django.contrib.auth.models import User
from django.db.models import Avg,Count
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
#'BoardGames/games/search/by_string'

from django.contrib.auth import authenticate, login, logout,get_user_model 
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models  import User

from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie

#TODO: przetestowac z postmanem
@csrf_exempt
def search_by_string(request):

    if request.method=='GET':
        parameters=request.GET
        #print(parameters)
        name_we_are_looking_for=parameters.__getitem__('name_string')
        print(name_we_are_looking_for)
        try:
            found_games=table.t_game.objects.filter(name__contains=name_we_are_looking_for).values()
        except table.t_game.DoesNotExist:
            return JsonResponse({"Massage":"game not found try different string"},
                                status=status.HTTP_404_NOT_FOUND)
        out_list = []
        for game in found_games:
            game_info_dict = game
            review = (table.t_review.objects
                    .values('game_id_id')
                    .annotate(avg_rank=Avg('review_number'))
                    .order_by('-avg_rank')).filter(game_id_id=game['id'])
            is_favourite = False
        
            if t_user_game.objects.filter(game_id=game['id'],
                                        user_id=request.user.id).exists():
                    is_favourite = True
            list_of_categories = []
            for j in t_game_genre.objects\
                            .filter(game_id_id=game["id"]).select_related().values():
                    list_of_categories.append(t_genre.objects.
                                            get(id=j['genre_id_id']).genre_name)
            game_info_dict['genres'] = list_of_categories
            if review.exists():
                game_info_dict['rank_value'] = round(review[0]['avg_rank'],2)
            else:
                game_info_dict['rank_value'] = 0.0
            
            game_info_dict['is_favourite'] = is_favourite
            out_list.append(game_info_dict)
        serializer=ser.t_gameSerializer(found_games, many=True)
        return JsonResponse(serializer.data, safe=False)

#User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#@csrf_exempt
#@login_required
def populateDataBase(request):
    script.run()

@csrf_exempt
@api_view(['GET'])
def getAllGames(request):
    args = request.GET
    try:
        game_id = args.__getitem__('game_id')
    except MultiValueDictKeyError:
        game_id = None

    if request.method == 'GET':
        if not t_game.objects.filter(id=game_id).exists():
            count_of_games_in_page = 10
            try:
                page_id = int(args.__getitem__('page_id'))
            except MultiValueDictKeyError:
                page_id = 1

            games_info = table.t_game.objects.filter(
                    id__gt=((page_id-1)*count_of_games_in_page),
                    id__lte=(page_id*count_of_games_in_page))

            output_list = []
            for game in games_info.values():
                
                review = (table.t_review.objects
                .values('game_id_id')
                .annotate(avg_rank=Avg('review_number'))
                .order_by('-avg_rank')).filter(game_id_id=game["id"])
                list_of_categories = []
                
                for j in t_game_genre.objects\
                            .filter(game_id_id=game["id"]).select_related().values():
                    list_of_categories.append(t_genre.objects.get(id=j['genre_id_id']).genre_name)

                is_favourite = False
                
                if t_user_game.objects.filter(game_id=game['id'],
                                        user_id=request.user.id).exists():
                    is_favourite = True

                game_info_dict = game
                if review.exists():
                    game_info_dict['rank_value'] = round(review[0]['avg_rank'],2)
                else:
                    game_info_dict['rank_value'] = 0.0
                game_info_dict['is_favourite'] = is_favourite
                game_info_dict['genres'] = list_of_categories
                output_list.append(game_info_dict)

            serializer = ser.t_gameSerializer(output_list,many=True)
            return JsonResponse(serializer.data,safe=False)

        else:
            game_info = table.t_game.objects.filter(id=game_id).values()
            review = (table.t_review.objects
                .values('game_id_id')
                .annotate(avg_rank=Avg('review_number'))
                .order_by('-avg_rank')).filter(game_id_id=game_id)

            list_of_categories = []
            for i in t_game_genre.objects.filter(game_id_id=game_id).select_related().values():
                list_of_categories.append(t_genre.objects.get(id=i['genre_id_id']).genre_name)

            is_favourite = False
            if t_user_game.objects.filter(game_id=game_id,
                                        user_id=request.user.id).exists():
                is_favourite = True

            game_info_dict = game_info[0]
            if review.exists():
                game_info_dict['rank_value'] = round(review[0]['avg_rank'],2)
            else:
                game_info_dict['rank_value'] = 0.0

            game_info_dict['is_favourite'] = is_favourite
            game_info_dict['genres'] = list_of_categories
            print(game_info_dict)

            serializer = ser.t_gameSerializer([game_info_dict],many=True)

            return JsonResponse(serializer.data,safe=False)

#def top10_using_serializer(request):
@csrf_exempt
@api_view(['GET'])
def top_10_games(request):
    if request.method == 'GET':
        result = (table.t_review.objects
                .values('game_id_id')
                .annotate(avg_rank=Avg('review_number'))
                .order_by('-avg_rank'))[:10]
        
        for i in result:
            i['name'] = table.t_game.objects.get(id=i['game_id_id']).name
            i['image_url'] = table.t_game.objects.get(id=i['game_id_id']).image_url
            
        serializer = ser.Top10Games(result,many=True)
        return JsonResponse(serializer.data,safe=False)

@csrf_exempt
@api_view(['GET'])
def get_games_review(request): 
    #All If Statements works correctly for GET method
    args = request.GET
    try:
        user_id1 = args.__getitem__('user')
    except MultiValueDictKeyError:
        user_id1=None
    try:
        game_id1 = args.__getitem__('game')
    except MultiValueDictKeyError:
        game_id1=None
        
    if request.method == 'GET':
        try:
            page_id = int(args.__getitem__('page_id'))
        except MultiValueDictKeyError:
            page_id = 1

        if all(item is not None for item in [user_id1,game_id1]):
            specific_review = table.t_review.objects.filter(user_id=user_id1,game_id=game_id1)
            serializer = ser.GamesReview(specific_review,many=True)
            return JsonResponse(serializer.data,safe=False)
        
        elif all(item is None for item in [user_id1,game_id1]):
            all_reviews = table.t_review.objects.all()
            serializer = ser.GamesReview(all_reviews,many=True)
            return JsonResponse(serializer.data,safe=False)

        elif user_id1 is None:
            specific_game = table.t_review.objects.filter(game_id=game_id1)
            serializer = ser.GamesReview(specific_game,many=True)
            return JsonResponse(serializer.data,safe=False)

        elif game_id1 is None:
            specific_user = table.t_review.objects.filter(user_id=user_id1)
            serializer = ser.GamesReview(specific_user,many=True)
            return JsonResponse(serializer.data,safe=False)

@csrf_exempt
@ensure_csrf_cookie
@api_view(['POST','DELETE','PUT'])
def add_del_edit_review(request):

    args = request.GET
    try:
        user_id1 = args.__getitem__('user')
    except MultiValueDictKeyError:
        return JsonResponse({"Message":"User need to be provided"})
    try:
        game_id1 = args.__getitem__('game')
    except MultiValueDictKeyError:
        return JsonResponse({"Message":"You need to give us a game"})


    if request.method == 'POST':
        user_added_review = table.t_review.objects.filter(user_id=user_id1,game_id=game_id1)
        if user_added_review.exists():
            return JsonResponse({"Massage":"You've added review for this game"},status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                game_score = args.__getitem__("game_score")            
            except MultiValueDictKeyError:
                return JsonResponse({"Massage":"You need to specify review score"},status=status.HTTP_404_NOT_FOUND)
            
            description = args.__getitem__("description")

            temp={'game_id_id':game_id1,'user_id_id':user_id1,
                    'review_number':game_score,'description':description}
            

            serializer = ser.GamesReview(data=temp)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"Massage":"Review was added"},status=status.HTTP_201_CREATED)
  
    elif request.method == 'PUT':
        user_added_review = table.t_review.objects.filter(user_id=user_id1,game_id=game_id1)
        if user_added_review.exists():
            try:
                review_description = args.__getitem__('description')
            except MultiValueDictKeyError:
                review_description = user_added_review.description
            
            try:
                review_score = args.__getitem__('game_score')
            except MultiValueDictKeyError:
                review_score = user_added_review.review_number
            
            temp={'game_id_id':game_id1,'user_id_id':user_id1,
                    'review_number':review_score,'description':review_description}

            serializer = ser.GamesReview(user_added_review.first(),data=temp)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({"Massage":"Review was edited"},status=status.HTTP_202_ACCEPTED)
            return JsonResponse({"Massage":"Review couldn't be edited"},status=status.HTTP_400_BAD_REQUEST)
    
        else:
            return JsonResponse({"Massage":"Unable to change review"},status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        try:
            review_info = table.t_review.objects.get(user_id=user_id1,game_id=game_id1)
        except table.t_review.DoesNotExist:
             return JsonResponse({"Massage":"You haven't Added Review for This Game"},status=status.HTTP_404_NOT_FOUND)

        review_info.delete()
        return JsonResponse({'Massage': 'Review was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@ensure_csrf_cookie
@api_view(['GET'])
def get_favourites(request):
    args = request.GET
    try:
        user_id = args.__getitem__('user')
    except MultiValueDictKeyError:
        return JsonResponse({"Message":"Something Went Wrong"},
                            status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        found_games=table.t_user_game.objects.filter(user_id=user_id).values()
        if found_games.exists():
            out_list = []
            for f_game in found_games:
                print(f_game)
                game_info_dict = table.t_game.objects.filter(id=f_game['game_id_id']).values()[0]
                review = (table.t_review.objects
                        .values('game_id_id')
                        .annotate(avg_rank=Avg('review_number'))
                        .order_by('-avg_rank')).filter(game_id_id=f_game['game_id_id'])
                list_of_categories = []
                for j in t_game_genre.objects\
                                .filter(game_id_id=f_game["game_id_id"]).select_related().values():
                        list_of_categories.append(t_genre.objects.
                                                get(id=j['genre_id_id']).genre_name)
                        
                game_info_dict['genres'] = list_of_categories
                if review.exists():
                    game_info_dict['rank_value'] = round(review[0]['avg_rank'],2)
                else:
                    game_info_dict['rank_value'] = 0.0
                
                game_info_dict['is_favourite'] = True
                out_list.append(game_info_dict)
                print(game_info_dict)
            serializer=ser.t_gameSerializer(out_list, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({"Message":"You don't haave any games in favourite"},
                            status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({"Message":"Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['POST'])
def add_to_favourites(request):
    args = request.GET
    try:
        game_name = args.__getitem__('game')
        user_id = args.__getitem__('user')

    except MultiValueDictKeyError:
        return JsonResponse({"Message":"Something Went Wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
    row = table.t_game.objects.filter(name=game_name).values()
    if row.exists() \
        and request.method == 'POST':
        game_info = row[0]
        row_in_table = table.t_user_game.objects.filter(game_id=game_info['id'],user_id=user_id)
        if row_in_table.exists():
            return JsonResponse({"Message":"Game already in your favorites"},
                                    status=status.HTTP_403_FORBIDDEN)
        else:
            row = {"user_id":user_id,"game_id":game_info['id']}
            serializer = ser.t_favourite_serializer(data=row)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"Message":"Game was added to your favourites"})

        return JsonResponse({"Message":"Something went wrong"},
                            status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"Message":"Only logged users can add games to favourites"},
                        status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def remove_from_favourites(request):
    args = request.GET
    try:
        game_name = args.__getitem__('game')
        user_id = args.__getitem__('user')
    except MultiValueDictKeyError:
        return JsonResponse({"Message":"Something Went Wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
    row = table.t_game.objects.filter(name=game_name).values()
    
    if row.exists() \
        and request.method == 'DELETE':
        game_info = row[0]
        row_in_table = t_user_game.objects.filter(game_id=game_info['id'],user_id=user_id)
        if row_in_table.exists():
            row_in_table.delete()
            return JsonResponse({'Massage': 'Game was deleted from favourites successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({"Message":"Unable to remove game"},
                                    status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"Message":"Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST','GET'])
def login_view2(request):
    args = request.GET
    username = args.__getitem__('username')
    password = args.__getitem__('password')
    if request.method == "GET":
        serializer = AuthTokenSerializer(data={'username':username,'password':password})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request,user)
            response={"message":"user is logged",
                "userToken":str(Token.objects.get(user=user)),
                "user_id":user.id,
                "username":user.username,
                "email":user.email}

            return JsonResponse(response,safe=False)
        else:
            return JsonResponse({"Message":"Something Went Wrong"},safe=False, status=status.HTTP_400_BAD_REQUEST)

        

@api_view(['GET','PUT','DELETE','UPDATE'])
@csrf_exempt
def logout_view2(request):
    logout(request)
    response={"sucess":True}
    return JsonResponse(response,safe=False)

def check_user_status(request):
    if request.user.is_authenticated:
        return JsonResponse({"user":"user is logged in"})
    else:
        return JsonResponse({"user":"User is not logged in"})

    
@api_view(['GET'])
def register_user2(request):
    args = request.GET
    try:
        username = args.__getitem__('username')
        mail = args.__getitem__('email')
        password = args.__getitem__('password')
    except MultiValueDictKeyError:
        return JsonResponse({"Massage":"Bad Request"},
                        status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        #User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        if User.objects.filter(username=username).exists():
            return JsonResponse({"Massage":"Username is taken"},
                            status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=mail).exists():
            return JsonResponse({"Massage":"Email is taken"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            user_data = {'username':username,'email':mail,'password':password}
        
        register = register_serializer(data=user_data)
        if register.is_valid(raise_exception=True):
            user = register.save()
            return JsonResponse({"user":user_serializer(user).data,
                                "token": str(Token.objects.create(user=user))},
                                status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"Message":"Something Went Wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
       

"""
def top10(requst):
    jsone = []
    iter = 0
    result = (table.t_review.objects
                .values('game_id_id')
                .annotate(avg_rank=Avg('review_number'))
                .order_by('-avg_rank'))
    
    for i in result:
        query = table.t_game.objects.filter(id=i['game_id_id']).first()
        output = {"game_name":query.name,"game_reviews":round(i['avg_rank'],2),"image":query.image_url}
        jsone.append(output)


    return JsonResponse(jsone,safe=False)
"""
'''def getAllGames(request):
    jsone = {}
    j = 0
    for row in table.t_genre.objects.all():
        jsone[j] = row.genre_name
        j += 1
    return JsonResponse(jsone)'''
"""
@csrf_exempt
@api_view(['PUT','GET'])
def register_user(request):
    args = request.GET
    try:
        username = args.__getitem__('Username')
        mail = args.__getitem__('Mail')
        password = args.__getitem__('Password')
    except MultiValueDictKeyError:
        return JsonResponse({"Massage":"Bad Request"},status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        if User.objects.filter(Username=username).exists():
            return JsonResponse({"Massage":"Username is taken"},status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(Mail=mail).exists():
            return JsonResponse({"Massage":"Email is taken"},status=status.HTTP_400_BAD_REQUEST)
        else:
            user_data = {'Username':username,'Mail':mail,'Password':password}
            
        User.objects.create_user(username, mail, password)
        #if serializer.is_valid():
        #    serializer.save()
        return JsonResponse({"Massage":"User Was Added"},status=status.HTTP_201_CREATED)"""
'''class t_game_view(ModelViewSet):#viewsets.ViewSet
    serializer_class = t_gameSerializer
    queryset = t_game.objects.all()'''
"""
class t_user_view(viewsets.ModelViewSet):
    serializer_class = t_user_Serializer
    queryset = t_user.objects.all()
"""