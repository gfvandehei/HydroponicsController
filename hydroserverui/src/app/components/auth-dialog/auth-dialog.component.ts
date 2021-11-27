import { Component, OnInit } from '@angular/core';
import {MatDialogRef} from "@angular/material/dialog";
import { Router } from '@angular/router';
@Component({
  selector: 'app-auth-dialog',
  templateUrl: './auth-dialog.component.html',
  styleUrls: ['./auth-dialog.component.scss']
})
export class AuthDialogComponent implements OnInit {

  constructor(
    public dialogRef: MatDialogRef<AuthDialogComponent>,
    private router: Router
  ) { }

  ngOnInit(): void {
  }

  stayOnPage(){
    this.dialogRef.close(false);
  }

  returnToLogin(){
    this.dialogRef.close(true);
  }

}
