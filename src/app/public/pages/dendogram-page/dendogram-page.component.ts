import { Component, OnInit, NgZone, PLATFORM_ID, Inject  } from '@angular/core';
import { Message, MessageService } from 'primeng/api';
import { PrimeNGConfig } from 'primeng/api'

import { Graph } from '../../Interfaces/graph';
import { GraphServiceService } from '../../Services/graph-service.service';

// amCharts imports
import * as am5 from '@amcharts/amcharts5';
import * as am5hierarchy from "@amcharts/amcharts5/hierarchy";
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated';


@Component({
  selector: 'app-dendogram-page',
  templateUrl: './dendogram-page.component.html',
  styleUrls: ['./dendogram-page.component.css'],
  providers: [MessageService]
})
export class DendogramPageComponent implements OnInit {

  msgPapers: Message[] = [];
  graph: Graph = {
    value: 0,
    name: "",
    children: []
  }

  constructor(
    private graph_service: GraphServiceService, 
    private primengConfig: PrimeNGConfig,
    private messageService: MessageService,
    @Inject(PLATFORM_ID) private platformId: Object, 
    private zone: NgZone
  ) { 
    const data = localStorage.getItem('matrix');
    this.graph_service.getGraph(data).subscribe({
      next: res => {
        this.graph = res;
        this.drawHierarchy(this.graph)
      },
      error: err => {
        console.log(err);
      }
    })
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    console.log('init');
  }

  ngAfterViewInit(){}

  drawHierarchy(data:Graph){
    let root = am5.Root.new("chartdiv");

    // Set themes
    root.setThemes([
      am5themes_Animated.new(root)
    ]);

    // Create wrapper container
    let container = root.container.children.push(am5.Container.new(root, {
      width: am5.percent(100),
      height: am5.percent(100),
      layout: root.verticalLayout
    }));

    // Create series
    let series = container.children.push(am5hierarchy.ForceDirected.new(root, {
      singleBranchOnly: false,
      downDepth: 1,
      initialDepth: 2,
      valueField: "value",
      categoryField: "name",
      childDataField: "children",
      centerStrength: 0.5
    }));

    series.data.setAll([data]);
    series.set("selectedDataItem", series.dataItems[0]);

    // Make stuff animate on load
    series.appear(1000, 100);
  }

}
