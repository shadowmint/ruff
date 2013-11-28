import ruff as r

# Paths
py = r.path(__file__, 'bin', 'py')
public_html = r.path(__file__, 'client', 'public')

# Start client server
r.command('open', 'http://localhost:3001/index.html')
r.command(py, '-m', 'wtest.main')
r.serve('0.0.0.0', 3001, public_html)
r.run()
