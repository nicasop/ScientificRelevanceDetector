import { Injectable } from '@angular/core';
import { MDS } from '../Interfaces/mds';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class MdsServiceService {

  constructor(private http: HttpClient) { }

  getMDS(data: any): Observable<MDS[]>{
    // Define los encabezados de la solicitud
    const headers = new HttpHeaders({
      'Content-Type': 'application/json', // Tipo de contenido
    });

    const body = {data: data}

    return this.http.post<MDS[]>('http://127.0.0.1:4000/api/mds',
          body,
          {headers})
  }

}
