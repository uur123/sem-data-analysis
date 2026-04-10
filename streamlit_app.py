import streamlit as st
import pandas as pd

st.set_page_config(page_title="ENLab Data Analysis", layout="wide")
st.header("ENLab Aspex Data Analysis (by Size)")

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
        # Read file with space separator
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

        # DEFINE CLASSES
        pore_classes = ['Al 75', 'Al 50 Si 5']
        oxide_classes = ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5']

        # FILTRATION LOGIC BY SIZE (DAVE)
        def count_by_size(data, classes):
            return {
                "5-15µm":  len(data[data['PSEM_CLASS'].isin(classes) & (data['DAVE'].between(5, 14.99))]),
                "15-30µm": len(data[data['PSEM_CLASS'].isin(classes) & (data['DAVE'].between(15, 29.99))]),
                "30-75µm": len(data[data['PSEM_CLASS'].isin(classes) & (data['DAVE'].between(30, 74.99))]),
                ">75µm":   len(data[data['PSEM_CLASS'].isin(classes) & (data['DAVE'] >= 75)])
            }

        pore_sizes = count_by_size(df, pore_classes)
        oxide_sizes = count_by_size(df, oxide_classes)

        result_data.append({
            "File": file.name,
            "Pores (5-15)": pore_sizes["5-15µm"],
            "Pores (15-30)": pore_sizes["15-30µm"],
            "Pores (30-75)": pore_sizes["30-75µm"],
            "Pores (>75)": pore_sizes[">75µm"],
            "Oxides (5-15)": oxide_sizes["5-15µm"],
            "Oxides (15-30)": oxide_sizes["15-30µm"],
            "Oxides (30-75)": oxide_sizes["30-75µm"],
            "Oxides (>75)": oxide_sizes[">75µm"]
        })

    if result_data:
        summary_df = pd.DataFrame(result_data)
        st.write("### Detailed Size Summary")
        st.dataframe(summary_df)
        
        st.write("### Size Distribution Graph")
        # Plotting the data - Streamlit will group bars automatically
        st.bar_chart(summary_df.set_index("File"))

else:
    st.info("Upload your Aspex files to generate the size-separated report.")
