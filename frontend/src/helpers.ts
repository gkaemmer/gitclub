export type obj = { [key: string]: unknown };

export function isObj(x: unknown): x is obj {
  return typeof x === 'object' && x !== null;
}

export const popField = (o: obj, f: string) =>
  Object.fromEntries(Object.entries(o).filter(([k]) => k !== f));

export function camelizeKeys(o: obj): unknown {
  const snakeToCamel = (s: string) =>
    s.replace(/_[a-z]/g, (c) => c[1].toUpperCase());

  return Object.fromEntries(
    Object.entries(o).map(([k, v]) => [snakeToCamel(k), v])
  );
}

export function snakeifyKeys(o: obj): unknown {
  const camelToSnake = (s: string) =>
    s.replace(/[A-Z]/g, (l) => '_' + l.toLowerCase());

  return Object.fromEntries(
    Object.entries(o).map(([k, v]) => [camelToSnake(k), v])
  );
}
