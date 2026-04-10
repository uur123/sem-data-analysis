import streamlit as st
import pandas as pd

st.set_page_config(page_title="ENLab Data Analysis", layout="wide")
st.header("ENLab Aspex Data Analysis")

uploaded_files = st.file_uploader("Upload files", type=["csv", "pxz"], accept_multiple_files=True)

if uploaded_files:
    result_data = []
    
    fields = [
        'PART#', 'FIELD#', 'MAGFIELD#', 'X_ABS', 'Y_ABS', 'X_CG', 'Y_CG', 'X_FERET','Y_FERET', 
        'DAVE', 'DMAX', 'DMIN', 'DPERP', 'ASPECT', 'AREA', 'PERIMETER','ORIENTATION', 'MAG', 
        'MAG_INDEX', 'ACTION', 'FIRST_ELEM', 'SECOND_ELEM', 'THIRD_ELEM', 'FOURTH_ELEM', 
        'FIRST_CONC', 'SECOND_CONC', 'THIRD_CONC', 'FOURTH_CONC', 'FIRST_PCT', 'SECOND_PCT', 
        'THIRD_PCT', 'FOURTH_PCT', 'VIDEO', 'LIVE_TIME', 'COUNTS', 'TYPE(4ET)#', 'DENSITY', 
        'PSEM_CLASS', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Mn', 'Fe', 'Ni', 'Cu'
    ]

    for file in uploaded_files:
        # FIX: Changed 'delim_whitespace=True' to 'sep=r"\s+"' for modern pandas
        df = pd.read_csv(file, names=fields, header=None, sep=r"\s+", engine='python')
        
        # Mapping numeric codes to Class Names
        mapping = {
            10: 'Al 75', 7: 'Al 50 Si 5',
            5: 'Al 50 Fe 5', 9: 'Al 50 Oth 5',
            6: 'Al 50 Cu 5', 4: 'Al 50 Mn 5',
            11: 'MgO 10', 1: 'NaCl 10',
            2: 'Cu Si 10', 8: 'Si Mn Fe 10', 3: 'Cu 10',
            0: '{Unclassified}', 12: '{Unclassified}'
        }
        df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(mapping)

        # --- FILTRATION LOGIC ---
        pore_classes = ['Al 75', 'Al 50 Si 5']
        total_pores = len(df[df['PSEM_CLASS'].isin(pore_classes)])

        oxide_classes = ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5']
        total_oxides = len(df[df['PSEM_CLASS'].isin(oxide_classes)])

        other_classes = ['MgO 10', 'NaCl 10', 'Cu Si 10', 'Si Mn Fe 10', 'Cu 10']
        total_others = len(df[df['PSEM_CLASS'].isin(other_classes)])

        result_data.append({
            "File name": file.name,
            "Total Pores": total_pores,
            "Total Oxides": total_oxides,
            "Total Others": total_others
        })

    if result_data:
        summary_df = pd.DataFrame(result_data)
        st.write("### Analysis Results")
        st.dataframe(summary_df)
        
        st.write("### Inclusion Comparison Graph")
        st.bar_chart(summary_df.set_index("File name"))
