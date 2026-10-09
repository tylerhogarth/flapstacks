import { fileURLToPath } from 'node:url';
import { join, normalize } from 'node:path';
import service from './service.ts';

// The built tree is copied verbatim, so resolve siblings against this file, not cwd.
const root = fileURLToPath(new URL('./public/', import.meta.url));

const IMMUTABLE = /\.(webp|jpg|png|ico|woff2?)$/;

function resolve(pathname: string): string | null {
  let path = decodeURIComponent(pathname);
  if (path.endsWith('/')) path += 'index.html';
  const full = normalize(join(root, path));
  if (!full.startsWith(root)) return null;
  return full;
}

async function handle(req: Request): Promise<Response> {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    return new Response('Method Not Allowed', { status: 405, headers: { allow: 'GET, HEAD' } });
  }
  const { pathname } = new URL(req.url);
  const full = resolve(pathname);
  if (!full) return new Response('Not Found', { status: 404 });

  const file = Bun.file(full);
  if (!(await file.exists())) return new Response('Not Found', { status: 404 });

  const headers = new Headers({
    'content-type': file.type,
    'content-length': String(file.size),
    'cache-control': IMMUTABLE.test(full) ? 'public, max-age=31536000, immutable' : 'public, max-age=300',
    'x-content-type-options': 'nosniff',
  });
  return new Response(req.method === 'HEAD' ? null : file, { headers });
}

Bun.serve({ port: service.port(), hostname: '0.0.0.0', fetch: handle });
