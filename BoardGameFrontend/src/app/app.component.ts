import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  
  constructor(private router: Router) {}

  goToFavorites() {
    this.router.navigate(['/', 'favorites']);
  }

  goToMyAccount() {
    this.router.navigate(['/', 'myAccount']);
  }

  goToHome() {
    this.router.navigate(['/', 'home']);
  }

  goToLogin() {
    this.router.navigate(['/', 'login']);
  }

  goToRegister() {
    this.router.navigate(['/', 'register']);
  }
}