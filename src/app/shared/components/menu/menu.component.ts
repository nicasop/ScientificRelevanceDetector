import { Component, OnInit } from '@angular/core';
import {MenuItem} from 'primeng/api';

@Component({
  selector: 'shared-menu',
  templateUrl: './menu.component.html',
  styles: [
  ]
})
export class MenuComponent implements OnInit {

  constructor() { }

  public menuItems: MenuItem[] = [];

  ngOnInit() {
      this.menuItems = [
          {
              label: 'Home',
              icon : 'pi pi-home',
              style : { fontSize: '1.5em' },
              iconStyle: { fontSize: '1.3em' },
              routerLink:'/'
          },
          {
              label: 'Papers',
              icon: 'pi pi-database',
              style : { fontSize: '1.5em' },
              iconStyle: { fontSize: '1.3em' },
              routerLink:'papers'
          },
          {
            label: 'Heat Map',
            icon: 'pi pi-table',
            style : { fontSize: '1.5em' },
            iconStyle: { fontSize: '1.3em' },
            routerLink:'heatmap'
          },
          {
            label: 'MDS',
            icon: 'pi pi-chart-line',
            style : { fontSize: '1.5em' },
            iconStyle: { fontSize: '1.3em' },
            routerLink:'mds'
          },
          {
            label: 'Dendogram',
            icon: 'pi pi-sitemap',
            style : { fontSize: '1.5em' },
            iconStyle: { fontSize: '1.3em' },
            routerLink:'dendogram'
          },
          {
            label: 'Schedule',
            icon: 'pi pi-folder',
            style : { fontSize: '1.5em' },
            iconStyle: { fontSize: '1.3em' },
            routerLink:'schedule'
          },
      ];
  }
}
