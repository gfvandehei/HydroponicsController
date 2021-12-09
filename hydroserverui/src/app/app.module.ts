import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SystemViewComponent } from './pages/system-view/system-view.component';
import { StoreModule } from '@ngrx/store';
import { ServoCardComponent } from './servo-card/servo-card.component';
//import { SystemsTabGroupComponent } from './systems-tab-group/systems-tab-group.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {MatTab, MatTabsModule} from "@angular/material/tabs";
import {MatInputModule} from "@angular/material/input";
import {MatButtonModule} from "@angular/material/button";
import { MatFormFieldModule } from '@angular/material/form-field';
import {MatMenu, MatMenuModule} from "@angular/material/menu";

import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { DhtCardComponent } from './components/dht-card/dht-card.component';
import { MatIcon, MatIconModule} from "@angular/material/icon";
import { PumpCardComponent } from './pump-card/pump-card.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterFormComponent } from './components/register-form/register-form.component';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { RegisterPageComponent } from './pages/register-page/register-page.component';
import { SystemsHomeComponent } from './pages/systems-home/systems-home.component';
import {AuthInterceptorInterceptor} from "src/app/interceptors/auth-interceptor.interceptor";
import { SystemInformationCardComponent } from './components/system-information-card/system-information-card.component';
import { SystemCameraComponent } from './pages/system-view/system-camera/system-camera.component';
import { AuthDialogComponent } from './components/auth-dialog/auth-dialog.component';
import { MatDialogModule } from '@angular/material/dialog';
import { SystemSensorsComponent } from './pages/system-view/system-sensors/system-sensors.component';
import { DualCircleGraphComponent } from './components/dual-circle-graph/dual-circle-graph.component';
import { SystemAutomationComponent } from './pages/system-view/system-automation/system-automation.component';
import { PumpInfoCardComponent } from './components/pump-info-card/pump-info-card.component';
import { PumpScheduleDisplayComponent } from './components/pump-schedule-display/pump-schedule-display.component';
import { NewTimeDialogComponent } from './components/pump-schedule-display/new-time-dialog/new-time-dialog.component';

@NgModule({
  declarations: [
    AppComponent,
    SystemViewComponent,
    ServoCardComponent,
    //SystemsTabGroupComponent,
    DhtCardComponent,
    PumpCardComponent,
    LoginComponent,
    RegisterFormComponent,
    LoginPageComponent,
    RegisterPageComponent,
    SystemsHomeComponent,
    SystemInformationCardComponent,
    SystemCameraComponent,
    AuthDialogComponent,
    SystemSensorsComponent,
    DualCircleGraphComponent,
    SystemAutomationComponent,
    PumpInfoCardComponent,
    PumpScheduleDisplayComponent,
    NewTimeDialogComponent
  ],
  imports: [
    BrowserModule,
    //RouterModule,
    AppRoutingModule,
    StoreModule.forRoot({}, {}),
    BrowserAnimationsModule,
    MatTabsModule,
    HttpClientModule,
    MatIconModule,
    MatInputModule,
    MatButtonModule,
    MatFormFieldModule,
    FormsModule,
    ReactiveFormsModule,
    MatMenuModule,
    MatDialogModule
  ],
  providers: [
    {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptorInterceptor, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
