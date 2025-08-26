from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:8000"}})

# Load model at startup
try:
    model = joblib.load('fraud_model.joblib')
    print("Model loaded successfully")
except Exception as e:
    model = None
    print(f"Model not available: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.json

    # Required fields
    required_fields = ['type', 'amount', 'oldbalanceOrg', 'newbalanceOrig',
                       'oldbalanceDest', 'newbalanceDest']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        amount = float(data['amount'])
        oldbalanceOrg = float(data['oldbalanceOrg'])
        newbalanceOrig = float(data['newbalanceOrig'])
        oldbalanceDest = float(data['oldbalanceDest'])
        newbalanceDest = float(data['newbalanceDest'])

        # Verify sender balance
        sender_diff = oldbalanceOrg - newbalanceOrig
        receiver_diff = newbalanceDest - oldbalanceDest

        is_amount_verified = abs(sender_diff - amount) < 0.01 and abs(receiver_diff - amount) < 0.01

        # If amount mismatch, mark as fraud regardless of model
        if not is_amount_verified:
            return jsonify({
                'prediction': 1,
                'isFraud': True,
                'fraudProbability': 100.0,
                'safeProbability': 0.0,
                'confidence': 100.0,
                'ruleBasedFlag': True,
                'reason': 'Amount mismatch between sender and receiver'
            })

        # Convert type to numerical
        type_mapping = {
            'CASH_OUT': 0,
            'TRANSFER': 1,
            'PAYMENT': 2,
            'CASH_IN': 3,
            'DEBIT': 4
        }

        trans_type = data['type'].upper()
        if trans_type not in type_mapping:
            return jsonify({'error': 'Invalid transaction type'}), 400

        transaction = pd.DataFrame([{
            'step': 1,
            'type': type_mapping[trans_type],
            'amount': amount,
            'oldbalanceOrg': oldbalanceOrg,
            'newbalanceOrig': newbalanceOrig,
            'oldbalanceDest': oldbalanceDest,
            'newbalanceDest': newbalanceDest,
            'actualAmount': sender_diff
        }])

        cols = ['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig',
                'oldbalanceDest', 'newbalanceDest', 'actualAmount']
        transaction = transaction[cols]

        # Use model only if available
        if model:
            prediction = model.predict(transaction)
            proba = model.predict_proba(transaction)
            fraud_prob = float(proba[0][1]) * 100
            safe_prob = float(proba[0][0]) * 100
            confidence = float(np.max(proba[0])) * 100
            is_fraud = bool(prediction[0])
            rule_based_flag = False
        else:
            # Fallback simple logic
            is_fraud = amount > 100000  # Example: Flag large transactions
            fraud_prob = 95.0 if is_fraud else 5.0
            safe_prob = 100 - fraud_prob
            confidence = max(fraud_prob, safe_prob)
            rule_based_flag = True

        return jsonify({
            'prediction': int(is_fraud),
            'isFraud': is_fraud,
            'fraudProbability': fraud_prob,
            'safeProbability': safe_prob,
            'confidence': confidence,
            'ruleBasedFlag': rule_based_flag,
            'amountVerified': is_amount_verified
        })

    except ValueError as ve:
        return jsonify({'error': f'Invalid input value: {ve}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)