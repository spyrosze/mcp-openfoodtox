import pandas as pd
import sqlite3 as sql

xls = pd.ExcelFile("data/source/OpenFoodToxTX22809_2023.xlsx")
dictionary = pd.read_excel(xls, "Dictionary")
synonym = pd.read_excel(xls, "COM_SYNONYM")
opinion = pd.read_excel(xls, "OPINION")
component = pd.read_excel(xls, "COMPONENT")
study = pd.read_excel(xls, "STUDY")
chem_assess = pd.read_excel(xls, "CHEM_ASSESS")
question = pd.read_excel(xls, "QUESTION")
genotox = pd.read_excel(xls, "GENOTOX")
endpoint_study = pd.read_excel(xls, "ENDPOINTSTUDY")


# result = synonym[synonym['DESCRIPTION'].str.contains('vitamin', na=False)]['SUB_COM_ID']
def create_db():
    try:
        conn = sql.connect("database/openfoodtox.db")

        # Write dataframes to SQLite tables
        dictionary.to_sql("dictionary", conn, if_exists="replace", index=False)
        synonym.to_sql("synonym", conn, if_exists="replace", index=False)
        opinion.to_sql("opinion", conn, if_exists="replace", index=False)
        component.to_sql("component", conn, if_exists="replace", index=False)
        study.to_sql("study", conn, if_exists="replace", index=False)
        chem_assess.to_sql("chem_assess", conn, if_exists="replace", index=False)
        question.to_sql("question", conn, if_exists="replace", index=False)
        genotox.to_sql("genotox", conn, if_exists="replace", index=False)
        endpoint_study.to_sql("endpoint_study", conn, if_exists="replace", index=False)

        conn.commit()
        print("Database created successfully at database/openfoodtox.db")
        print(
            f"Tables created: dictionary, synonym, opinion, component, study, chem_assess, question, genotox, endpoint_study"
        )
    except sql.Error as e:
        print(f"Error creating database: {e}")
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    create_db()
