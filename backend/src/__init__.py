from flask import Flask, render_template_string, request
from flask_cors import CORS
from .config import Config
from .db import db
from .routes import api, configure_scheduler
from .controllers import admin_create, create_skills


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {"origins": "http://localhost:5173"}},
        methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    app.register_blueprint(api)

    with app.app_context():
        db.create_all()
        admin_create()
        create_skills()

    @app.route("/")
    def index():
        from collections import defaultdict

        route_map = defaultdict(list)

        for rule in app.url_map.iter_rules():
            if rule.endpoint != "static":
                bp = rule.endpoint.split(".")[0] if "." in rule.endpoint else "main"
                methods = ", ".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))

                # Replace <params> with placeholders for demo
                path = rule.rule.replace("<", "{").replace(">", "}")
                try:
                    url = request.host_url.rstrip("/") + rule.rule.replace(
                        "<", "{"
                    ).replace(">", "}")
                except Exception:
                    url = rule.rule  # fallback
                route_map[bp].append({"url": url, "rule": path, "methods": methods})

        return render_template_string(
            """
            <h1>API Routes</h1>
            {% for bp, routes in route_map.items() %}
                <h2>{{ bp }}</h2>
                <ul>
                    {% for route in routes %}
                        <li>
                            <code>[{{ route.methods }}]</code>
                            <a href="{{ route.url }}" target="_blank">{{ route.rule }}</a>
                        </li>
                    {% endfor %}
                </ul>
            {% endfor %}
        """,
            route_map=route_map,
        )

    # Configure the session cleanup scheduler
    configure_scheduler(app)

    return app
