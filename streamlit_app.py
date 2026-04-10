import streamlit as st
import pandas as pd

st.set_page_config(page_title="ENLab Inclusion Analysis", layout="wide")
st.header("ENLab Aspex Inclusion Analysis")

uploaded_files = st.file_uploader("Upload Aspex files", type=["csv", "pxz"], accept_multiple_files=True)

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
        df = pd.read_csv(file, names=fields, header=None, sep=r"\s+", engine='python')
        
        mapping = {
            10: 'Al 75', 7: 'Al 50 Si 5',
            5: 'Al 50 Fe 5', 9: 'Al 50 Oth 5', 6: 'Al 50 Cu 5', 4: 'Al 50 Mn 5',
            11: 'MgO 10', 1: 'NaCl 10', 2: 'Cu Si 10', 8: 'Si Mn Fe 10', 3: 'Cu 10',
            0: '{Unclassified}', 12: '{Unclassified}'
        }
        df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(mapping)

        # Helper to get size counts
        def get_sizes(data, classes):
            subset = data[data['PSEM_CLASS'].isin(classes)]
            return [
                len(subset[subset['DAVE'].between(5, 14.99)]),
                len(subset[subset['DAVE'].between(15, 29.99)]),
                len(subset[subset['DAVE'].between(30, 74.99)]),
                len(subset[subset['DAVE'] >= 75])
            ]

        # Categorize
        pores = get_sizes(df, ['Al 75', 'Al 50 Si 5'])
        oxides = get_sizes(df, ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5'])
        others = get_sizes(df, ['MgO 10', 'NaCl 10', 'Cu Si 10', 'Si Mn Fe 10', 'Cu 10'])

        result_data.append({
            "File": file.name,
            "P_5_15": pores[0], "P_15_30": pores[1], "P_30_75": pores[2], "P_GT75": pores[3],
            "O_5_15": oxides[0], "O_15_30": oxides[1], "O_30_75": oxides[2], "O_GT75": oxides[3],
            "I_5_15": others[0], "I_15_30": others[1], "I_30_75": others[2], "I_GT75": others[3]
        })

    if result_data:
        full_df = pd.DataFrame(result_data)
        
        # --- 1. PORES GRAPH ---
        st.subheader("Graph 1: Pores Size Distribution")
        pore_df = full_df[["File", "P_5_15", "P_15_30", "P_30_75", "P_GT75"]].set_index("File")
        pore_df.columns = ["5-15µm", "15-30µm", "30-75µm", ">75µm"]
        st.bar_chart(pore_df)

        # --- 2. OXIDES GRAPH ---
        st.subheader("Graph 2: Oxides Size Distribution")
        oxide_df = full_df[["File", "O_5_15", "O_15_30", "O_30_75", "O_GT75"]].set_index("File")
        oxide_df.columns = ["5-15µm", "15-30µm", "30-75µm", ">75µm"]
        st.bar_chart(oxide_df)

        # --- 3. OTHER INCLUSIONS GRAPH ---
        st.subheader("Graph 3: Other Inclusions Size Distribution")
        other_df = full_df[["File", "I_5_15", "I_15_30", "I_30_75", "I_GT75"]].set_index("File")
        other_df.columns = ["5-15µm", "15-30µm", "30-75µm", ">75µm"]
        st.bar_chart(other_df)

        # Summary Table
        st.write("### Raw Data Summary")
        st.dataframe(full_df)

else:
    st.info("Upload files to generate graphs.")
