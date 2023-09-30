import { Injectable } from '@angular/core';
import { Papers, Heatmap } from '../Interfaces/papers';
import * as Papa from 'papaparse';
import { HttpClient, HttpHeaders} from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class PapersServiceService {

  constructor(private http: HttpClient) { }

  jsonData: Papers[] = [];
  flagViewPapers:boolean = true;
  heatmapData: any;

  // Convertir a JSON
  parseCsvToJSON(csvString: string, strSeparator?: string) {
    const strSeparatorToUse = strSeparator || ','; // Usar el separador personalizado si se proporciona, de lo contrario, usar el predeterminado
    Papa.parse<any>(csvString, {
      delimiter: strSeparatorToUse,
      header: true,
      skipEmptyLines: true,
      complete: (strResult) => {
        const strData = strResult.data;
        // Verificar que las tres columnas estén presentes
        if (!strData.every(strRow => "Titles" in strRow && "Keywords" in strRow && "Abstract" in strRow)) {
          console.error("El CSV no contiene las columnas requeridas: Titles, Keywords y Abstract");
          this.jsonData = [] as Papers[]
          this.saveToLocalStorage(this.jsonData);
          this.jsonData = [] as Papers[]
          return;
        }
        // Seleccionar solo las columnas requeridas
        const strSelectedData = strData.map(strRow => ({
          Titles: strRow.Titles,
          Keywords: strRow.Keywords,
          Abstract: strRow.Abstract
        }));
        this.jsonData = strSelectedData as Papers[];


        ///// llamada a la api
        // Define los encabezados de la solicitud
        const headers = new HttpHeaders({
          'Content-Type': 'application/json', // Tipo de contenido
        });

        const body = {data: this.jsonData}
        
        this.http.post<Heatmap>('http://127.0.0.1:4000/api/matrices',
          body,
          {headers}).subscribe({
          next: (res) =>{
            console.log(res);
            localStorage.setItem('heatmap', res.heat_map)
            // this.heatmapData = res.heat_map;
          },
          error: (err) =>{
            console.log(err);
          }
        }
        )


        this.saveToLocalStorage(this.jsonData);
      }
    });
  }

  saveToLocalStorage ( strDatos : Papers[]){
    this.flagViewPapers = true;
    localStorage.setItem('datos',JSON.stringify(strDatos))
    localStorage.setItem('papersView',(this.flagViewPapers).toString())
  }

  obtenerToLocalStorage (){
    let datosGuardados = localStorage.getItem('datos') ;
    const flagViewPapersStr = localStorage.getItem('papersView');
    if (flagViewPapersStr !== null) {
      this.flagViewPapers = Boolean(flagViewPapersStr);
    } else {
      this.flagViewPapers = false;
    }
    if (datosGuardados) {
      this.jsonData = JSON.parse(datosGuardados) as Papers[];
    } else {
      this.jsonData =[]
      console.log('No se encontraron datos en el almacenamiento local.');
    }
  }

}
