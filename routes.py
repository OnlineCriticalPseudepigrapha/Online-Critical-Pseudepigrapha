
routes_in = (
  ('/$anything', '/grammateus3/$anything'),
  ('/$c/$f', '/grammateus3/$c/$f'),
)

routes_out = [(x, y) for (y, x) in routes_in]
