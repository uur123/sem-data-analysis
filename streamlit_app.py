import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="ENLab Multi-Instrument Analysis", layout="wide")
st.header("ENLab Inclusion Analysis Report")

# --- TABS FOR DIFFERENT INSTRUMENTS ---
tab1, tab2 = st.tabs(["Aspex Instrument", "Phenom/Phantom Instrument"])

def process_and_display(df, instrument_type):
    """Core logic to process cleaned data and return metrics regardless of source"""
    
    # 1. IDENTIFY COLUMNS (Fuzzy search to avoid KeyErrors)
    class_col = None
    size_col = None
    
    # Look for classification column
    for col in df.columns:
        if any(keyword in col for keyword in ['Classification', 'PSEM_CLASS', 'Type']):
            class_col = col
            break
            
    # Look for size/diameter column
    for col in df.columns:
        if 'DAve' in col or 'DAVE' in col:
            size_col = col
            break

    if not class_col or not size_col:
        st.error(f"Could not find required columns in {instrument_type} file. Found: {list(df.columns)}")
        return [0]*15

    # 2. MAPPING (Different for each instrument)
    if instrument_type == "Aspex":
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
        # Phenom specific mapping as provided
        mapping = {
            0: 'Pore via cps', 1: '{Unclassified}', 2: 'NaCl 10', 3: 'CuSi 10', 
            4: 'Cu 10', 5: 'Al50Mn5', 6: 'AL50Fe5', 7: 'Al50Cu5', 8: 'Al50Si5', 
            9: 'SiMnFe10', 10: 'Al50 Oth5', 11: 'Al75', 12: 'MgO10', 13: 'True'
        }
        pore_classes = ['Pore via cps', 'Al75', 'Al50Si5']
        oxide_classes = ['AL50Fe5', 'Al50 Oth5', 'Al50Cu5', 'Al50Mn5']
        other_classes = ['MgO10', 'NaCl 10', 'CuSi 10', 'SiMnFe10', 'Cu 10']

    # Convert column to numeric first (Phenom often reads them as strings if quoted)
    df[class_col] = pd.to_numeric(df[class_col], errors='coerce')
    df_mapped = df.copy()
    df_mapped[class_col] = df[class_col].map(mapping)

    def get_metrics(data, classes):
        sub = data[data[class_col].isin(classes)]
        # Ensure size column is numeric
        sizes = pd.to_numeric(sub[size_col], errors='coerce')
        m5_15 = len(sub[sizes.between(5, 14.99)])
        m15_30 = len(sub[sizes.between(15, 29.99)])
        m30_75 = len(sub[sizes.between(30, 74.99)])
        m75 = len(sub[sizes >= 75])
        return [m5_15 + m15_30 + m30_75 + m75, m5_15, m15_30, m30_75, m75]

    # Calculate Results
    p_res = get_metrics(df_mapped, pore_classes)
    o_res = get_metrics(df_mapped, oxide_classes)
    i_res = get_metrics(df_mapped, other_classes)
    
    return p_res + o_res + i_res

def run_ui(uploaded_files, instrument_type):
    if not uploaded_files:
        st.info(f"Upload {instrument_type} files to generate the report.")
        return

    report_dict = {}
    aspex_fields = [
        'PART#', 'FIELD#', 'MAGFIELD#', 'X_ABS', 'Y_ABS', 'X_CG', 'Y_CG', 'X_FERET','Y_FERET', 
        'DAVE', 'DMAX', 'DMIN', 'DPERP', 'ASPECT', 'AREA', 'PERIMETER','ORIENTATION', 'MAG', 
        'MAG_INDEX', 'ACTION', 'FIRST_ELEM', 'SECOND_ELEM', 'THIRD_ELEM', 'FOURTH_ELEM', 
        'FIRST_CONC', 'SECOND_CONC', 'THIRD_CONC', 'FOURTH_CONC', 'FIRST_PCT', 'SECOND_PCT', 
        'THIRD_PCT', 'FOURTH_PCT', 'VIDEO', 'LIVE_TIME', 'COUNTS', 'TYPE(4ET)#', 'DENSITY', 
        'PSEM_CLASS', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Mn', 'Fe', 'Ni', 'Cu'
    ]

    for file in uploaded_files:
        try:
            if instrument_type == "Aspex":
                df = pd.read_csv(file, names=aspex_fields, header=None, sep=r"\s+", engine='python')
            else:
                # Phenom files usually use tab or comma; sep=None allows pandas to guess
                df = pd.read_csv(file, sep=None, engine='python')
                df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", "")
            
            report_dict[file.name] = process_and_display(df, instrument_type)
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")

    row_names = [
        "Total pores", "Number of Pores (5 to 15um)", "Number of Pores (15 to 30um)", "Number of Pores (30 to 75um)", "Number of Pores (>75um)",
        "Total Oxides", "Oxides (5 to 15um)", "Oxides (15 to 30um)", "Oxides (30 to 75um)", "Oxides (>75um)",
        "Total Other Inclusions", "Other Inclusions (5 to 15um)", "Other Inclusions (15 to 30um)", "Other Inclusions (30 to 75um)", "Other Inclusions (>75um)"
    ]
    
    final_table = pd.DataFrame(report_dict, index=row_names)
    st.write(f"### Summary Report Table ({instrument_type})")
    st.table(final_table)

    # --- DOWNLOAD LOGIC ---
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        final_table.to_excel(writer, sheet_name='Summary')
        writer.sheets['Summary'].set_column(0, 0, 40)
    
    st.download_button(label=f"📥 Download {instrument_type} Excel", data=output.getvalue(), 
                       file_name=f"ENLab_{instrument_type}_Report.xlsx", key=f"dl_{instrument_type}")

    # --- VISUALS ---
    plot_df = final_table.T
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Pores")
        st.bar_chart(plot_df[row_names[1:5]])
    with c2:
        st.subheader("Oxides")
        st.bar_chart(plot_df[row_names[6:10]])
    with c3:
        st.subheader("Other Inclusions")
        st.bar_chart(plot_df[row_names[11:15]])

# Render
with tab1:
    files1 = st.file_uploader("Upload Aspex files", type=["csv", "pxz"], accept_multiple_files=True, key="u1")
    run_ui(files1, "Aspex")

with tab2:
    files2 = st.file_uploader("Upload Phenom files", type=["csv"], accept_multiple_files=True, key="u2")
    run_ui(files2, "Phenom-Phantom")
