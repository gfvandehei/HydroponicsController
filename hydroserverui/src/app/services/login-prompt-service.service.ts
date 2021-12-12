import { Injectable, EventEmitter } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AuthDialogComponent } from '../components/auth-dialog/auth-dialog.component';

@Injectable({
  providedIn: 'root'
})
export class LoginPromptServiceService {
  loginPromptDisplayed = false;
  loginPromtEvent = new EventEmitter();

  constructor(
    private dialog: MatDialog,
    private router: Router
  ) { }

  displayLogin(){
    if(!this.loginPromptDisplayed){
      this.loginPromptDisplayed = true;
      this.dialog.open(AuthDialogComponent).afterClosed().subscribe((toLogin: boolean) => {
        console.log(toLogin);
        if(toLogin){
          this.router.navigate(['login']);
        }
      })
      this.loginPromtEvent.emit("loginEvent");
    }
  }
}
