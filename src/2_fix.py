# Bereinigen der Daten 

import pandas as pd
import re

def process_data(input_path="data/extrahierte_daten.csv"):

    df = pd.read_csv(input_path, encoding="utf-8")

    #--------------Herkunft------------------------------------
    herkunft_dict = {
        "el-Lahun (Illahun), Siedlung": "el-Lahun",
        "Tal der Könige (Biban el-Muluk)": "Tal der Könige",
        "Karnak, Chonstempel, südöstlich des Karnaktempels": "Karnak",
        "Deir el-Bahari, Mentuhotep-Tempel": "Deir el-Bahari",
        "(the inv_no is collective)": "Tebtynis",
        "aus den Grabungen von W.M.F. Petrie in Kom Medinet Ghurab (Fischer-Elfert, in: JEA 84, 1998, 87)": "Gurob",
        "Papyrus, bestehend aus ca. 200 Fragmenten v.a. aus Kopenhagen (P. Carlsberg inv. 205) sowie in Florenz, Kairo, Michigan, Oxford, Yale": "Tebtynis",
        "(unbestimmt); Ro: Rede des Sachmetpriesters Renseneb": "unbestimmt",
        "Saqqara, Nekropolen": "Saqqara"
    }

    df = df[~df['Herkunft'].str.contains("Mann", na=False)]

    df['Herkunft'] = (
        df['Herkunft']
        .astype(str)
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.replace(r'^Tebtynis Temple Library.*$', 'Tebtynis Temple Library', regex=True)
        .str.replace(r'^Tebtynis Tempelbibliothek.*$', 'Tebtynis Temple Library', regex=True)
        .replace(herkunft_dict)
    )

    def clean_herkunft(text):
        if pd.isna(text):
            return ""
        return re.sub(r'[^A-Za-zÄÖÜäöüß,\s\-]', '', str(text))

    df['Herkunft'] = df['Herkunft'].apply(clean_herkunft)

    herkunft_counts = df['Herkunft'].value_counts().reset_index()
    herkunft_counts.columns = ['Herkunft', 'Anzahl']
    herkunft_counts.to_csv("data/herkunft_haeufigkeiten_herkunft.csv", index=False, encoding="utf-8-sig")




    #--------------Datierung------------------------------------

    df['Datierung'] = (
        df["Datierung"]
        .str.replace(r'^AD 100 - 150.*$', 'AD 100 - 150', regex=True)
        .str.replace(r'^AD 75 - 125.*$', 'AD 75 - 125', regex=True)
        .str.replace(r'^Merenptah.*$', 'Merenptah', regex=True)
        .str.replace(r'^.*Re-Harachte.*$', 'Re-Harachte', regex=True)
        .str.replace(r'^Ramses II\..*$', 'Ramses II.', regex=True)
        .str.replace(r'^Sethos II\..*$', 'Sethos II.', regex=True)
    )

    datierung_dict = {
        "1. Hälfte 2. Jhdt. n.Chr.": "200-250 n. Chr.",
        "1. Jhdt. n.Chr.": "1-100 n. Chr.",
        "1. Jhdt. v.Chr.": "1-100 v. Chr.",
        "1. Viertel 2. Jhdt. n.Chr.": "200-225 n. Chr.",
        "2. Jh. n. Chr., 150-200 (Quack)": "150-200 n. Chr. ",
        "2. Jhdt. n.Chr.": "101-200 n. Chr",
        "2. Jhdt. v.Chr.": "101-200 v. Chr.",
        "2. Viertel 2. Jhdt. n.Chr.": "200-225 n. Chr.",
        "18.-19. Dyn.":"18. Dyn. - 19. Dyn.",
        "18.Dyn.": "18. Dyn.",
        "19. Dyn.  (Quack: 18. Dyn., mdl. Auskunft)": "19. Dyn.",
        "19.-20. Dyn.": "19. Dyn. - 20. Dyn.",
        "20. Dyn. - 21. Dyn.  (Quack: 20. Dyn.)": "19. Dyn.",
        "4. Viertel 6. Jhdt. v.Chr.":"27. Dynastie",
        "AD 1 - 150": "1-150 n. Chr.",
        "AD 1 - 199": "100-150 n. Chr.",
        "AD 100 - 150": "100-150 n. Chr.",
        "AD 100-199, auf der Rückseite eines lateinischen Texts (zweites Exemplar: der unpublizierte P. Carlsberg inv. 671)": "100-199 n. Chr.",
        "AD 105 - 150": "105-150 v. Chr.",
        "AD 50 - 150?": "50-150 n. Chr.",
        "AD 75 - 125": "75-125 n. Chr.",
        "Amenemhet III.": "18. Dynastie",
        "Amenhotep II., Re, Götterneunheit, Meer": "18.-19. Dynastie",
        "Amenmesse - Sethos II.": "19. Dynastie",
        "Amenophis I. (lt. Blumenthal)": "18. Dynastie",
        "frühes 2. Jh. n. Chr.": "200-225 n. Chr.",
        "Makedonen, Ptolemäer": "Hellenistische Zeit",
        "Merenptah": "19. Dynastie",
        "Re-Harachte": "19. Dynastie",
        "Psammetich I.": "26. Dynastie",
        "ptol. oder röm.": "Griechisch-römische Zeit",
        "Ramses II.": "19. Dynastie",
        "Ramses III.": "20. Dynastie",
        "Ramses III. - Ramses VI.": "20. Dynastie",
        "Ramses VI.": "19.-20. Dynastie",
        "Ramses IV.": "20. Dynastie",
        "römisch?": "Römische Zeit",
        "Sethos II.": "19. Dynastie",
        "Thutmosis III. (Gesamtzeitraum)": "19. Dynastie",
        "Thutmosis IV. - Amenophis III.": "18.Dynastie",
    }

    df['Datierung'] = (
        df['Datierung']
        .replace(datierung_dict)
        .str.replace("Dynastie", "Dyn.", regex=False)
    )

    df = df[~df['Datierung'].str.contains("efer", na=False)]

    df[['Datierung']].drop_duplicates().to_csv("data/einzigartige_datierungen.csv", index=False, encoding="utf-8-sig")

    datierung_counts = df['Datierung'].value_counts().reset_index()
    datierung_counts.columns = ['Datierung', 'Anzahl']
    datierung_counts.to_csv("data/datierung_haeufigkeiten.csv", index=False, encoding="utf-8-sig")


    

    #--------------Übersetzung------------------------------------

    def clean_and_normalize(text):
        if pd.isna(text):
            return ""
        text = str(text)
        text = re.sub(r'[^A-Za-zÄÖÜäöüß\s\-]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    df['Übersetzung'] = df['Übersetzung'].apply(clean_and_normalize)
    

    #--------------Epochen------------------------------------

    periode_dict = {
    "12. Dyn.": "Mittleres Reich",
    "12. Dyn. - 13. / 14. Dyn.": "Zweite Zwischenzeit",
    "13. / 14. Dyn.": "Zweite Zwischenzeit",
    "15. / 16. / 17. Dyn.": "Zweite Zwischenzeit",
    "19. Dyn. - 20. Dyn.": "Neues Reich",
    "19. Dyn.": "Neues Reich",
    "18. Dyn.": "Neues Reich",
    "20. Dyn.": "Neues Reich",
    "18. Dyn. - 19. Dyn.": "Neues Reich",
    "Neues Reich": "Neues Reich",
    "19.-20. Dyn.": "Neues Reich",
    "18.Dyn.": "Neues Reich",
    "18.-19. Dyn.": "Neues Reich",
    "21. Dyn. - 22. / 23. Dyn.": "Dritte Zwischenzeit",
    "25. Dyn.": "Dritte Zwischenzeit",
    "21. Dyn.": "Dritte Zwischenzeit",
    "20. Dyn. - 21. Dyn.": "Dritte Zwischenzeit",
    "26. Dyn.": "Spätzeit",
    "25. Dyn. - 26. Dyn.": "Spätzeit",
    "Dritte Zwischenzeit - Spätzeit": "Spätzeit",
    "27. Dyn.": "Spätzeit",
    "30. Dyn.": "Spätzeit",
    "Dritte Zwischenzeit - 26. Dyn.": "Spätzeit",
    "Spätzeit": "Spätzeit",
    "Hellenistische Zeit": "Griechisch-römische Zeit",
    "101-200 n. Chr": "Griechisch-römische Zeit",
    "75-125 n. Chr.": "Griechisch-römische Zeit",
    "römische Zeit": "Griechisch-römische Zeit",
    "200-250 n. Chr.": "Griechisch-römische Zeit",
    "100-150 n. Chr.": "Griechisch-römische Zeit",
    "1-100 v. Chr.": "Griechisch-römische Zeit",
    "200-225 n. Chr.": "Griechisch-römische Zeit",
    "101-200 v. Chr.": "Griechisch-römische Zeit",
    "1-100 n. Chr.": "Griechisch-römische Zeit",
    "100-199 n. Chr.": "Griechisch-römische Zeit",
    "Griechisch-römische Zeit": "Griechisch-römische Zeit",
    "1-150 n. Chr.": "Griechisch-römische Zeit",
    "50-150 n. Chr.": "Griechisch-römische Zeit",
    "150-200 n. Chr. ": "Griechisch-römische Zeit",
    "105-150 v. Chr.": "Griechisch-römische Zeit",
    "Römische Zeit": "Griechisch-römische Zeit",
    "keiner, Kolophon": "Unbekannt",
}

    df["Epoche"] = df["Datierung"].map(periode_dict).fillna("Unbekannt")

    df.to_csv("data/extrahierte_daten_bereinigt.csv", index=False, encoding="utf-8-sig")

    # Nur Übersetzungen 
    # df[['Datei', 'Übersetzung']].to_csv("data/texte.csv", index=False, encoding="utf-8-sig")

    print("Datei erstellt.")

if __name__ == "__main__":
    process_data()
