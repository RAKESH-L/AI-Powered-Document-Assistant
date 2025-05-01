import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  private apiUrl = 'http://127.0.0.1:5000/upload'; // Update the API URL as per your backend's actual URL

  constructor(private http: HttpClient) { }

  uploadDocument(file: File, question: string): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('question', question);

    return this.http.post<any>(this.apiUrl, formData)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error('An error occurred:', error.error.message);
    } else {
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    return throwError(
      'Something went wrong; please try again later.');
  }
}
