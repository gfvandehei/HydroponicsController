import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-new-time-dialog',
  templateUrl: './new-time-dialog.component.html',
  styleUrls: ['./new-time-dialog.component.scss']
})
export class NewTimeDialogComponent implements OnInit {
  newTime: string = "12:00";

  constructor(
    public dialogRef: MatDialogRef<NewTimeDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) { }

  ngOnInit(): void {
  }

  onCancel(): void{
    this.dialogRef.close(null);
  }

  onSubmit(): void{
    this.dialogRef.close(this.newTime);
  }

}
