from flask import Flask, request, render_template
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('model_placement_prediction')

# Initialize Flask app
app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the form
        cgpa = float(request.form['cgpa'])
        project_score = float(request.form['project_score'])
        internships = int(request.form['internships'])
        extracurricular_score = float(request.form['extracurricular_score'])
        total_score = float(request.form['total_score'])
        department = int(request.form['department'])
        field = int(request.form['field'])
        
        # Create a DataFrame for the input
        new_data = pd.DataFrame({
            'cgpa': [cgpa],
            'project_score': [project_score],
            'internships': [internships],
            'extracurricular_score': [extracurricular_score],
            'total_score': [total_score],
            'department': [department],
            'field': [field],
        })
        
        # Make prediction
        prediction = model.predict(new_data)[0]
        probability = model.predict_proba(new_data)[0]
        
        # Map prediction to outcome
        outcome_map = {0: "Selected", 1: "Rejected", 2: "No Offer"}
        result = outcome_map[prediction]
        
        return render_template(
            'index.html',
            prediction=result,
            probability=round(probability[prediction] * 100, 2)
        )
    except Exception as e:
        return render_template('index.html', error=str(e))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)