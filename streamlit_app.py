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
    
    # Mapping for Classification IDs to Names
    mapping = {
        10: 'Al 75', 7: 'Al 50 Si 5',
        5: 'Al 50 Fe 5', 9: 'Al 50 Oth 5', 6: 'Al 50 Cu 5', 4: 'Al 50 Mn 5',
        11: 'MgO 10', 1: 'NaCl 10', 2: 'Cu Si 10', 8: 'Si Mn Fe 10', 3: 'Cu 10',
        0: '{Unclassified}', 12: '{Unclassified}'
    }
    
    # Normalizing Column Names between instruments
    # Aspex uses 'PSEM_CLASS' and 'DAVE'
    # Phenom uses 'Classification' and 'DAve (µm)'
    class_col = 'PSEM_CLASS' if 'PSEM_CLASS' in df.columns else 'Classification'
    
    # Handle the specific encoding characters in Phenom column names (Î¼m)
    size_col = 'DAVE'
    for col in df.columns:
        if 'DAve' in col:
            size_col = col
            break
    
    df[class_col] = df[class_col].replace(mapping)

    def get_metrics(data, classes):
        sub = data[data[class_col].isin(classes)]
        m5_15 = len(sub[sub[size_col].between(5, 14.99)])
        m15_30 = len(sub[sub[size_col].between(15, 29.99)])
        m30_75 = len(sub[sub[size_col].between(30, 74.99)])
        m75 = len(sub[sub[size_col] >= 75])
        return [m5_15 + m15_30 + m30_75 + m75, m5_15, m15_30, m30_75, m75]

    # Grouping logic
    p_res = get_metrics(df, ['Al 75', 'Al 50 Si 5'])
    o_res = get_metrics(df, ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5'])
    i_res = get_metrics(df, ['MgO 10', 'NaCl 10', 'Cu Si 10', 'Si Mn Fe 10', 'Cu 10'])
    
    return p_res + o_res + i_res

def run_ui(uploaded_files, instrument_type):
    if not uploaded_files:
        st.info(f"Upload {instrument_type} files to generate the report.")
        return

    report_dict = {}
    
    # Columns for Aspex (No headers in raw file)
    aspex_fields = [
        'PART#', 'FIELD#', 'MAGFIELD#', 'X_ABS', 'Y_ABS', 'X_CG', 'Y_CG', 'X_FERET','Y_FERET', 
        'DAVE', 'DMAX', 'DMIN', 'DPERP', 'ASPECT', 'AREA', 'PERIMETER','ORIENTATION', 'MAG', 
        'MAG_INDEX', 'ACTION', 'FIRST_ELEM', 'SECOND_ELEM', 'THIRD_ELEM', 'FOURTH_ELEM', 
        'FIRST_CONC', 'SECOND_CONC', 'THIRD_CONC', 'FOURTH_CONC', 'FIRST_PCT', 'SECOND_PCT', 
        'THIRD_PCT', 'FOURTH_PCT', 'VIDEO', 'LIVE_TIME', 'COUNTS', 'TYPE(4ET)#', 'DENSITY', 
        'PSEM_CLASS', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Mn', 'Fe', 'Ni', 'Cu'
    ]

    for file in uploaded_files:
        if instrument_type == "Aspex":
            df = pd.read_csv(file, names=aspex_fields, header=None, sep=r"\s+", engine='python')
        else:
            # Phenom/Phantom usually has headers and uses standard CSV comma/tab separation
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip() # Clean column name whitespace

        report_dict[file.name] = process_and_display(df, instrument_type)

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
        writer.sheets['Summary'].set_column(0, 0, 35)
    
    st.download_button(
        label=f"📥 Download {instrument_type} Summary (Excel)",
        data=output.getvalue(),
        file_name=f"ENLab_{instrument_type}_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # --- VISUALS ---
    plot_df = final_table.T
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Pores Size Distribution")
        st.bar_chart(plot_df[row_names[1:5]])
    with c2:
        st.subheader("Oxides Size Distribution")
        st.bar_chart(plot_df[row_names[6:10]])
    with c3:
        st.subheader("Other Inclusions")
        st.bar_chart(plot_df[row_names[11:15]])

# Render the tabs
with tab1:
    files1 = st.file_uploader("Upload Aspex files", type=["csv", "pxz"], accept_multiple_files=True, key="u1")
    run_ui(files1, "Aspex")

with tab2:
    files2 = st.file_uploader("Upload Phenom/Phantom files", type=["csv"], accept_multiple_files=True, key="u2")
    run_ui(files2, "Phenom-Phantom")
