// 16x16 Pixelart-Symbole I-VII (PNG als Data-URL). CSS: image-rendering: pixelated;
export const EPOCHEN_ICONS = {
 "I": {
  "epoche": "Antike",
  "png": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYUlEQVR4XmNkYGBgSPVW/A+iSQWzt95nZAFpDraTZtBT4idJ/6V7H0Hq/7PAdEEFSAZM+HS45y4AY3wArwHEgFEDGIZDGMBTIjawc3ICwaRAcToAu+DEtXcEbcIFGCnNzgCnuhgjuToMoAAAAABJRU5ErkJggg=="
 },
 "II": {
  "epoche": "Klassik",
  "png": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAZklEQVR4XmNkYGBg0HBN/g+iSQU3ds9lZAFpVrIKYhCS1yVJ/7uHl0Hq/7PAdEEFSAZMuHRsLVcHYxBAZqMDnAYQC0YNYBgOYQBPiejAu/MmXAiZTfWEBHbBy5sniU14GICR0uwMAINnHHZMcA9VAAAAAElFTkSuQmCC"
 },
 "III": {
  "epoche": "Mittelalter",
  "png": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAY0lEQVR4XmNkYGBgcHHx/Q+iSQV79mxmZAFptrCwZ5CXVyZJ/8OHd0Hq/7PAdEEFSAZM6DqaqwLAGARwsZEBhgGkglEDGIZDGDDCkjI54MSJg5SHATgv3Lp1jRwHgAEjpdkZAOLVIHGRJrOHAAAAAElFTkSuQmCC"
 },
 "IV": {
  "epoche": "Renaissance",
  "png": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAeElEQVR4XmNkYGBg8JbX+A+iSQVbH95gZAFptpdWYlDiEyJJ/71P70Dq/7PAdEEFSAZM6DpK90wCYxDAxUYGGAaQCmhrQLdLHtwrIADjDyEvIDsbm/NBgLaBSAxghCVlcsDBp/co9wI4L1x795IcB4ABI4igJDsDACJZKXVRfMKgAAAAAElFTkSuQmCC"
 },
 "V": {
  "epoche": "Industrie",
  "png": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAdUlEQVR4XmNkYGBgSNaR/w+iSQVzrzxkZAFpDlSRZtAV4SNJ/+U3n0Dq/7PAdEEFSAZMuHR4L1sExiCAzEYHOA0gFtDOgK1RcXDngwCMP4S8gOxsXM4HAdoFIrGAoAvwOZ8qXgDnhZMv3hHrYgzACBKhJDsDAINpIrHL4a+OAAAAAElFTkSuQmCC"
 },
 "VI": {
  "epoche": "Moderne",
  "png": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAfElEQVR4XmNkYGBgkPTz+A+iSQXPN+1gZAFpFnO0ZuBWViBJ/9e7D0Dq/7PAdEEFSAZM6DoupEeCMQjgYiMDDANIBdQ3wGDmcrjzQQDGxwWo7wJSAVYXwJxNyPkgMPBeYIQlZXLAq/1HKfcCOC98vHqDHAeAASOIoCQ7AwCQbykRS8XitwAAAABJRU5ErkJggg=="
 },
 "VII": {
  "epoche": "Atomzeitalter",
  "png": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAeklEQVR4XmNkYGBg0AiR/w+iSQU31jxkZAFpVnKTZhBS4yNJ/7tbn0Dq/7PAdEEFSAZMyDq2xiwCYxAghg0CKAaQA6hrgPeSOLjzQQDGxweo6wJyAIYLYM4mxvmDIxYYYUmZHHBv11PKYwGcF15efEeOA8CAEURQkp0BpqUsu98YtgUAAAAASUVORK5CYII="
 }
};

// Zeitalter 0..6 -> Bild. Scharf vergrößert (image-rendering: pixelated, siehe CSS .za)
const REIHE = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'];
export const zaName = (z) => EPOCHEN_ICONS[REIHE[z]].epoche;
export const zaIcon = (z, px = 24, extra = '') => `<img class="za ${extra}" src="${EPOCHEN_ICONS[REIHE[z]].png}" width="${px}" height="${px}" alt="Zeitalter ${REIHE[z]} · ${zaName(z)}" title="${REIHE[z]} · ${zaName(z)}" draggable="false">`;
