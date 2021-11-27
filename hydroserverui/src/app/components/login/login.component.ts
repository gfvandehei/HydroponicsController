import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { UserService } from 'src/app/services/user.service';
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginFormData = {
    email: null,
    password: null
  }

  loginForm = new FormGroup({
    email: new FormControl(this.loginFormData.email, [
      Validators.required
    ]),
    password: new FormControl(this.loginFormData.password,[
      Validators.required,
      Validators.minLength(8)
    ])
  });

  constructor(
    private userService: UserService,
    private router: Router
  ) { }

  ngOnInit(): void {
  }

  get email() {return this.loginForm.get("email")}
  get password() {return this.loginForm.get('password')}

  login(){
    console.log(this.loginForm.value);
    if(this.loginForm.valid){
      //login with server
      this.userService.login(this.email?.value, this.password?.value).then((token) => {
        this.router.navigate(["home"]);
      }).catch((reason) => {
        console.log(reason);
        alert(reason);
      });
    } else{
      alert("Please fix mistakes and try again")
    }
    return false;
  }
}
