import kagglehub
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def download_dataset():
    print("Downloading dataset from Kaggle Hub...")
    try:
        # Download the dataset
        path = kagglehub.dataset_download("rupakroy/online-payments-fraud-detection-dataset")
        print(f"Dataset downloaded to: {path}")
        
        # Find the CSV file in the downloaded directory
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.csv'):
                    csv_path = os.path.join(root, file)
                    print(f"Found CSV file: {csv_path}")
                    return csv_path
        raise FileNotFoundError("CSV file not found in downloaded dataset")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None

def load_and_preprocess(csv_path):
    print("\nLoading and preprocessing data...")
    df = pd.read_csv(csv_path)
    
    # Basic preprocessing
    df = df.drop(['nameOrig', 'nameDest', 'isFlaggedFraud'], axis=1)
    
    # Convert categorical 'type' to numerical
    df['type'] = df['type'].map({
        'CASH_OUT': 0,
        'TRANSFER': 1,
        'PAYMENT': 2,
        'CASH_IN': 3,
        'DEBIT': 4,
        'PAYMENT': 5
    }).fillna(0).astype(int)
    
    # Create transaction amount feature
    df['actualAmount'] = df['oldbalanceOrg'] - df['newbalanceOrig']
    
    return df

def train_and_save_model(df):
    print("\nTraining model...")
    X = df.drop('isFraud', axis=1)
    y = df['isFraud']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    print("\nModel Evaluation:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    joblib.dump(model, 'fraud_model.joblib')
    print("\nModel saved as 'fraud_model.joblib'")
    
    return model

if __name__ == "__main__":
    csv_path = download_dataset()
    if csv_path:
        df = load_and_preprocess(csv_path)
        train_and_save_model(df)