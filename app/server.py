from app import app
from app import api
from app import blueprint
from app import death_namespace
from app import recovered_namespace
from app import confirmed_namespace


@app.route(r'/', methods=["GET"])
def index():
    return "<h1>Index Page: COVID-19 API</h1>"


def init_app():
    api.init_app(blueprint)
    api.add_namespace(death_namespace)
    api.add_namespace(recovered_namespace)
    api.add_namespace(confirmed_namespace)
    app.register_blueprint(blueprint)

    # db.init_app(app)
    # ma.init_app(app)
    # with app.app_context():
    #     db.create_all()

    return True


if __name__ == '__main__':
    try:
        init_app()
        app.run(host="localhost", port=5555, debug=True)
    except Exception as e:
        print(f'App Crashed: [ {e} ]')