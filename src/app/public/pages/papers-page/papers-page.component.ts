import { AppRoutingModule } from './../../../app-routing.module';
import { Component, Input, OnInit,ViewChild  } from '@angular/core';
import { FormBuilder, FormGroup,Validators} from '@angular/forms';
import { ValidatorsService } from '../../Validators/validators.service';
import {Message,MessageService} from 'primeng/api';
import { PrimeNGConfig } from 'primeng/api'
import { PapersServiceService } from '../../Services/papers-service.service';

import {
  ChartComponent,
  ApexAxisChartSeries,
  ApexTitleSubtitle,
  ApexDataLabels,
  ApexChart
} from "ng-apexcharts";

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  dataLabels: ApexDataLabels;
  title: ApexTitleSubtitle;
  colors: any;
};


@Component({
  selector: 'app-papers-page',
  templateUrl: './papers-page.component.html',
  styleUrls: ['./papers-page.component.css'],
  providers: [MessageService]
})
export class PapersPageComponent implements OnInit {

  @ViewChild("chart") chart!: ChartComponent;
  public chartOptions: Partial<ChartOptions>;

  constructor(
    private fb: FormBuilder,
    private validatorService : ValidatorsService,
    private messageService: MessageService,
    private primengConfig: PrimeNGConfig,
    public papersService : PapersServiceService
    ) {
      this.chartOptions = {
        series: [
          {
            name: "Metric1",
            data: this.generateData(18,
              0,
              90
            )
          },
          {
            name: "Metric2",
            data: this.generateData(18,
              0,
              90
            )
          },
          {
            name: "Metric3",
            data: this.generateData(18,
              0,
              90
            )
          },
          {
            name: "Metric4",
            data: this.generateData(18,
              0,
              90
            )
          },
          {
            name: "Metric5",
            data: this.generateData(18,
              0,
              90
            )
          },
          {
            name: "Metric6",
            data: this.generateData(18,
              0,
              90
            )
          },
          {
            name: "Metric7",
            data: this.generateData(18 ,
              0,
              90
            )
          },
          {
            name: "Metric8",
            data: this.generateData(18,
              0,
              90
            )
          },
          {
            name: "Metric9",
            data: this.generateData(18,
              0,
              90
            )
          }
        ],
        chart: {
          height: 350,
          type: "heatmap",
          foreColor:"white"
        },
        dataLabels: {
          enabled: false,
        },
        colors: ["#008FFB"],
        title: {
          text: "HeatMap Chart (Single color)",
          style: {
            color:"white"
          },
        }
      };
  }

  public generateData(count:number, max:number,min:number) {
    var i = 0;
    var series = [];
    while (i < count) {
      var x = "w" + (i + 1).toString();
      var y =
        Math.floor(Math.random() * (max - min + 1)) + min;

      series.push({
        x: x,
        y: y
      });
      i++;
    }
    return series;
  }

  boolLoading : boolean = false;
  boolValid : boolean = false;
  strContentCsv : String = '';
  strSeparator : string = ',';
  msgPapers: Message[] = [];
  cols: any[]= [''];
  flagViewPapers : boolean = false;

  _selectedColumns: any[] = [''];

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



}
