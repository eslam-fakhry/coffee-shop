import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { ManageUsersPage } from './manage-users.page';
import { UsersFormComponent } from './users-form/users-form.component';

const routes: Routes = [
  {
    path: '',
    component: ManageUsersPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  entryComponents: [UsersFormComponent],
  declarations: [ManageUsersPage, UsersFormComponent]
})
export class ManageUsersPageModule {}
