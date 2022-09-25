from tkinter import CASCADE
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.utils.translation import gettext_lazy as _


# Create your models here.

class t_user(models.Model):
    id = models.BigAutoField(primary_key=True)
    Username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    Mail = models.CharField(max_length=100, unique=True, null=False, blank=False)
    Password = models.CharField(max_length=50, null=False, blank=False)


class t_friend_list(models.Model):
    user1_id = models.ForeignKey(t_user, on_delete=models.CASCADE),
    user2_Id = models.ForeignKey(t_user, on_delete=models.CASCADE),
    Last_Seen = models.DateField(auto_now=True)
    class Meta:
        #unique_together = ['user1_id', 'user2_id']
        constraints = [
            # Ensures constraint on DB level, raises IntegrityError (500 on debug=False)
            models.CheckConstraint(check=Q(F('user1_id') != F('user2_id')), name='check_same_user_IDs',),
            models.UniqueConstraint(fields=['user1_id', 'user2_Id'], name="cant be your own friend")
        ]



    # class Meta:
    #    constraints = (
    #        ("check_name", Check(proj_name__like!=User_Id)))

    # def clean(self): chyba nie jest potrzebne
    #    # Ensures constraint on model level, raises ValidationError
    #    if self.User_Id == self.User2_Id:
    #        # raise error for field
    #        raise ValidationError({'same_ID2': _('user cannot be his own friend.')})


class t_user_activity:
    User_Id = models.ForeignKey(t_user, on_delete=models.CASCADE),
    Activity_Type = models.CharField(max_length=30, unique=True, null=False, blank=False),
    Activity_Timestamp = models.DateTimeField(),

    def clean(self):
        # Ensures constraint on model level, raises ValidationError
        if self.User_Id == self.User2_Id:
            # raise error for field
            raise ValidationError({'same_ID2': _('user cannot be his own friend.')})

    '''
    Constraint fk_user1 FOREIGN KEY(User_Id) References t_user(Id),
    Constraint fk_user2 FOREIGN KEY(User2_Id) References t_user(Id),
    Constraint different_User_Id check (User_Id <> User2_Id),
    Unique (User_Id,User2_Id)
    '''


# TODO: t_games, t_genre, t_game_genre, t_review,

class t_genre(models.Model):
    id = models.BigAutoField(primary_key=True)
    genre_name = models.CharField(max_length=255,
                                  unique=True,
                                  null=False,
                                  blank=False)


class t_game(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255,
                            unique=True,
                            null=False,
                            blank=False)

    min_player = models.PositiveSmallIntegerField(default=2,
                                                  validators=[
                                                      MinValueValidator(1)
                                                  ])

    max_player = models.PositiveSmallIntegerField(default=4,
                                                  validators=[
                                                      MaxValueValidator(15),
                                                  ])

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(min_player__lt=F('max_player')),
                name='min_player_lower_than_max')
        ]


class t_game_denre(models.Model):
    gamd_id = models.ForeignKey(t_game,
                                on_delete=models.CASCADE)
    genre_id = models.ForeignKey(t_genre,
                                 on_delete=models.CASCADE)


class t_review(models.Model):
    game_id = models.ForeignKey(t_game,
                                on_delete=models.CASCADE)

    user_id = models.ForeignKey(t_user,
                                on_delete=models.CASCADE)

    review_number = models.DecimalField(
        null=False,
        blank=False,
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ])

    description = models.TextField(max_length=1000)


class t_user_game(models.Model):
    user_id = models.ForeignKey(t_user,
                                on_delete=models.CASCADE)

    game_id = models.ForeignKey(t_game,
                                on_delete=models.CASCADE)


