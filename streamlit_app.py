import streamlit as st
import pandas as pd

st.set_page_config(page_title="ENLab Data Analysis", layout="wide")
st.header("ENLab Aspex Data Analysis")

uploaded_files = st.file_uploader("Upload files", type=["csv", "pxz"], accept_multiple_files=True)

if uploaded_files:
    result_data = []
    
    # Define the columns based on your logic
    fields = [
        'PART#', 'FIELD#', 'MAGFIELD#', 'X_ABS', 'Y_ABS', 'X_CG', 'Y_CG', 'X_FERET','Y_FERET', 
        'DAVE', 'DMAX', 'DMIN', 'DPERP', 'ASPECT', 'AREA', 'PERIMETER','ORIENTATION', 'MAG', 
        'MAG_INDEX', 'ACTION', 'FIRST_ELEM', 'SECOND_ELEM', 'THIRD_ELEM', 'FOURTH_ELEM', 
        'FIRST_CONC', 'SECOND_CONC', 'THIRD_CONC', 'FOURTH_CONC', 'FIRST_PCT', 'SECOND_PCT', 
        'THIRD_PCT', 'FOURTH_PCT', 'VIDEO', 'LIVE_TIME', 'COUNTS', 'TYPE(4ET)#', 'DENSITY', 
        'PSEM_CLASS', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Mn', 'Fe', 'Ni', 'Cu'
    ]

    for file in uploaded_files:
        # Read using whitespace delimiter as per your logic
        df = pd.read_csv(file, names=fields, header=None, delim_whitespace=True)
        
        # Mapping numeric codes to Class Names
        mapping = {
            10: 'Al 75', 7: 'Al 50 Si 5',            # Pores
            5: 'Al 50 Fe 5', 9: 'Al 50 Oth 5',      # Oxides
            6: 'Al 50 Cu 5', 4: 'Al 50 Mn 5',       # Oxides
            11: 'MgO 10', 1: 'NaCl 10',             # Others
            2: 'Cu Si 10', 8: 'Si Mn Fe 10', 3: 'Cu 10', # Others
            0: '{Unclassified}', 12: '{Unclassified}'
        }
        df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(mapping)

        # --- FILTRATION LOGIC ---
        # Pores
        pore_classes = ['Al 75', 'Al 50 Si 5']
        total_05_15 = len(df[df['PSEM_CLASS'].isin(pore_classes) & (df["DAVE"].between(0.5, 14.99))])
        total_15_30 = len(df[df['PSEM_CLASS'].isin(pore_classes) & (df["DAVE"].between(15, 29.99))])
        total_30_75 = len(df[df['PSEM_CLASS'].isin(pore_classes) & (df["DAVE"].between(30, 74.99))])
        total_75    = len(df[df['PSEM_CLASS'].isin(pore_classes) & (df["DAVE"] >= 75)])

        # Oxides
        oxide_classes = ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5']
        total_AlO_05_15 = len(df[df['PSEM_CLASS'].isin(oxide_classes) & (df["DAVE"].between(0.5, 14.99))])
        total_AlO_15_30 = len(df[df['PSEM_CLASS'].isin(oxide_classes) & (df["DAVE"].between(15, 29.99))])
        total_AlO_30_75 = len(df[df['PSEM_CLASS'].isin(oxide_classes) & (df["DAVE"].between(30, 74.99))])
        total_AlO_75    = len(df[df['PSEM_CLASS'].isin(oxide_classes) & (df["DAVE"] >= 75)])

        # Others
        other_classes = ['MgO 10', 'NaCl 10', 'Cu Si 10', 'Si Mn Fe 10', 'Cu 10']
        total_other_count = len(df[df['PSEM_CLASS'].isin(other_classes)])

        result_data.append({
            "File name": file.name,
            "Total Pores": total_05_15 + total_15_30 + total_30_75 + total_75,
            "Total Oxides": total_AlO_05_15 + total_AlO_15_30 + total_AlO_30_75 + total_AlO_75,
            "Total Others": total_other_count
        })

    if result_data:
        summary_df = pd.DataFrame(result_data)
        st.write("### Analysis Results")
        st.dataframe(summary_df)
        
        st.write("### Inclusion Comparison Graph")
        st.bar_chart(summary_df.set_index("File name"))
else:
    st.info("Upload your Aspex data files to begin.")
