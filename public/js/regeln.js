// Platzhalter – wird in Stufe 2 durch die vollständige Regelseite ersetzt.
export function regelnSeite(app, D, zurueck) {
  app.innerHTML = `<div class="menue"><h2 style="color:#fff">Regeln</h2><div class="karte-panel"><p>Die vollständigen Regeln folgen in Stufe 2.</p></div><div class="btns"><button id="r-zu">Zurück</button></div></div>`;
  document.getElementById('r-zu').onclick = zurueck;
}
