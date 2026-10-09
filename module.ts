import { module } from '@prisma/composer';
import web from './app/service.ts';

export default module('flapstacks', ({ provision }) => {
  provision(web);
});
