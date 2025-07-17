import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from pathlib import Path
from . import create_reports as crep
import pickle

def save_f(filename, object_to_save):
    with open(filename, "wb") as file:
        pickle.dump(object_to_save, file)

def prepare_df(df_name):
    df = pd.read_csv(df_name, sep = '\t', header = None, names = ['label', 'text'])
    df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})
    df = df.dropna(subset=['label_num'])
    return df

def make_model(df): 
    spam_model_path = Path(__file__).parent.parent / "library" / "spam_model.pkl"
    vectorizer_path = Path(__file__).parent.parent / "library" / "vectorizer.pkl"

    X_train, X_test, y_train, y_test = train_test_split(
        df['text'],
        df['label_num'],
        test_size = 0.2,
        random_state = 322
    )

    vectorizer = TfidfVectorizer(
        ngram_range = (1, 2),
        max_df = 0.95,
        sublinear_tf = True
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = RandomForestClassifier(
    n_estimators=100, 
    max_depth=20,      
    random_state=322,   
    class_weight='balanced'  
)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)

    conf_matrix = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)

    spam_mask = (y_test == 1) 
    wrong_pred_mask = (y_pred == 0)  
    combined_mask = spam_mask & wrong_pred_mask  
    unhandled_messages_arr = X_test[combined_mask]

    unhandled_messages = "\n".join(unhandled_messages_arr)

    save_f(spam_model_path, model)
    save_f(vectorizer_path, vectorizer)

    return conf_matrix, report, accuracy, unhandled_messages

def reteach_model():
    df_path = Path(__file__).parent.parent / "Data" / "SMSSpamCollection"
    df = prepare_df(df_path)
    conf_matrix, report, accuracy, unhandled_messages = make_model(df)
    text_report_path = Path(__file__).parent.parent / "Output" / "text_report.txt"
    graphic_report_path = Path(__file__).parent.parent / "Graphics" / "graphic.png"
    model_report_path = Path(__file__).parent.parent / "Output" / "model_report.txt"

    crep.create_text_report(text_report_path, df_path)
    crep.create_graphic_report(graphic_report_path, df_path)
    crep.create_model_report(conf_matrix, report, accuracy, unhandled_messages, model_report_path)

def load_model(model_path, vectorizer_path):    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)
    
    return model, vectorizer