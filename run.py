import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # En producción, Gunicorn ejecutará la aplicación automáticamente
    # En desarrollo, usa debug mode si está habilitado
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port,
        use_reloader=debug
    )