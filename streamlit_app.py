import streamlit as st
import pandas as pd

st.set_page_config(page_title="ENLab Analysis", layout="wide")
st.header("ENLab Inclusion Analysis Report")

uploaded_files = st.file_uploader("Upload Aspex files", type=["csv", "pxz"], accept_multiple_files=True)

if uploaded_files:
    # We will collect data in a dictionary where keys are Filenames
    report_dict = {}
    
    fields = [
        'PART#', 'FIELD#', 'MAGFIELD#', 'X_ABS', 'Y_ABS', 'X_CG', 'Y_CG', 'X_FERET','Y_FERET', 
        'DAVE', 'DMAX', 'DMIN', 'DPERP', 'ASPECT', 'AREA', 'PERIMETER','ORIENTATION', 'MAG', 
        'MAG_INDEX', 'ACTION', 'FIRST_ELEM', 'SECOND_ELEM', 'THIRD_ELEM', 'FOURTH_ELEM', 
        'FIRST_CONC', 'SECOND_CONC', 'THIRD_CONC', 'FOURTH_CONC', 'FIRST_PCT', 'SECOND_PCT', 
        'THIRD_PCT', 'FOURTH_PCT', 'VIDEO', 'LIVE_TIME', 'COUNTS', 'TYPE(4ET)#', 'DENSITY', 
        'PSEM_CLASS', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Mn', 'Fe', 'Ni', 'Cu'
    ]

    for file in uploaded_files:
        df = pd.read_csv(file, names=fields, header=None, sep=r"\s+", engine='python')
        
        mapping = {
            10: 'Al 75', 7: 'Al 50 Si 5',
            5: 'Al 50 Fe 5', 9: 'Al 50 Oth 5', 6: 'Al 50 Cu 5', 4: 'Al 50 Mn 5',
            11: 'MgO 10', 1: 'NaCl 10', 2: 'Cu Si 10', 8: 'Si Mn Fe 10', 3: 'Cu 10',
            0: '{Unclassified}', 12: '{Unclassified}'
        }
        df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(mapping)

        def get_metrics(data, classes):
            sub = data[data['PSEM_CLASS'].isin(classes)]
            m5_15 = len(sub[sub['DAVE'].between(5, 14.99)])
            m15_30 = len(sub[sub['DAVE'].between(15, 29.99)])
            m30_75 = len(sub[sub['DAVE'].between(30, 74.99)])
            m75 = len(sub[sub['DAVE'] >= 75])
            return [m5_15 + m15_30 + m30_75 + m75, m5_15, m15_30, m30_75, m75]

        p = get_metrics(df, ['Al 75', 'Al 50 Si 5'])
        o = get_metrics(df, ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5'])
        i = get_metrics(df, ['MgO 10', 'NaCl 10', 'Cu Si 10', 'Si Mn Fe 10', 'Cu 10'])

        # Store in dictionary with specific row names
        report_dict[file.name] = [
            p[0], p[1], p[2], p[3], p[4],
            o[0], o[1], o[2], o[3], o[4],
            i[0], i[1], i[2], i[3], i[4]
        ]

    # --- CREATE THE TRANSPOSED TABLE ---
    row_names = [
        "Total pores", "Number of Pores (5 to 15um)", "Number of Pores (15 to 30um)", "Number of Pores (30 to 75um)", "Number of Pores (>75um)",
        "Total Oxides", "Oxides (5 to 15um)", "Oxides (15 to 30um)", "Oxides (30 to 75um)", "Oxides (>75um)",
        "Total Other Inclusions", "Other Inclusions (5 to 15um)", "Other Inclusions (15 to 30um)", "Other Inclusions (30 to 75um)", "Other Inclusions (>75um)"
    ]
    
    final_table = pd.DataFrame(report_dict, index=row_names)
    st.write("### Summary Report Table")
    st.table(final_table) # Using st.table for the static "printed" look

    # --- 3 GRAPHS ---
    # Convert dictionary back to a format easy for plotting
    plot_df = final_table.T.reset_index().rename(columns={'index': 'File'})

    st.subheader("Graph 1: Pores Size Distribution")
    st.bar_chart(plot_df.set_index("File")[row_names[1:5]])

    st.subheader("Graph 2: Oxides Size Distribution")
    st.bar_chart(plot_df.set_index("File")[row_names[6:10]])

    st.subheader("Graph 3: Other Inclusions Size Distribution")
    st.bar_chart(plot_df.set_index("File")[row_names[11:15]])

else:
    st.info("Please upload your Aspex files.")
