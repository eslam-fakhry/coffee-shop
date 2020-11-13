import { environment } from "./../../environments/environment";
import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { AuthService } from "./auth.service";

@Injectable({
  providedIn: "root",
})
export class UsersService {
  url = environment.apiServerUrl;
  public items: any = {};

  constructor(private auth: AuthService, private http: HttpClient) {}

  getHeaders() {
    const header = {
      headers: new HttpHeaders().set(
        "Authorization",
        `Bearer ${this.auth.activeJWT()}`
      ),
    };
    return header;
  }

  getUsers() {
    if (this.auth.can("manage:baristas")) {
      this.http
        .get(this.url + "/users", this.getHeaders())
        .subscribe((res: any) => {
          this.usersToItems(res.users);
          console.log(res);
        });
    }
  }

  getUserRoles(userId) {
    let res$;
    if (this.auth.can("manage:baristas")) {
      res$ = this.http.get(
        `${this.url}/users/${userId}/roles`,
        this.getHeaders()
      );
    }
    return res$;
  }

  hireBarista(user_id: string, toFireBarista = false) {
    let res$;
    if (this.auth.can("manage:baristas")) {
      res$ = this.http.patch(
        this.url + "/baristas/" + user_id,
        { toFireBarista },
        this.getHeaders()
      );
    }
    return res$;
  }

  usersToItems(users) {
    for (const user of users) {
      this.items[user["user_id"]] = user;
    }
  }
}
