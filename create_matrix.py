import pandas as pd

def create_matrix(in_file, out_file, lang_list, params):
    """
    Convert a language-feature matrix to a pairwise distance matrix.
    """
    min_feat, min_langs, selected_feat = params
    df = pd.read_csv(in_file, sep=",", encoding="utf-8")

    if selected_feat != "all":
        df = choose_features(df, selected_feat)

    # reduce matrix to chosen languages, get rid of languages and features with too little values
    selection = df.loc[df["Language_ID"].isin(lang_list)]
    selection = selection[selection.notna().sum(axis=1) > min_feat]
    selection = selection.loc[:, selection.notna().sum(axis=0) >= min_langs]

    # calculate pairwise distance matrix with Hamming distance
    selection_list = selection.values.tolist()
    no_langs = len(selection_list)
    header = ["lang"]
    dist_matrix = []
    for lang in selection_list:
        header.append(lang[0])
        lang_count = [lang[0]]
        for i in range(no_langs):
            feat_tot = 0
            feat_same = 0
            for feat, ele in enumerate(lang):
                other_lang = selection_list[i][feat]
                if pd.notna(ele) and pd.notna(other_lang):
                    feat_tot += 1
                    if ele == other_lang:
                        feat_same += 1
            lang_count.append(1-(feat_same/feat_tot))
            print(f"{lang[0]}-{selection_list[i][0]}: feat_tot={feat_tot}, feat_same={feat_same}")

        dist_matrix.append(lang_count)
    dist_matrix.insert(0, header)

    # print output to terminal
    print("\nPairwise distance matrix:\n")
    for row in dist_matrix:
        row = [str(round(n, 2)) if isinstance(n, (int, float)) else str(n) for n in row]
        print("\t".join(row))

    # save output to file
    with open(out_file, "w", encoding="utf-8") as f:
        for row in dist_matrix:
            row = [str(n) for n in row]
            f.write("\t".join(row))
            f.write("\n")
    print(f"\nMatrix saved to {out_file}.")


def language_selection(file, column_name, column_values):
    df = pd.read_csv(file, sep=",", encoding="utf-8")

    lang_select = df.loc[df[column_name].isin(column_values), "ID"].tolist()
    return lang_select


def choose_features(feat_df, selected_feat):
    if selected_feat == "phonology":
        feat_range = [(1, 19)]
    if selected_feat == "morphology":
        feat_range = [(20, 57), (65, 80)]
    if selected_feat == "syntax":
        feat_range = [(58, 64), (81, 128), (143, 144)]

    def check_if_feature_in_category(feat_no):
        num = int(feat_no[:-1])
        return any(start <= num <= end for start, end in feat_range)


    feat_df = feat_df[["Language_ID"] + [col for col in feat_df.columns[1:] if check_if_feature_in_category(col)]]
    return feat_df


######################################################################################
if __name__ == "__main__":
    features_file = "data/language_feature_matrix.csv"
    lang_file = "data/languages.csv"
    output_matrix_file = "matrices/Rom_syntax.txt"


    all_features = False

    if all_features:
        # define languages
        lang_subclass = ["Family", "Genus"]
        families = ["Pama-Nyungan", "Indo-European", "Austronesian"]
        genus = ["Romance", "Germanic", "Slavic"]

        # define parameters for matrix creation
        min_features = 50 # how many non-zero values in the lang-feat matrix for a lang to be considered
        min_lang_for_feature = 3 # from the language selection, how many languages do at least need to have the feature for it to be considered?
        selected_features = "all"

        ###########################################################
        parameters = [min_features, min_lang_for_feature, selected_features]

        lang_list = language_selection(lang_file, column_name=lang_subclass[1], column_values=genus[2:])
        create_matrix(features_file, output_matrix_file, lang_list, parameters)
        ###########################################################

    else:
        # define languages
        lang_family = "Ger"

        # define parameters for matrix creation
        min_features = 1
        min_lang_for_feature = 1
        selected_features = "phonology"

        ###########################################################
        if lang_family == "Rom":
            languages = ["spa", "por", "ita", "rom", "ctl", "fre"]

        if lang_family == "Ger":
            languages = ["dsh", "dut", "eng", "ger", "ice", "nor", "swe"]

        if lang_family == "Slav":
            languages = ["bul",	"cze", "pol", "rus", "scr", "ukr"]

        output_matrix_file = f"matrices/{lang_family}_{selected_features}.txt"

        parameters = [min_features, min_lang_for_feature, selected_features]

        create_matrix(features_file, output_matrix_file, languages, parameters)