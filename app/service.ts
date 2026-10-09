import { compute } from '@prisma/composer-prisma-cloud';
import node from '@prisma/composer/node';

/** The static web service. The build (scripts/build.sh) writes dist/server.mjs and dist/public/. */
export default compute({
  name: 'web',
  deps: {},
  build: node({ module: import.meta.url, dir: '../dist', entry: 'server.mjs' }),
});
