import { NgModule } from '@angular/core';
import { Router, RouterModule, Routes } from '@angular/router';
//import { SystemsTabGroupComponent } from './systems-tab-group/systems-tab-group.component';
import {LoginComponent} from "./components/login/login.component";
import { RegisterFormComponent } from './components/register-form/register-form.component';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { RegisterPageComponent } from './pages/register-page/register-page.component';
import { SystemsHomeComponent } from './pages/systems-home/systems-home.component';
import { SystemViewComponent } from './pages/system-view/system-view.component';
import { SystemCameraComponent } from './pages/system-view/system-camera/system-camera.component';
import { SystemSensorsComponent } from './pages/system-view/system-sensors/system-sensors.component';
import { SystemAutomationComponent } from './pages/system-view/system-automation/system-automation.component';

const routes: Routes = [
  {
    path: "login",
    component: LoginPageComponent
  },
  {
    path: "register",
    component: RegisterPageComponent
  },
  {
    path: "home",
    component: SystemsHomeComponent
  },
  {
    path: "system/:systemId",
    component: SystemViewComponent,
    children: [
      {path: 'camera/:cameraId', component: SystemCameraComponent},
      {path: 'sensor', component: SystemSensorsComponent},
      {path: "automation", component: SystemAutomationComponent}
    ]
  }
];

@NgModule({
  imports: [
    //RouterModule,
    RouterModule.forRoot(routes),
    //RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
