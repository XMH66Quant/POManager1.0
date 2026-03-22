from flask import Flask, render_template, request
from pathlib import Path
import json
import pandas as pd

from Parser import parse_pdf_to_json

app = Flask(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

AI_MODELS = ["gemini-2.5-flash"]


@app.route("/", methods=["GET", "POST"])
def index():

    json_output = None
    csv_data = None
    error = None

    if request.method == "POST":

        ai_model = request.form.get("ai_model")
        api_key = request.form.get("api_key")

        if not api_key:
            return render_template("index.html", models=AI_MODELS, error="API key is required")

        files = request.files.getlist("file")

        if not files or files[0].filename == "":
            return render_template("index.html", models=AI_MODELS, error="Please upload at least one PDF")

        all_json = []
        all_rows = []

        for pdf in files:
            input_path = UPLOAD_DIR / pdf.filename
            pdf.save(input_path)

            json_string = parse_pdf_to_json(
                pdf_path=input_path,
                ai_model=ai_model,
                api_key=api_key
            )

            data = json.loads(json_string)
            all_json.append(data)

            # Flatten for CSV
            for item in data["items"]:
                row = {
                    "source_file": pdf.filename,  # ⭐ important for multi-file
                    **data["client"],
                    **data["order_info"],
                    **item
                }
                all_rows.append(row)

        # JSON output (list of documents)
        json_output = json.dumps(all_json, indent=2)

        # CSV output
        df = pd.DataFrame(all_rows)
        csv_data = df.to_dict(orient="records")

    return render_template(
        "index.html",
        models=AI_MODELS,
        json_output=json_output,
        csv_data=csv_data,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)