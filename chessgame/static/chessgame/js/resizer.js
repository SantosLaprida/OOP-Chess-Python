const wrapper = document.getElementById("boardWrapper");
const resizer = document.getElementById("resizer");

const getCssVal = (name, fallback) =>
  getComputedStyle(document.documentElement).getPropertyValue(name).trim() ||
  fallback;

const MIN = parseInt(getCssVal("--min-board", "240px"), 10);
const MAX = parseInt(getCssVal("--max-board", "1000px"), 10);

let startX, startY, startSize;

function onPointerMove(e) {
  const dx = e.clientX - startX;
  const dy = e.clientY - startY;
  const delta = Math.max(dx, dy);
  let next = Math.max(MIN, Math.min(MAX, startSize + delta));
  document.documentElement.style.setProperty("--board-size", `${next}px`);
}

function onPointerUp() {
  window.removeEventListener("pointermove", onPointerMove);
  window.removeEventListener("pointerup", onPointerUp);
}

resizer.addEventListener("pointerdown", (e) => {
  e.preventDefault();
  startX = e.clientX;
  startY = e.clientY;
  startSize = wrapper.offsetWidth;
  window.addEventListener("pointermove", onPointerMove);
  window.addEventListener("pointerup", onPointerUp);
});
