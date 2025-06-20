import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("Imported")
"""Load dataset"""

df = pd.read_csv("Data.csv")  # Change to your dataset file

"""Preprocessing"""

# Automatically detect non-numeric (categorical) columns
categorical_cols = df.select_dtypes(include=['object', 'category']).columns

# Label encode categorical columns (incl. target if needed)
le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

# Assume last column is the target (you can change this)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Optional: normalize numerical features
scaler = StandardScaler()
X = scaler.fit_transform(X)

"""Handling missing values"""

# Make sure X is a DataFrame
if not isinstance(X, pd.DataFrame):
    X = pd.DataFrame(X)

# --- Numerical columns ---
num_cols = X.select_dtypes(include=['int64', 'float64']).columns
if len(num_cols) > 0:
    num_imputer = SimpleImputer(strategy='mean')
    X[num_cols] = num_imputer.fit_transform(X[num_cols])

# --- Categorical columns ---
cat_cols = X.select_dtypes(include=['object', 'category']).columns
if len(cat_cols) > 0:
    cat_imputer = SimpleImputer(strategy='most_frequent')
    X[cat_cols] = cat_imputer.fit_transform(X[cat_cols])

"""Dataset Info"""

print("\nDataset Info:\n")
print(df.info())

"""Train and test data"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = GaussianNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))