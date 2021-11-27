import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpResponse,
  HttpInterceptor,
  HttpErrorResponse,
} from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { LoginPromptServiceService } from '../services/login-prompt-service.service';
import {catchError, filter, tap} from "rxjs/operators"

@Injectable()
export class AuthInterceptorInterceptor implements HttpInterceptor {

  constructor(
    private loginSignalService: LoginPromptServiceService
  ) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    let token = localStorage.getItem("auth_token");
    if(token != null){
      console.log(token);
      request = request.clone({setHeaders: {
        auth_token: token
      }});
    }
    return next.handle(request).pipe(
      catchError((response) => this.handleError(response)),
      filter((response) => response instanceof HttpResponse),
      tap((event) => {
        this.handleResponse(event as HttpResponse<any>);
      })
    )
  }

  handleError(response: HttpErrorResponse){
    if(response.status == 401){
      //handle unauthorized by prompting to login
      this.loginSignalService.displayLogin();
      return throwError(response);
    } else{
      return throwError(response);
    }
  }

  handleResponse(response: HttpResponse<any>){
    console.log("Handling response");
    if(response.status == 401){
      //need to login
      console.log("401 recieved");
      this.loginSignalService.displayLogin();
    }
    if(response.headers.has("refresh-token")){
      let refreshToken = response.headers.get("refresh-token")!;
      localStorage.setItem("auth_token", refreshToken);
    }
    return response;
  }
}
