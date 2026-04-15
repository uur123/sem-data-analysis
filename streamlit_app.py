import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="ENLab Multi-Instrument Analysis", layout="wide")
st.header("ENLab Inclusion Analysis Report")

def process_data(df, instrument_type):
    """
    Processes the dataframe using physical column indices.
    Perception/Phenom: Size is Col 12 (Index 11), Class is Col 40 (Index 39)
    Aspex: Size is Col 10 (Index 9), Class is Col 38 (Index 37)
    """
    
    if instrument_type == "Aspex":
        size_idx = 9   
        class_idx = 37 
        mapping = {
            10: 'Al 75', 7: 'Al 50 Si 5', 5: 'Al 50 Fe 5', 9: 'Al 50 Oth 5', 
            6: 'Al 50 Cu 5', 4: 'Al 50 Mn 5', 11: 'MgO 10', 1: 'NaCl 10', 
            2: 'Cu Si 10', 8: 'Si Mn Fe 10', 3: 'Cu 10', 0: '{Unclassified}', 12: '{Unclassified}'
        }
    else:
        # Perception/Phenom mapping from your helper file
        size_idx = 11  # The 12th value (e.g., 5.82)
        class_idx = 39 # The 40th value (e.g., 8)
        mapping = {
            0: 'Pore via cps', 1: '{Unclassified}', 2: 'NaCl 10', 3: 'CuSi 10', 
            4: 'Cu 10', 5: 'Al50Mn5', 6: 'AL50Fe5', 7: 'Al50Cu5', 8: 'Al50Si5', 
            9: 'SiMnFe10', 10: 'Al50 Oth5', 11: 'Al75', 12: 'MgO10', 13: 'True'
        }

    # Extract columns by physical position
    df['size_vals'] = pd.to_numeric(df.iloc[:, size_idx], errors='coerce')
    df['class_codes'] = pd.to_numeric(df.iloc[:, class_idx], errors='coerce').fillna(1).astype(int)
    
    # Map codes to names and clean (lowercase, no spaces) for grouping
    df['Mapped_Name'] = df['class_codes'].map(mapping).str.replace(" ", "").str.lower()

    # Define Categories
    pores = ['poreviacps', 'al75', 'al50si5']
    oxides = ['al50fe5', 'al50oth5', 'al50cu5', 'al50mn5']
    others = ['mgo10', 'nacl10', 'cusi10', 'simnfe10', 'cu10']

    def get_metrics(data, target_classes):
        sub = data[data['Mapped_Name'].isin(target_classes)]
        s = sub['size_vals']
        return [
            len(sub), 
            len(sub[s.between(5, 14.99)]), 
            len(sub[s.between(15, 29.99)]), 
            len(sub[s.between(30, 74.99)]), 
            len(sub[s >= 75])
        ]

    return get_metrics(df, pores) + get_metrics(df, oxides) + get_metrics(df, others)

def run_ui(uploaded_files, instrument_type):
    if not uploaded_files:
        st.info(f"Please upload {instrument_type} files to begin.")
        return

    report_dict = {}
    for file in uploaded_files:
        try:
            # Perception/Aspex raw files use whitespace/tabs
            df = pd.read_csv(file, header=None, sep=None, engine='python')
            
            if len(df) > 0:
                st.success(f"✅ {file.name}: Processed {len(df)} particles.")
                report_dict[file.name] = process_data(df, instrument_type)
            else:
                st.error(f"❌ {file.name} appears to be empty.")
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    if report_dict:
        row_names = [
            "Total pores", "Number of Pores (5 to 15um)", "Number of Pores (15 to 30um)", "Number of Pores (30 to 75um)", "Number of Pores (>75um)",
            "Total Oxides", "Oxides (5 to 15um)", "Oxides (15 to 30um)", "Oxides (30 to 75um)", "Oxides (>75um)",
            "Total Other Inclusions", "Other Inclusions (5 to 15um)", "Other Inclusions (15 to 30um)", "Other Inclusions (30 to 75um)", "Other Inclusions (>75um)"
        ]
        
        final_table = pd.DataFrame(report_dict, index=row_names)
        
        st.write("### Summary Report Table")
        st.table(final_table)

        # --- EXCEL DOWNLOAD ---
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            final_table.to_excel(writer, sheet_name='Summary')
            writer.sheets['Summary'].set_column(0, 0, 35)
        
        st.download_button(
            label=f"📥 Download {instrument_type} Report (Excel)",
            data=output.getvalue(),
            file_name=f"ENLab_{instrument_type}_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"btn_{instrument_type}"
        )

        # --- GRAPHS ---
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

# --- TABS INTERFACE ---
tab1, tab2 = st.tabs(["Aspex Instrument", "Perception/Phenom Instrument"])

with tab1:
    files_aspex = st.file_uploader("Upload Aspex files (.csv, .pxz)", accept_multiple_files=True, key="asp_up")
    run_ui(files_aspex, "Aspex")

with tab2:
    files_phenom = st.file_uploader("Upload Perception/Phenom files (.csv, .pxz)", accept_multiple_files=True, key="phen_up")
    run_ui(files_phenom, "Perception")
