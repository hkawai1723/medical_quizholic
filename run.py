import os
from flask import render_template
from main import create_app

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', error=e), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html', error=e), 500

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 8080))
#     app.run(host="0.0.0.0", port=port)

# if __name__ == '__main__':
#     app.run(debug=True, port=8080)