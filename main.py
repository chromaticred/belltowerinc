from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    try:
        file = request.files['excel_file']
        sheet_name = request.form['sheet_name']

        df = pd.read_excel(file, sheet_name=sheet_name)
        original_order = df.columns.tolist()
        print(df.head())

        df.fillna('', inplace=True)

        # Convert the DataFrame to a list of dictionaries
        print(df.columns.tolist())
        data = df.to_dict(orient='records')
        response = {
            "data": data,
            "columns": original_order
        }
        return jsonify(response)
    except ValueError as e:
        error_message = f"Sheet '{sheet_name}' not found in the Excel file."
        return jsonify({"error": error_message}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
