import { Component, OnInit, NgZone, PLATFORM_ID, Inject  } from '@angular/core';
import { Message, MessageService } from 'primeng/api';
import { PrimeNGConfig } from 'primeng/api'
import { MdsServiceService } from '../../Services/mds-service.service';
import { MDS } from '../../Interfaces/mds';

// amCharts imports
import * as am5 from '@amcharts/amcharts5';
import * as am5xy from '@amcharts/amcharts5/xy';
// import * as am5hierarchy from "@amcharts/amcharts5/hierarchy";
import am5themes_Animated from '@amcharts/amcharts5/themes/Dark';

@Component({
  selector: 'app-mds-page',
  templateUrl: './mds-page.component.html',
  styleUrls: ['./mds-page.component.css'],
  providers: [MessageService]
})
export class MdsPageComponent implements OnInit {

  flagViewMDS : boolean = false;
  msgPapers: Message[] = [];
  mds_data: MDS[] = [];

  constructor(
    private mds_service: MdsServiceService,
    private primengConfig: PrimeNGConfig,
    private messageService: MessageService,
    @Inject(PLATFORM_ID) private platformId: Object,
    private zone: NgZone) {



    }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.flagViewMDS = false;
    console.log('init');
    const data = localStorage.getItem('matrix');
    this.mds_service.getMDS(data).subscribe({
      next: res => {
        this.mds_data = res;
        this.flagViewMDS = true;
        this.drawScatter(this.mds_data)
      },
      error: err => {
        console.log('error al realizar la peticion');
      }
    })
  }

  ngAfterViewInit(){}

  drawScatter( data: MDS[] ){
    let root = am5.Root.new("chartdiv");

    // Set themes
    root.setThemes([
      am5themes_Animated.new(root)
    ]);

    // Create chart
    let chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelY: "zoomXY",
      pinchZoomX: true,
      pinchZoomY: true
    }));

    // Create axes
    let xAxis = chart.xAxes.push(am5xy.ValueAxis.new(root, {
      renderer: am5xy.AxisRendererX.new(root, { minGridDistance: 50 }),
      tooltip: am5.Tooltip.new(root, {})
    }));

    let yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
      renderer: am5xy.AxisRendererY.new(root, {}),
      tooltip: am5.Tooltip.new(root, {})
    }));

    // Create series
    let series = chart.series.push(am5xy.LineSeries.new(root, {
      xAxis: xAxis,
      yAxis: yAxis,
      valueYField: "y",
      valueXField: "x",
      valueField: "value",
      tooltip: am5.Tooltip.new(root, {
        labelText: "x: {valueX}, y: {valueY}, value: {value}"
      })
    }));

    series.strokes.template.set("visible", false);

    // Add cursor
    chart.set("cursor", am5xy.XYCursor.new(root, {
      xAxis: xAxis,
      yAxis: yAxis,
      snapToSeries: [series]
    }));

    // Add scrollbars
    chart.set("scrollbarX", am5.Scrollbar.new(root, {
      orientation: "horizontal"
    }));

    chart.set("scrollbarY", am5.Scrollbar.new(root, {
      orientation: "vertical"
    }));

    // add graphics to line series which will contain bullets
    let canvasBullets = series.children.push(am5.Graphics.new(root, {}));

    canvasBullets.set("draw", (display) => {

      // loop through all data items
      am5.array.each(series.dataItems, (dataItem) => {
        // set fill style from data context
        let dataContext:any = dataItem.dataContext;

        if (dataContext) {
          const point = dataItem.get("point");
          if (point) {
            display.beginPath();
            display.beginFill(dataContext.color);
            display.drawCircle(point.x, point.y, 30 / 2);
            display.endFill();
          }
        }
      })

    })

    // user data is set on each redraw, so we use this to mark draw as dirty
    series.strokes.template.on("userData", drawBullets);

    function drawBullets() {
      canvasBullets._markDirtyKey("draw");
    }

    series.data.setAll(data);
  }



  showSuccess() {
    this.messageService.add({key: 'msg', severity:'success', summary: 'Correcto', detail: 'Base de datos cargada'});
  }

  showError() {
    // this.myForm.reset({file:null,separetor:','})
    this.messageService.add({key: 'msg', severity:'error', summary: 'Error', detail: 'El CSV no contiene las columnas requeridas: Titles, Keywords y Abstract o separador incorrecto'});
  }

  onConfirm() {
    this.messageService.clear('c');
  }

  onReject() {
    this.messageService.clear('c');
  }

  clear() {
    this.messageService.clear();
  }


}
