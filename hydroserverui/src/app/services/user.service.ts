import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  
  constructor(
    private http: HttpClient
  ) { }

  async login(email: string, password: string){
    try{
      let response = await this.http.post<{token: string}>(`${environment.API_URL}/auth/login`, {
        email: email,
        password: password
      }).toPromise();
      console.log(response.token);
      localStorage.setItem("auth_token", response.token);
      return response.token;
    } catch(err: any){
      console.log(err.status);
      throw Error("Failed to login");
    }
  }
}
