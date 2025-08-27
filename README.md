# 🛡️ Online Fraud Detection System  

An **AI-powered Fraud Detection System** that identifies suspicious financial transactions in real-time. The system combines a clean frontend interface with a machine learning backend to protect users from financial fraud.  

---

## 📌 Introduction  
Financial fraud causes **billions in losses annually**.  
Our solution provides **automated detection with visual risk indicators**, making AI-powered fraud detection accessible to end-users.  


**Tech Stack:**  
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask (Python)  
- **Machine Learning Model:** Random Forest Classifier  

---

## 🎨 Frontend Demonstration  

### 🔹 Home Page  
- Simple interface with a clear call-to-action  
- Clean design and background image  
<img width="1094" height="632" alt="image" src="https://github.com/user-attachments/assets/a7cb7a68-b87d-45a6-9350-c20bfdd434d8" />
### 🔹 Form Page  
- Users enter transaction details (all fields validated)  
- Dropdown for transaction types  
- Fully responsive design  
<img width="1092" height="619" alt="image" src="https://github.com/user-attachments/assets/a594eb7c-e387-453f-b574-a41adaaf57f2" />

### 🔹 Results Page  
- **Visual risk assessment with color coding:**  
  - 🚨 Fraud case → Red pulse animation  
  - ✅ Safe transaction → Green checkmark  
- Probability meter animation for fraud likelihood  
![Uploading image.png…]()

**Code Highlight:**  
```javascript
// Navigation between pages
function showPage(page) {
  document.querySelectorAll('.page-container').forEach(p => p.style.display = 'none');
  page.style.display = 'block'; 
}

⚙️ Backend Explanation
-API Flow

Frontend sends data to Flask API (/predict)

Backend validates inputs, checks consistency, and applies fraud detection

Rule-Based Checks:

Ensures sender/receiver amounts are consistent before ML inference

Model Prediction:

If model is available → Predict fraud probability

If model not available → Apply fallback rules

Code Highlight:

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Validate inputs
    # 2. Convert amounts
    # 3. Run rule-based checks


Fallback Rule Example:

if not model:
    is_fraud = amount > 100000
    fraud_prob = 95.0 if is_fraud else 5.0

🤖 Machine Learning
Training Process

Dataset: Kaggle financial transactions

Features: Transaction type, amount, balances, etc.

Handling imbalanced data (fraud cases are rare)

Model Choice

Random Forest → Robust for imbalanced datasets, provides probabilities

Code Highlight:

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    class_weight='balanced',
    random_state=42
)

🏗️ System Architecture
User Browser → Frontend → Flask API → ML Model
                ↑              ↑
           (Displays)    (Processes/Rules)

✅ Key Takeaways

Visual interface makes AI insights user-friendly

Defensive programming ensures safety before ML predictions

Modular design → Easy to update/improve models
