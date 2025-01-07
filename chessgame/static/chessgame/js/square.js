export class Square {
  constructor(index) {
    this.index = index;
    this.element = this.createElement();
    this.piece = null;
  }

  createElement() {
    let cell = document.createElement("div");
    cell.className =
      Math.floor(this.index / 8) % 2 === this.index % 2 ? "white" : "black";
    return cell;
  }
}
