import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class AuthInterceptorInterceptor implements HttpInterceptor {

  constructor() {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    let token = localStorage.getItem("auth_token");
    if(token != null){
      console.log(token);
      return next.handle(request.clone({setHeaders: {
        auth_token: token
      }}));
    }
    return next.handle(request);

  }
}
