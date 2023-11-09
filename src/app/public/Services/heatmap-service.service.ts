import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';
import { HeatMap } from '../Interfaces/heatmap';

@Injectable({
  providedIn: 'root'
})
export class HeatmapServiceService {

  constructor(private http: HttpClient) { }
  getHeatMap(data: any):Observable<HeatMap>{
    // Define los encabezados de la solicitud
    const headers = new HttpHeaders({
      'Content-Type': 'application/json', // Tipo de contenido
    });

    const body = {data: data}
    return this.http.post<HeatMap>('http://127.0.0.1:4000/api/heatmap',
    body,
    {headers})
  }
}
