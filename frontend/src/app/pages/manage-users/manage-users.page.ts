import { UsersFormComponent } from "./users-form/users-form.component";
import { UsersService } from "./../../services/users.service";
import { Component, OnInit } from "@angular/core";
import { ModalController } from "@ionic/angular";
import { AuthService } from "src/app/services/auth.service";

@Component({
  selector: "app-manage-users",
  templateUrl: "./manage-users.page.html",
  styleUrls: ["./manage-users.page.scss"],
})
export class ManageUsersPage implements OnInit {
  Object = Object;
  constructor(
    public users: UsersService,
    private modalCtrl: ModalController,
    public auth: AuthService
  ) {}

  ngOnInit() {
    this.users.getUsers();
  }

  async openForm(activeUser: any) {
    if (!this.auth.can('manage:baristas')) {
      return;
    }

    const modal = await this.modalCtrl.create({
      component: UsersFormComponent,
      componentProps: { user: activeUser },
    });

    modal.present();
  }
}
