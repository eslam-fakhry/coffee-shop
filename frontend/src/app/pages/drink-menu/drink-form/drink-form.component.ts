import { Component, OnInit, Input } from "@angular/core";
import { Drink, DrinksService } from "src/app/services/drinks.service";
import { ModalController } from "@ionic/angular";
import { AuthService } from "src/app/services/auth.service";

@Component({
  selector: "app-drink-form",
  templateUrl: "./drink-form.component.html",
  styleUrls: ["./drink-form.component.scss"],
})
export class DrinkFormComponent implements OnInit {
  @Input() drink: Drink;
  @Input() isNew: boolean;
  errors: null | string = null;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private drinkService: DrinksService
  ) {}

  ngOnInit() {
    if (this.isNew) {
      this.drink = {
        id: -1,
        title: "",
        recipe: [],
      };
      this.addIngredient();
    }
  }

  customTrackBy(index: number, obj: any): any {
    return index;
  }

  addIngredient(i: number = 0) {
    this.drink.recipe.splice(i + 1, 0, { name: "", color: "white", parts: 1 });
  }

  removeIngredient(i: number) {
    this.drink.recipe.splice(i, 1);
  }

  closeModal() {
    this.modalCtrl.dismiss();
  }

  saveClicked() {
    this.drinkService.saveDrink(this.drink).subscribe((res: any) => {
      this.closeModal();
     },(err: any) =>{
      if (err.status == 400) {
        this.errors = err.error.message
      }
    });
  }

  deleteClicked() {
    this.drinkService.deleteDrink(this.drink);
    this.closeModal();
  }
}
