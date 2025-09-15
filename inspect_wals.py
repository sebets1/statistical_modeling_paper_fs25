import pycldf
import pandas as pd


def import_data(file_path):
    ds = pycldf.Dataset.from_metadata(file_path)
    # Load as pandas DataFrames
    languages = pd.DataFrame(ds['LanguageTable'])
    features = pd.DataFrame(ds['ParameterTable'])
    values = pd.DataFrame(ds['ValueTable'])

    print("Languages:")
    print(languages.head())

    print("\nFeatures:")
    print(features.head())

    print("\nValues:")
    print(values.head())

    # Create a language-feature pivot table (matrix)
    feat_matrix = values.pivot_table(
        index='Language_ID',  # rows
        columns='Parameter_ID',  # columns
        values='Value',  # values in the table
        aggfunc='first'  # use first value if there's more than one
    )
    return languages, features, values, feat_matrix


def export_data(languages, features, values, matrix):
    # Export individual tables
    languages.to_csv('data/languages.csv', index=False)
    features.to_csv('data/features.csv', index=False)
    values.to_csv('data/values.csv', index=False)
    # Export matrix to CSV
    matrix.to_csv('data/language_feature_matrix.csv')
    print("✅ Export complete: languages.csv, features.csv, values.csv, language_feature_matrix.csv")


def reduce_matrix(matrix, lang_dict):
    feat_counts = []
    for feature_id, col_values in matrix.items():
        count = col_values.notna().sum()
        feat_counts.append([int(count), feature_id])


    feat_counts.sort(reverse=True)
    chosen_feats = []
    for ele in feat_counts[1:41]:
        chosen_feats.append(ele[1])

    lang_counts = []
    for lang_id, row in matrix.iterrows():
        lang_count = 0
        for feat in chosen_feats:
           # print(row[feat])
            if str(row[feat]) != "nan" :
                lang_count += 1
        lang_name = lang_dict.get(lang_id, lang_id)  # fallback to ID if name missing
        lang_name = row["Language_ID"]
        lang_counts.append([lang_count, lang_name])

    lang_counts = sorted(lang_counts, key=lambda x: x[0], reverse=True)
    #lang_counts.sort(reverse=True)
    print(lang_counts[:30])
    for count, name in lang_counts[:10]:
        print(f"{name}: {count} features filled")

    print(matrix.index[:5])
    print(matrix.head())
    print(languages.columns)
    print(languages[['ID', 'Name']].head())


#####################################################################################################
if __name__ == "__main__":
    # lang, feat, values, matrix = import_data('../wals/cldf/StructureDataset-metadata.json')
    # export_data(lang, feat, values, matrix)

    feat_matrix = pd.read_csv('data/language_feature_matrix.csv')
    languages = pd.read_csv("data/languages.csv")
    # Create a lookup dictionary: {Language_ID: Language_Name}
    id_to_name = dict(zip(languages['ID'], languages['Name']))

    reduce_matrix(feat_matrix, id_to_name)