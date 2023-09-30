import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { PapersPageComponent } from './pages/papers-page/papers-page.component';
import { HeatmapPageComponent } from './pages/heatmap-page/heatmap-page.component';
import { MdsPageComponent } from './pages/mds-page/mds-page.component';
import { DendogramPageComponent } from './pages/dendogram-page/dendogram-page.component';
import { SchedulePageComponent } from './pages/schedule-page/schedule-page.component';

const routes: Routes = [
  {
    path : '',
    component : HomePageComponent
  },
  {
    path : 'papers',
    component : PapersPageComponent
  },
  {
    path : 'heatmap',
    component : HeatmapPageComponent
  },
  {
    path : 'mds',
    component : MdsPageComponent
  },
  {
    path : 'dendogram',
    component : DendogramPageComponent
  },
  {
    path : 'schedule',
    component : SchedulePageComponent
  },
  {
    path : '**',
    redirectTo : ''
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PublicRoutingModule { }
