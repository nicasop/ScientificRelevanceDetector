import { AppRoutingModule } from './../../../app-routing.module';
import { Component, Input, OnInit,ViewChild, Inject, NgZone, PLATFORM_ID  } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { FormBuilder, FormGroup,Validators} from '@angular/forms';
import { ValidatorsService } from '../../Validators/validators.service';
import { Message, MessageService } from 'primeng/api';
import { PrimeNGConfig } from 'primeng/api'
import { PapersServiceService } from '../../Services/papers-service.service';

// amCharts imports
import * as am5 from '@amcharts/amcharts5';
import * as am5xy from '@amcharts/amcharts5/xy';
import * as am5hierarchy from "@amcharts/amcharts5/hierarchy";
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated';

@Component({
  selector: 'app-papers-page',
  templateUrl: './papers-page.component.html',
  styleUrls: ['./papers-page.component.css'],
  providers: [MessageService]
})
export class PapersPageComponent implements OnInit {
  constructor(
    private fb: FormBuilder,
    private validatorService : ValidatorsService,
    private messageService: MessageService,
    private primengConfig: PrimeNGConfig,
    public papersService : PapersServiceService,
    @Inject(PLATFORM_ID) private platformId: Object, 
    private zone: NgZone
    ) { 
      // this.chartOptions = {}
    }

  boolLoading : boolean = false;
  boolValid : boolean = false;
  strContentCsv : String = '';
  strSeparator : string = ',';
  msgPapers: Message[] = [];
  cols: any[]= [''];
  flagViewPapers : boolean = false;
  flagHeatMap: boolean = false;

  _selectedColumns: any[] = [''];

  /////// grafico
  private root!: am5.Root;

  // Run the function only in the browser
  browserOnly(f: () => void) {
    if (isPlatformBrowser(this.platformId)) {
      this.zone.runOutsideAngular(() => {
        f();
      });
    }
  }

  @Input() get selectedColumns(): any[] {
    return this._selectedColumns;
  }

  set selectedColumns(val: any[]) {
    //restore original order
    this._selectedColumns = this.cols.filter(col => val.includes(col));
  }

  ngOnInit(): void {
    this.myForm.reset({file:null,separetor:','});
    this.primengConfig.ripple = true;
    this.msgPapers = [
      {severity:'info', summary:'', detail:' El analizador de similitud escogera las filas Titles, Keywords y Abstract del CSV. Verificar que el archivo .CSV cuente con estas columnas con el nombre de lo Headers mencionados.'},
    ];
    this.papersService.obtenerToLocalStorage();
    this.cols = [
      { field: 'Titles', header: 'Titles' },
      { field: 'Keywords', header: 'Keywords' },
      { field: 'Abstract', header: 'Abstract' }
  ];
    this.flagViewPapers =this.papersService.flagViewPapers
    this._selectedColumns = this.cols
    console.log("On init ");
    console.log(this.papersService.jsonData);

  }

  showSuccess() {
    this.messageService.add({severity:'success', summary: 'Correcto', detail: 'Base de datos cargada'});
  }

  showError() {
    this.myForm.reset({file:null,separetor:','})
    this.messageService.add({severity:'error', summary: 'Error', detail: 'El CSV no contiene las columnas requeridas: Titles, Keywords y Abstract o separador incorrecto'});
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



  //Formulario Reactivo
  public myForm: FormGroup = this.fb.group({
    file : ['f',Validators.required],
    separetor : [',',[Validators.required,Validators.minLength(1),Validators.maxLength(1)]]
  })
  isValidField(field:string):boolean | null{
    return this.validatorService.isValidField(this.myForm,field)
  }

  getFieldError(field: string): string |null{
    return this.validatorService.getFieldError(this.myForm,field)
  }
  onLoadFile():void{
    if(this.myForm.invalid) {
      this.myForm.markAllAsTouched();
      return;
    };
    if(!this.boolValid) return;

    console.log(this.myForm.value)
    console.log(this.myForm.value['separetor'])
    this.strSeparator = this.myForm.value['separetor']
    this.papersService.parseCsvToJSON(this.strContentCsv.toString(),this.strSeparator )
    this.strContentCsv = ''
    if(this.papersService.jsonData.length == 0){
      this.flagViewPapers =this.papersService.flagViewPapers
      this.showError()
      return
    }
    this.showSuccess()
    console.log("Datos JSON")
    console.log(this.papersService.jsonData)
    this.flagViewPapers =this.papersService.flagViewPapers
    this.cols = [
      { field: 'Titles', header: 'Titles' },
      { field: 'Keywords', header: 'Keywords' },
      { field: 'Abstract', header: 'Abstract' }
    ];
    this._selectedColumns = this.cols
    this.myForm.reset({file:null,separetor:','})

    setTimeout(() => { 
      // this.flagHeatMap = true;

      //////////////////////////////// Heat Map
      // const heat_map_str: string | null = localStorage.getItem('heatmap');
      // const heat_map_data = JSON.parse(heat_map_str || '');
      
      // const heat_map_xaxis: string | null = localStorage.getItem('xaxis');
      // const heat_map_xaxis_data = JSON.parse(heat_map_xaxis || '');

      // const heat_map_yaxis: string | null = localStorage.getItem('yaxis');
      // const heat_map_yaxis_data = JSON.parse(heat_map_yaxis || '');

      // this.drawHeatMap(heat_map_xaxis_data, heat_map_yaxis_data, heat_map_data)
      //////////////////////////////// Heat Map

      //////////////////////////////// Cluster
      // const cluster_str: string | null = localStorage.getItem('cluster');
      // const cluster_data = JSON.parse(cluster_str || '');

      // this.drawHierarchy(cluster_data)
      //////////////////////////////// Cluster

      //////////////////////////////// MDS
      const mds_str: string | null = localStorage.getItem('mds');
      const mds_data = JSON.parse(mds_str || '');

      this.drawScatter(mds_data)
      //////////////////////////////// MDS
      
    }, 20000); 
  }
  //Fin de formulario

  onFileSelected(event: any): void {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      this.boolLoading = true;
      setTimeout(() => {
        this.readFileContent(selectedFile);
      }, 2000); // 2000 milisegundos = 2 segundos
    }
    this.boolValid =true;
  }

  readFileContent(file: File): void {
    const fileReader = new FileReader();
    fileReader.onload = (e: any) => {
      this.strContentCsv = e.target.result;
      this.boolLoading = false;
    };
    console.log("Cargando el contenido ......")
    fileReader.readAsText(file);
  }

  drawHeatMap(xaxis:any, yaxis:any, data:any){
    this.browserOnly(() => {
      let root = am5.Root.new("chartdiv");

      root.setThemes([am5themes_Animated.new(root)]);

      /////////// mapa de calor
      let chart = root.container.children.push(
        am5xy.XYChart.new(root, {
          panX: false,
          panY: false,
          wheelX: "none",
          wheelY: "none",
          layout: root.verticalLayout
        })
      );

      // Create Y-axis
      let yRenderer = am5xy.AxisRendererY.new(root, {
        visible: false,
        minGridDistance: 20,
        inversed: true
      });
      
      yRenderer.grid.template.set("visible", false);
      
      let yAxis = chart.yAxes.push(am5xy.CategoryAxis.new(root, {
        maxDeviation: 0,
        renderer: yRenderer,
        categoryField: "yaxis"
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
        categoryField: "xaxis"
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
        height: am5.percent(100)
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
      
      
      // Set up heat rules
      // https://www.amcharts.com/docs/v5/concepts/settings/heat-rules/
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

      this.root = root;
    });
  }

  drawHierarchy(data:any){
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

  drawScatter( data:any ){
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

    // let data = [];
    // for (var i = 0; i < 200; i++) {
    //   data.push({ x: Math.random() * 100, y: Math.random() * 100, color: am5.Color.fromString("#" + Math.floor(Math.random() * 16777215).toString(16)), value: Math.random() * 20 })
    // }

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

  ngAfterViewInit() { 
    // this.drawHierarchy();
    // this.drawScatter()
  }

  ngOnDestroy() {
    // Clean up chart when the component is removed
    this.browserOnly(() => {
      if (this.root) {
        this.root.dispose();
      }
    });
  }

}
