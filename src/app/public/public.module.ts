import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

import { PublicRoutingModule } from './public-routing.module';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { PapersPageComponent } from './pages/papers-page/papers-page.component';
import { HeatmapPageComponent } from './pages/heatmap-page/heatmap-page.component';
import { PrimeNgModule } from '../prime-ng/prime-ng.module';
import { MdsPageComponent } from './pages/mds-page/mds-page.component';
import { DendogramPageComponent } from './pages/dendogram-page/dendogram-page.component';
import { SchedulePageComponent } from './pages/schedule-page/schedule-page.component';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { NgApexchartsModule } from 'ng-apexcharts';


@NgModule({
  declarations: [
    HomePageComponent,
    PapersPageComponent,
    HeatmapPageComponent,
    MdsPageComponent,
    DendogramPageComponent,
    SchedulePageComponent
  ],
  imports: [
    CommonModule,
    PublicRoutingModule,
    PrimeNgModule,
    ReactiveFormsModule,
    FormsModule,
    NgApexchartsModule,
    HttpClientModule,
  ]
})
export class PublicModule { }
