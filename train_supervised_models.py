import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, auc, classification_report, ConfusionMatrixDisplay
import pickle


# Charger le dataset
print("Chargement des données...")
df = pd.read_csv(r"C:\Users\CYTech Student\projet\big data\Big-Data\fichier\transaction_dataset.csv")  # adapte le chemin si besoin

df = df.iloc[:,2:]
categories = df.select_dtypes('O').columns.astype('category')
df[categories]
numericals = df.select_dtypes(include=['float','int']).columns
df.drop(df[categories], axis=1, inplace=True)

# Nettoyage de colonnes vides
df.fillna(df.median(), inplace=True)
no_var = df.var() == 0
df.drop(df.var()[no_var].index, axis = 1, inplace = True)

# Supprimer les valeurs manquantes sur FLAG
df = df.dropna(subset=["FLAG"])

# Créer les features et la target
features = [
        'Avg min between sent tnx', 'Avg min between received tnx',
        'Time Diff between first and last (Mins)', 'Sent tnx', 'Received Tnx',
        'Number of Created Contracts', 'max value received ',
        'avg val received', 'avg val sent',
        'total Ether sent', 'total ether balance',
        ' ERC20 total Ether received', ' ERC20 total ether sent',
        ' ERC20 total Ether sent contract', ' ERC20 uniq sent addr',
        ' ERC20 uniq rec token name'
]


X = df[features].fillna(0)
y = df["FLAG"]

# Créer un train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Normalize the training features
norm = PowerTransformer()
norm_train_f = norm.fit_transform(X_train)
norm_df = pd.DataFrame(norm_train_f, columns=X_train.columns)

oversample = SMOTE()
print(f'Shape of the training before SMOTE: {norm_train_f.shape, y_train.shape}')

x_tr_resample, y_tr_resample = oversample.fit_resample(norm_train_f, y_train)
print(f'Shape of the training after SMOTE: {x_tr_resample.shape, y_tr_resample.shape}')


# Target distribution before SMOTE
non_fraud = 0
fraud = 0

for i in y_train:
  if i == 0:
    non_fraud +=1
  else:
    fraud +=1

# Target distribution after SMOTE
no = 0
yes = 1

for j in y_tr_resample:
  if j == 0:
    no +=1
  else:
    yes +=1



# Initialiser les modèles
log_model = LogisticRegression(max_iter=1000, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=123, colsample_bytree=0.7, learning_rate=0.5, max_depth=4, n_estimators=200, subsample=0.9)


models = {
    "logistic_model.pkl": log_model,
    "random_forest_model.pkl": rf_model,
    "xgb_model.pkl": xgb_model
}

# Entraînement, évaluation et sauvegarde
for filename, model in models.items():
    print(f"\n=== Entraînement de {filename} ===")
    model.fit(x_tr_resample, y_tr_resample)
    y_pred = model.predict(norm.transform(X_test))  # Attention : X_test doit être normalisé

    print(classification_report(y_test, y_pred))

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.title(f"Matrice de confusion - {filename}")
    plt.savefig(f"models_ml/conf_matrix_{filename.replace('.pkl', '')}.png")
    plt.clf()

    # Sauvegarde du modèle
    with open(f"models_ml/{filename}", "wb") as f:
        pickle.dump(model, f)

print("\n\u2705 Modèles entraînés et enregistrés avec succès dans le dossier 'models_ml/'")
