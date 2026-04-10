import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="ENLab Inclusion Analysis", layout="wide")
st.header("ENLab Aspex Inclusion Analysis Report")

# --- FILE UPLOADER ---
uploaded_files = st.file_uploader("Upload Aspex files", type=["csv", "pxz"], accept_multiple_files=True)

if uploaded_files:
    report_dict = {}
    
    # Aspex standard fields based on your logic
    fields = [
        'PART#', 'FIELD#', 'MAGFIELD#', 'X_ABS', 'Y_ABS', 'X_CG', 'Y_CG', 'X_FERET','Y_FERET', 
        'DAVE', 'DMAX', 'DMIN', 'DPERP', 'ASPECT', 'AREA', 'PERIMETER','ORIENTATION', 'MAG', 
        'MAG_INDEX', 'ACTION', 'FIRST_ELEM', 'SECOND_ELEM', 'THIRD_ELEM', 'FOURTH_ELEM', 
        'FIRST_CONC', 'SECOND_CONC', 'THIRD_CONC', 'FOURTH_CONC', 'FIRST_PCT', 'SECOND_PCT', 
        'THIRD_PCT', 'FOURTH_PCT', 'VIDEO', 'LIVE_TIME', 'COUNTS', 'TYPE(4ET)#', 'DENSITY', 
        'PSEM_CLASS', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Mn', 'Fe', 'Ni', 'Cu'
    ]

    for file in uploaded_files:
        # Read file using modern pandas separator
        df = pd.read_csv(file, names=fields, header=None, sep=r"\s+", engine='python')
        
        # Numeric code mapping
        mapping = {
            10: 'Al 75', 7: 'Al 50 Si 5',
            5: 'Al 50 Fe 5', 9: 'Al 50 Oth 5', 6: 'Al 50 Cu 5', 4: 'Al 50 Mn 5',
            11: 'MgO 10', 1: 'NaCl 10', 2: 'Cu Si 10', 8: 'Si Mn Fe 10', 3: 'Cu 10',
            0: '{Unclassified}', 12: '{Unclassified}'
        }
        df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(mapping)

        # Helper to calculate size metrics
        def get_metrics(data, classes):
            sub = data[data['PSEM_CLASS'].isin(classes)]
            m5_15 = len(sub[sub['DAVE'].between(5, 14.99)])
            m15_30 = len(sub[sub['DAVE'].between(15, 29.99)])
            m30_75 = len(sub[sub['DAVE'].between(30, 74.99)])
            m75 = len(sub[sub['DAVE'] >= 75])
            return [m5_15 + m15_30 + m30_75 + m75, m5_15, m15_30, m30_75, m75]

        # Calculate for Pores, Oxides, and Others
        p_res = get_metrics(df, ['Al 75', 'Al 50 Si 5'])
        o_res = get_metrics(df, ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5'])
        i_res = get_metrics(df, ['MgO 10', 'NaCl 10', 'Cu Si 10', 'Si Mn Fe 10', 'Cu 10'])

        # Store data: Total, 5-15, 15-30, 30-75, >75 for each type
        report_dict[file.name] = p_res + o_res + i_res

    # --- DEFINE ROW LABELS ---
    row_names = [
        "Total pores", "Number of Pores (5 to 15um)", "Number of Pores (15 to 30um)", "Number of Pores (30 to 75um)", "Number of Pores (>75um)",
        "Total Oxides", "Oxides (5 to 15um)", "Oxides (15 to 30um)", "Oxides (30 to 75um)", "Oxides (>75um)",
        "Total Other Inclusions", "Other Inclusions (5 to 15um)", "Other Inclusions (15 to 30um)", "Other Inclusions (30 to 75um)", "Other Inclusions (>75um)"
    ]
    
    # Create final vertical table
    final_table = pd.DataFrame(report_dict, index=row_names)
    
    # Display table in app
    st.write("### Summary Report Table")
    st.table(final_table)

    # --- EXCEL DOWNLOAD LOGIC ---
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        final_table.to_excel(writer, sheet_name='Inclusion_Summary')
        # Auto-adjust column width for readability
        worksheet = writer.sheets['Inclusion_Summary']
        worksheet.set_column(0, 0, 30)
    
    st.download_button(
        label="📥 Download Summary Report (Excel)",
        data=output.getvalue(),
        file_name="ENLab_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # --- VISUALS (GRAPHS) ---
    plot_df = final_table.T  # Transpose files to rows for chart grouping

    st.subheader("Graph 1: Pores Size Distribution")
    st.bar_chart(plot_df[row_names[1:5]])

    st.subheader("Graph 2: Oxides Size Distribution")
    st.bar_chart(plot_df[row_names[6:10]])

    st.subheader("Graph 3: Other Inclusions Size Distribution")
    st.bar_chart(plot_df[row_names[11:15]])

else:
    st.info("Upload Aspex files to generate the report and graphs.")
