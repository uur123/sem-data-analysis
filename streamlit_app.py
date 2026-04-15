import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="ENLab Multi-Instrument Analysis", layout="wide")
st.header("ENLab Inclusion Analysis Report")

tab1, tab2 = st.tabs(["Aspex Instrument", "Phenom/Phantom Instrument"])

def process_data(df, instrument_type):
    """Processes dataframe based on instrument-specific column mapping"""
    
    # 1. DEFINE COLUMNS AND MAPPING
    if instrument_type == "Aspex":
        size_col = 'DAVE'
        class_col = 'PSEM_CLASS'
        mapping = {
            10: 'Al 75', 7: 'Al 50 Si 5',
            5: 'Al 50 Fe 5', 9: 'Al 50 Oth 5', 6: 'Al 50 Cu 5', 4: 'Al 50 Mn 5',
            11: 'MgO 10', 1: 'NaCl 10', 2: 'Cu Si 10', 8: 'Si Mn Fe 10', 3: 'Cu 10',
            0: '{Unclassified}', 12: '{Unclassified}'
        }
        pore_classes = ['Al 75', 'Al 50 Si 5']
        oxide_classes = ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5']
        other_classes = ['MgO 10', 'NaCl 10', 'Cu Si 10', 'Si Mn Fe 10', 'Cu 10']
    else:
        # Phenom Mapping based on your provided list
        size_col = 'DAve' # Column index 9
        class_col = 'PSEM_CLASS' # Column index 18
        mapping = {
            0: 'Pore via cps', 1: '{Unclassified}', 2: 'NaCl 10', 3: 'CuSi 10', 
            4: 'Cu 10', 5: 'Al50Mn5', 6: 'AL50Fe5', 7: 'Al50Cu5', 8: 'Al50Si5', 
            9: 'SiMnFe10', 10: 'Al50 Oth5', 11: 'Al75', 12: 'MgO10', 13: 'True'
        }
        pore_classes = ['Pore via cps', 'Al75', 'Al50Si5']
        oxide_classes = ['AL50Fe5', 'Al50 Oth5', 'Al50Cu5', 'Al50Mn5']
        other_classes = ['MgO10', 'NaCl 10', 'CuSi 10', 'SiMnFe10', 'Cu 10']

    # 2. APPLY MAPPING
    df[class_col] = pd.to_numeric(df[class_col], errors='coerce').fillna(1).astype(int)
    df['Mapped_Class'] = df[class_col].map(mapping)

    def get_metrics(data, classes):
        sub = data[data['Mapped_Class'].isin(classes)]
        sizes = pd.to_numeric(sub[size_col], errors='coerce')
        m5_15 = len(sub[sizes.between(5, 14.99)])
        m15_30 = len(sub[sizes.between(15, 29.99)])
        m30_75 = len(sub[sizes.between(30, 74.99)])
        m75 = len(sub[sizes >= 75])
        return [m5_15 + m15_30 + m30_75 + m75, m5_15, m15_30, m30_75, m75]

    return get_metrics(df, pore_classes) + get_metrics(df, oxide_classes) + get_metrics(df, other_classes)

def run_ui(uploaded_files, instrument_type):
    if not uploaded_files:
        st.info(f"Please upload {instrument_type} files.")
        return

    # Column Definitions
    aspex_fields = [
        'PART#', 'FIELD#', 'MAGFIELD#', 'X_ABS', 'Y_ABS', 'X_CG', 'Y_CG', 'X_FERET','Y_FERET', 
        'DAVE', 'DMAX', 'DMIN', 'DPERP', 'ASPECT', 'AREA', 'PERIMETER','ORIENTATION', 'MAG', 
        'MAG_INDEX', 'ACTION', 'FIRST_ELEM', 'SECOND_ELEM', 'THIRD_ELEM', 'FOURTH_ELEM', 
        'FIRST_CONC', 'SECOND_CONC', 'THIRD_CONC', 'FOURTH_CONC', 'FIRST_PCT', 'SECOND_PCT', 
        'THIRD_PCT', 'FOURTH_PCT', 'VIDEO', 'LIVE_TIME', 'COUNTS', 'TYPE(4ET)#', 'DENSITY', 
        'PSEM_CLASS', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Mn', 'Fe', 'Ni', 'Cu'
    ]
    
    # Phenom mapping based on your raw data snippet
    phenom_fields = [
        "Part#", "Field#", "SubField#", "X_Stage", "Y_Stage", "X_Pixel", "Y_Pixel", "Width", "Height", 
        "DAve", "DMax", "DMin", "DPerp", "Aspect", "Area", "Perimeter", "Orientation", "Mag", "Density",
        "HV", "Cond", "PAction", "VoidA", "VoidC", "Rough", "Rms", "Round", "Form", "ECD", "Skel", 
        "HullA", "HullP", "E1", "E2", "E3", "E4", "LiveT", "Counts", "Type(4ET)", "Al", "Si", "Fe", "Cu"
        # ... remaining columns will be handled by pandas automatically
    ]

    report_dict = {}
    for file in uploaded_files:
        try:
            if instrument_type == "Aspex":
                df = pd.read_csv(file, names=aspex_fields, header=None, sep=r"\s+", engine='python')
            else:
                # Phenom raw pxz data is tab-separated (\t)
                df = pd.read_csv(file, names=phenom_fields, header=None, sep=None, engine='python')
            
            report_dict[file.name] = process_data(df, instrument_type)
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    row_names = [
        "Total pores", "Number of Pores (5 to 15um)", "Number of Pores (15 to 30um)", "Number of Pores (30 to 75um)", "Number of Pores (>75um)",
        "Total Oxides", "Oxides (5 to 15um)", "Oxides (15 to 30um)", "Oxides (30 to 75um)", "Oxides (>75um)",
        "Total Other Inclusions", "Other Inclusions (5 to 15um)", "Other Inclusions (15 to 30um)", "Other Inclusions (30 to 75um)", "Other Inclusions (>75um)"
    ]
    
    final_table = pd.DataFrame(report_dict, index=row_names)
    st.table(final_table)

    # Download
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        final_table.to_excel(writer, sheet_name='Report')
    st.download_button("📥 Download Excel", output.getvalue(), f"{instrument_type}_Report.xlsx", key=f"dl_{instrument_type}")

    # Charts
    plot_df = final_table.T
    st.subheader("Pores Distribution")
    st.bar_chart(plot_df[row_names[1:5]])
    st.subheader("Oxides Distribution")
    st.bar_chart(plot_df[row_names[6:10]])

with tab1:
    run_ui(st.file_uploader("Upload Aspex", accept_multiple_files=True, key="a"), "Aspex")
with tab2:
    run_ui(st.file_uploader("Upload Phenom", accept_multiple_files=True, key="p"), "Phenom")
