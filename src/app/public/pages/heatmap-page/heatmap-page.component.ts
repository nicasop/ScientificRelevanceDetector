import { Component, OnInit, NgZone, PLATFORM_ID, Inject  } from '@angular/core';
import { Message, MessageService } from 'primeng/api';
import { PrimeNGConfig } from 'primeng/api'

import { HeatmapServiceService } from '../../Services/heatmap-service.service';
import { HeatMap, HeatMapData, Xaxis, Yaxis } from '../../Interfaces/heatmap';

// amCharts imports
import * as am5 from '@amcharts/amcharts5';
import * as am5xy from '@amcharts/amcharts5/xy';
// import am5themes_Animated from '@amcharts/amcharts5/themes/Dark';

@Component({
  selector: 'app-heatmap-page',
  templateUrl: './heatmap-page.component.html',
  styleUrls: ['./heatmap-page.component.css'],
  providers: [MessageService]
})
export class HeatmapPageComponent implements OnInit {

  flagViewHeat : boolean = false;
  msgPapers: Message[] = [];
  heatmap: HeatMap = {
    data: [],
    xaxis: [],
    yaxis: []
  };

  constructor(
    private heatmap_service: HeatmapServiceService,
    private primengConfig: PrimeNGConfig,
    private messageService: MessageService,
    @Inject(PLATFORM_ID) private platformId: Object,
    private zone: NgZone
  ) {

  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    console.log('init');
    const data = localStorage.getItem('matrix');
    this.flagViewHeat = false;
    this.heatmap_service.getHeatMap(data).subscribe({
      next: res => {
        console.log("Datos")
        console.log(res);
        this.heatmap = res
        this.flagViewHeat = true;
        this.drawHeatMap(this.heatmap.xaxis, this.heatmap.yaxis, this.heatmap.data);
      },
      error: err => {
        console.log(err);

      }
    })
  }

  ngAfterViewInit(){}

  drawHeatMap(xaxis:Xaxis[], yaxis:Yaxis[], data:HeatMapData[]){

    let root = am5.Root.new("chartdiv");
    // root.setThemes([am5themes_Animated.new(root)]);

    /////////// mapa de calor
    let chart = root.container.children.push(
      am5xy.XYChart.new(root, {
        panX: true,
        panY: true,
        wheelY: "zoomXY",
      pinchZoomX: true,
      pinchZoomY: true,
        layout: root.verticalLayout,


      })
    );

       // Add scrollbars
    chart.set("scrollbarX", am5.Scrollbar.new(root, {
      orientation: "horizontal"
    }));

    chart.set("scrollbarY", am5.Scrollbar.new(root, {
      orientation: "vertical"
    }));

    // Create Y-axis
    let yRenderer = am5xy.AxisRendererY.new(root, {
      visible: false,
      minGridDistance: 20,
      inversed: true,


    });

    yRenderer.grid.template.set("visible", false);

    let yAxis = chart.yAxes.push(am5xy.CategoryAxis.new(root, {
      maxDeviation: 0,
      renderer: yRenderer,
      categoryField: "yaxis",
    }));

    // Create X-Axis
    let xRenderer = am5xy.AxisRendererX.new(root, {
      visible: false,
      minGridDistance: 30,
      opposite:true
    });

    xRenderer.grid.template.set("visible", false);

    let xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
      renderer: xRenderer,
      categoryField: "xaxis",

    }));

    // Create series
    let series = chart.series.push(am5xy.ColumnSeries.new(root, {
      calculateAggregates: true,
      stroke: am5.color(0xffffff),
      clustered: false,
      xAxis: xAxis,
      yAxis: yAxis,
      categoryXField: "xaxis",
      categoryYField: "yaxis",
      valueField: "value"
    }));

    series.columns.template.setAll({
      tooltipText: "{value}",
      strokeOpacity: 1,
      strokeWidth: 2,
      width: am5.percent(100),
      height: am5.percent(100),
    });

    series.columns.template.events.on("pointerover", function(event) {
      let di = event.target.dataItem;
      let pointData:any = di?.dataContext;
      if (di) {
        heatLegend.showValue(pointData.value);
      }
    });

    series.events.on("datavalidated", function() {
      heatLegend.set("startValue", series.getPrivate("valueHigh"));
      heatLegend.set("endValue", series.getPrivate("valueLow"));
    });

    series.set("heatRules", [{
      target: series.columns.template,
      min: am5.color(0xfffb77),
      max: am5.color(0xfe131a),
      dataField: "value",
      key: "fill"
    }]);

    // Add legend
    let heatLegend = chart.bottomAxesContainer.children.push(am5.HeatLegend.new(root, {
      orientation: "horizontal",
      endColor: am5.color(0xfffb77),
      startColor: am5.color(0xfe131a)
    }));

    //set data
    series.data.setAll(data);
    yAxis.data.setAll(yaxis);
    xAxis.data.setAll(xaxis);


    // Add cursor
    chart.set("cursor", am5xy.XYCursor.new(root, {}));

    chart.appear(1000, 100);

  }

}
