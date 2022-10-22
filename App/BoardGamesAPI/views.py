from pickle import NONE
import BoardGamesAPI.models as table
import BoardGamesAPI.serializers as serializers
import BoardGamesAPI.scripts.populate_models as script

from django.db.models import Avg
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 


# Create your views here.
#'BoardGames/games/search/by_string'
#TODO: przetestowac z postmanem
def search_by_string(request):

    if request.method=='GET':
        parameters=request.GET()
        name_we_are_looking_for=parameters.__getitem__('name_string')
        found_games=table.t_game.objects.filter(name__contains=name_we_are_looking_for).values()
        serializer=serializers.t_gameSerializer(found_games, many=True)
        return JsonResponse(serializer.data, safe=False)



def populateDataBase(request):
    script.run()

# wyswietl wszytskie gry 
def getAllGames(request):
    jsone = {}
    j = 0
    for row in table.t_genre.objects.all():
        jsone[j] = row.genre_name
        j += 1
    return JsonResponse(jsone)


#http://127.0.0.1:8000/BoardGamesAPI/games/top_10_games

#def top10_using_serializer(request):
@api_view(['GET'])
def top_10_games(request):
    if request.method == 'GET':
        result = (table.t_review.objects
                .values('game_id_id',)
                .annotate(avg_rank=Avg('review_number'))
                .order_by('-avg_rank'))
        print(result)
        serializer = serializers.GamesReview(result,many=True)
        #return Response(serializer.data)
        return JsonResponse(serializer.data,safe=False)

@api_view(['GET','PUT','DELETE','UPDATE'])
def games_review(request): 
    args = request.args
    user_id1 = args.get('user')
    game_id1 = args.get('game')
    if request.method == 'GET':
        if user_id1 is None:
            specific_game = table.t_review.objects.filter(user_id=user_id1)
            serializer = serializers.GamesReview(specific_game,many=True)
            return JsonResponse(serializer.data,safe=False)

        elif game_id1 is None:
            specific_game = table.t_review.objects.filter(game_id=game_id1)
            serializer = serializers.GamesReview(specific_game,many=True)
            return JsonResponse(serializer.data,safe=False)

        elif None not in (user_id1,game_id1):
            specific_review = table.t_review.objects.filter(user_id=user_id1,game_id=game_id1)
            serializer = serializers(specific_review)
            return JsonResponse(serializer.data,safe=False)
        else:
            all_reviews = table.t_review.objects.all()
            serializer = serializers.GamesReview(all_reviews,many=True)
            return JsonResponse(serializer.data,safe=False)
    
    elif request.method == 'PUT':
        try:
            user_info = table.t_user.objects.get(id=user_id1)
        except table.t_user.DoesNotExist:
            return JsonResponse({"Massage":"Only Users With Account \
                                        Can Add Reviews"},status=status.HTTP_404_NOT_FOUND)
        try:
            game_info = table.t_game.objects.get(id=game_id1)
        except table.t_game.DoesNotExist:
            return JsonResponse({"Massage":"Game Does Not Exist In Our Database"},status=status.HTTP_404_NOT_FOUND)
        
        review_data = JSONParser().parse(request)
        serializer = serializers.GamesReview(data=review_data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            user_info = table.t_user.objects.get(id=user_id1)
        except table.t_user.DoesNotExist:
            return JsonResponse({"Massage":"Only Users With Account \
                                        Can Delete Reviews"},status=status.HTTP_404_NOT_FOUND)
        try:
            review_info = table.t_review.objects.get(user_id=user_info.id,game_id=game_id1)
        except table.t_review.DoesNotExist:
             return JsonResponse({"Massage":"You haven't Added Review for This Game"},status=status.HTTP_404_NOT_FOUND)

        review_info.delete()
        return JsonResponse({'Massage': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


            
        
    
"""
def top10(request):
    postgre_connection = postgre.connect(database=environ.get('POSTGRES_NAME'), 
                                    user=environ.get('POSTGRES_USER'),
                                    password=environ.get('POSTGRES_PASSWORD'), 
                                    host=environ.get('POSTGRES_HOST'), port='5432')
    postgre_cur = postgre_connection.cursor()
    postgre_cur.execute(""""""
        select game.name,Round(coalesce(avg(review.review_number),0),2) as avg_review 
        from "BoardGamesAPI_t_game" as game left join "BoardGamesAPI_t_review" as review on game.id = review.game_id_id
        group by game.name order by avg_review desc)""""""

    jsone = {}
    for iter,row in postgre_cur.fetchmany(10):
        print(row)
        jsone[iter] = row
    
    return JsonResponse(jsone)

    def getAllGames(request):
    # stri="hello world. You are at the polls index"+str(request)
   # return JsonResponse({"R-Va":"Slawek"})

    
    postgre_connection = postgre.connect(database=environ.get('POSTGRES_NAME'), 
                                        user=environ.get('POSTGRES_USER'),
                                        password=environ.get('POSTGRES_PASSWORD'), 
                                        host=environ.get('POSTGRES_HOST'), port='5432')

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
"""

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