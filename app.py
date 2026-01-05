from flask import Flask, jsonify, request
from flask_mail import Mail, Message
from flask_cors import CORS
import os


DEFAULT_SENDER = os.getenv("MAIL_USERNAME")
DEFAULT_PASSWORD = os.getenv("MAIL_PASSWORD")
DEFAULT_RECIPIENT = os.getenv("RECIPIENT_EMAIL")

os.getenv("MAIL_USERNAME")

def create_app() -> Flask:
    """Set up a simple Flask app that emails sample requests."""
    app = Flask(__name__)

    app.config.update(
        MAIL_SERVER="smtp.gmail.com",
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=DEFAULT_SENDER,
        MAIL_PASSWORD=DEFAULT_PASSWORD,
        MAIL_DEFAULT_SENDER=DEFAULT_SENDER,
    )
    app.config["RECIPIENT_EMAIL"] = DEFAULT_RECIPIENT

    mail = Mail(app)
    CORS(app)

    @app.route("/api/request-sample", methods=["POST", "OPTIONS"])
    def request_sample():
        if request.method == "OPTIONS":
            return (
                "",
                204,
                {
                    "Access-Control-Allow-Origin": request.headers.get(
                        "Origin", "*"
                    ),
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": request.headers.get(
                        "Access-Control-Request-Headers", "Content-Type"
                    ),
                },
            )

        data = request.get_json(force=True) or {}

        subject = f"New Sample Request from {data.get('name', 'Unknown')}"
        body_lines = [
            "You have received a new sample request.",
            "",
            f"Name: {data.get('name', '')}",
            f"Email: {data.get('email', '')}",
            f"Phone: {data.get('phone', '')}",
            f"Company: {data.get('company', '')}",
            f"Address: {data.get('address', '')}",
            f"Country: {data.get('country', '')}",
            f"Port of Discharge: {data.get('port', '')}",
            f"Requested Product(s): {data.get('product', '')}",
            "",
            "Additional Information:",
            data.get("message", ""),
        ]

        msg = Message(
            subject=subject,
            recipients=[app.config["RECIPIENT_EMAIL"]],
            body="\n".join(body_lines),
        )
        mail.send(msg)

        return jsonify({"success": True})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

