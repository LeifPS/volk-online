// Schnellsuche: merkt sich offene Räume und schickt Suchende in einen passenden Raum.
import { DurableObject } from 'cloudflare:workers';
const CODE_ZEICHEN = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
const neuerCode = () => Array.from({ length: 5 }, () => CODE_ZEICHEN[Math.floor(Math.random() * CODE_ZEICHEN.length)]).join('');
const GUELTIG_MS = 3 * 60 * 1000;

export class Lobby extends DurableObject {
  constructor(ctx, env) { super(ctx, env); this.offen = new Map(); }
  schluessel(c) { return `${c.max}|${c.vk ? 1 : 0}|${c.rel ? 1 : 0}`; }
  async fetch(request) {
    const url = new URL(request.url); const jetzt = Date.now();
    for (const [code, e] of this.offen) if (jetzt - e.t > GUELTIG_MS) this.offen.delete(code);
    if (url.pathname === '/schnell') {
      const c = await request.json(); const max = [2, 3, 4].includes(+c.max) ? +c.max : 2; const cfg = { max, vk: !!c.vk, rel: !!c.rel };
      for (const [code, e] of this.offen) if (e.k === this.schluessel(cfg) && e.n < e.max && e.n >= 1) { e.n++; e.t = jetzt; return Response.json({ code, neu: false, cfg }); }
      const code = neuerCode(); this.offen.set(code, { k: this.schluessel(cfg), n: 1, max, t: jetzt }); return Response.json({ code, neu: true, cfg });
    }
    if (url.pathname === '/update') { const u = await request.json(); const e = this.offen.get(u.code); if (e) { if (!u.offen) this.offen.delete(u.code); else { e.n = u.n; e.t = jetzt; } } return new Response('ok'); }
    return new Response('?', { status: 404 });
  }
}
