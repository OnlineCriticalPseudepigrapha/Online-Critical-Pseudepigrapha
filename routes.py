
routes_in = (
    # ('/admin/$anything', '/admin/$anything'),
    # ('/static/$anything', '/grammateus3/static/$anything'),
    # ('/appadmin/$anything', '/grammateus3/appadmin/$anything'),
    # ('/docs/$anything', '/grammateus3/docs/$anything'),
    ('/$anything', '/grammateus3/$anything'),
    ('/$c/$f', '/grammateus3/$c/$f'),
)

routes_out = [(x, y) for (y, x) in routes_in]
