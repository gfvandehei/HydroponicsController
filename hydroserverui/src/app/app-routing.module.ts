import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SystemsTabGroupComponent } from './systems-tab-group/systems-tab-group.component';

const routes: Routes = [
  {
    path: "",
    component: SystemsTabGroupComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
