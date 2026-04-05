import os
import sys

from flask import Flask, request, render_template
import numpy as np
import pandas as pd

# Ensure src/ is discoverable
sys.path.append(os.path.abspath("."))

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Flask app
application = Flask(__name__)
app = application


# Home route
@app.route('/')
def index():
    return render_template('index.html')


# Prediction route
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')

    try:
        # Collect form data
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )

        # Convert to DataFrame
        pred_df = data.get_data_as_data_frame()
        print("Input DataFrame:\n", pred_df)

        # Prediction pipeline
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        print("Prediction result:", results)

        return render_template('home.html', results=results[0])

    except Exception as e:
        # Return error clearly (very useful on Render logs)
        return f"Error occurred: {str(e)}"


# Local run (Render uses gunicorn, not this block)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)