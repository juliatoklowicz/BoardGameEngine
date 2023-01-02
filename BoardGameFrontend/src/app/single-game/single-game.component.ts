import { Component, OnInit, Inject } from '@angular/core';
import { ThemePalette } from '@angular/material/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { switchMap } from 'rxjs';
import { DialogComponent } from '../dialog/dialog.component';
import { Game } from '../models/game';
import { AuthService } from '../services/auth.service';
import { GamesService } from '../services/games.service';

export interface GameItem { 
  img: string,
  title: string,
  state: boolean,
  rating: number, 
  label: string,
  players: string,
  age: string, 
  time: string,
  categories: Array<string>,
  description: string
}

interface Rating {
  value: number;
  max: number;
  color?: ThemePalette;
  disabled?: boolean;
  dense?: boolean;
  readonly?: boolean;
}

export interface DialogData {
  name: string;
  user_rating: string;
}

@Component({
  selector: 'app-single-game',
  templateUrl: './single-game.component.html',
  styleUrls: ['./single-game.component.scss']
})
export class SingleGameComponent implements OnInit {

  constructor(private router: Router, private gamesService: GamesService, private route: ActivatedRoute, 
    private auth: AuthService, public dialog: MatDialog) {
      this.router.routeReuseStrategy.shouldReuseRoute = function() {
        return false;
      };
     }

  id: number = 0;
  game: Game[] = [];
  name: string = "";
  user_rating: number = 0;
  user_current_rating: number = 0;
  user_id: any = sessionStorage.getItem('User_id');

  ngOnInit(): void {
    this.route.queryParams
      .subscribe(params => {
        this.id = params['game_id'];
      }
      );

      if (this.isLoggedIn()) {
        this.gamesService.getSingleGame(this.id, this.user_id).subscribe(data1=> {
          this.game = data1;
          this.name = this.game[0].name;
          this.gamesService.getReview(this.user_id, this.game[0].id).subscribe(data2 => {
             this.user_current_rating = data2[0].review_number;
          });
       });
      }
      else {
        this.gamesService.getSingleGame(this.id, 0).subscribe(data1=> {
          this.game = data1;
          this.name = this.game[0].name;
          // this.gamesService.getReview(this.user_id, this.game[0].id).subscribe(data2 => {
          //    this.user_current_rating = data2[0].review_number;
          // });
       });
      }

  }

  favClick() {
    if(this.game[0].is_favourite) {
      this.gamesService.removeFavourite(this.user_id, this.game[0].id).subscribe(data => {
        console.log(data);
        this.game[0].is_favourite = false;
      })
    }
    else {
      this.gamesService.addFavourite(this.user_id, this.game[0].id).subscribe(data => {
        console.log(data);
        this.game[0].is_favourite = true;
      })
    }
 }

  isLoggedIn() {
    return this.auth.checkUserStatus();
  }

  openDialog(): void {

     let dialogRef = this.dialog.open(DialogComponent, {
      width: '250px',
      data: {name: this.name, user_rating: this.user_rating}
     });

     dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.user_rating = result;
      if (this.user_current_rating == 0) {
        this.postReview();
      }
      else {
        this.putReview();
      }
     });
  }

  postReview() {
    this.gamesService.addReview(this.user_id, this.game[0].id, this.user_rating).subscribe(data => {
      console.log(data);
    })
    window.location.reload();
  }
 
  putReview() {
    this.gamesService.editReview(this.user_id, this.game[0].id, this.user_rating).subscribe(data => {
      console.log(data);
    })
    this.ngOnInit();
  }

}

