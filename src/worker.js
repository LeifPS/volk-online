// Cloudflare Worker: Einstieg, Schnellsuche (Lobby) und Spielräume (Durable Objects).
import { Raum } from './raum.js';
import { Lobby } from './lobby.js';
export { Raum, Lobby };

const CODE_ZEICHEN = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
export const neuerCode = () => Array.from({ length: 5 }, () => CODE_ZEICHEN[Math.floor(Math.random() * CODE_ZEICHEN.length)]).join('');

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const m = url.pathname.match(/^\/ws\/raum\/([A-Za-z0-9]{3,8})$/);
    if (m) {
      if (request.headers.get('Upgrade') !== 'websocket') return new Response('WebSocket erwartet', { status: 426 });
      return env.RAUM.get(env.RAUM.idFromName(m[1].toUpperCase())).fetch(request);
    }
    if (url.pathname === '/api/schnell' && request.method === 'POST') {
      const cfg = await request.json().catch(() => ({}));
      return env.LOBBY.get(env.LOBBY.idFromName('haupt')).fetch(new Request('https://lobby/schnell', { method: 'POST', body: JSON.stringify(cfg) }));
    }
    if (url.pathname === '/api/status') return Response.json({ ok: true });
    return env.ASSETS ? env.ASSETS.fetch(request) : new Response('Nicht gefunden', { status: 404 });
  },
};
