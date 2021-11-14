import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SystemViewComponent } from './system-view/system-view.component';
import { StoreModule } from '@ngrx/store';
import { ServoCardComponent } from './servo-card/servo-card.component';
import { SystemsTabGroupComponent } from './systems-tab-group/systems-tab-group.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatTab, MatTabsModule} from "@angular/material/tabs";
import { HttpClientModule } from '@angular/common/http';
import { DhtCardComponent } from './dht-card/dht-card.component';
import { MatIcon, MatIconModule} from "@angular/material/icon";
import { PumpCardComponent } from './pump-card/pump-card.component';
@NgModule({
  declarations: [
    AppComponent,
    SystemViewComponent,
    ServoCardComponent,
    SystemsTabGroupComponent,
    DhtCardComponent,
    PumpCardComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    StoreModule.forRoot({}, {}),
    BrowserAnimationsModule,
    MatTabsModule,
    HttpClientModule,
    MatIconModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
