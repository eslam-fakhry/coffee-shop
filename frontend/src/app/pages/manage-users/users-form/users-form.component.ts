import { Component, Input, OnInit } from "@angular/core";
import { ModalController } from "@ionic/angular";
import { AuthService } from "src/app/services/auth.service";
import { UsersService } from "src/app/services/users.service";

@Component({
  selector: "app-users-form",
  templateUrl: "./users-form.component.html",
  styleUrls: ["./users-form.component.scss"],
})
export class UsersFormComponent implements OnInit {
  @Input() user: any;
  roles: any;
  errors: string | null = null;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private usersService: UsersService
  ) {}

  ngOnInit() {
    this.usersService
      .getUserRoles(this.user["user_id"])
      .subscribe((res: any) => {
        this.roles = res.roles
      });
  }

  closeModal() {
    this.modalCtrl.dismiss();
  }

  hireBarista() {
    this.usersService.hireBarista(this.user["user_id"]).subscribe(
      (res: any) => {
        this.closeModal();
      },
      (err: any) => {
        if (err.status == 400) {
          this.errors = err.error.message;
        }
      }
    );
  }

  fireBarista() {
    this.usersService.hireBarista(this.user["user_id"], true).subscribe(
      (res: any) => {
        this.closeModal();
      },
      (err: any) => {
        if (err.status == 400) {
          this.errors = err.error.message;
        }
      }
    );
  }

  isManager() {
    if(!this.roles){
      return false
    }
    return this.roles.some(r=>r['name'].toLowerCase() === 'manager')
  }

  isBarista() {
    if(!this.roles){
      return false
    }
    return this.roles.some(r=>r['name'].toLowerCase() === 'barista')
  }
}
