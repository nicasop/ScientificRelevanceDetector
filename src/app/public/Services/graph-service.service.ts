import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';
import { Graph } from '../Interfaces/graph';

@Injectable({
  providedIn: 'root'
})
export class GraphServiceService {

  constructor( private http: HttpClient ) { }
  getGraph(data: any):Observable<Graph>{
    // Define los encabezados de la solicitud
    const headers = new HttpHeaders({
      'Content-Type': 'application/json', // Tipo de contenido
    });

    const body = {data: data}

    return this.http.post<Graph>('https://back-scientificrelevancedetector.onrender.com/api/cluster',
    body,
    {headers})
  }
}
