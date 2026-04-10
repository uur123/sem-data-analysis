import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="ENLab Data Analysis", layout="wide")
st.header("ENLab PXZ/CSV Data Analysis")

# --- FILE UPLOADER ---
uploaded_files = st.file_uploader("Upload PXZ or CSV files", type=["pxz", "csv"], accept_multiple_files=True)

if uploaded_files:
    result_data = []
    
    for file in uploaded_files:
        # Read the file
        df = pd.read_csv(file)
        
        # Data cleaning: ensure all object columns are strings (fixes LargeUtf8 errors)
        for col in df.columns:
            if pd.api.types.is_object_dtype(df[col]):
                df[col] = df[col].astype(str)

        # --- FILTRATION LOGIC ---
        # 1. Pores (Al 75 and Al 50 Si 5)
        total_pores = len(df[df['PSEM_CLASS'].isin(['Al 75', 'Al 50 Si 5'])])
        
        # 2. Oxides (Specific Al 50 classes)
        oxide_classes = ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5']
        total_oxides = len(df[df['PSEM_CLASS'].isin(oxide_classes)])
        
        # 3. Others (MgO, NaCl, etc.)
        other_classes = ['MgO 10', 'NaCl 10', 'Cu Si 10', 'Si Mn Fe 10', 'Cu 10']
        total_others = len(df[df['PSEM_CLASS'].isin(other_classes)])

        # Store Results in a simple dictionary
        result_data.append({
            "File name": file.name,
            "Total Pores": total_pores,
            "Total Oxides": total_oxides,
            "Total Others": total_others
        })

    # --- DISPLAY & PLOT ---
    if result_data:
        summary_df = pd.DataFrame(result_data)
        
        st.write("### Data Summary Table")
        st.dataframe(summary_df)

        st.write("### Inclusion Comparison Graph")
        # Set 'File name' as index so the chart groups by file automatically
        chart_df = summary_df.set_index("File name")
        st.bar_chart(chart_df)

        # Optional: Download Button
        csv_data = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Summary CSV",
            data=csv_data,
            file_name='enlab_summary.csv',
            mime='text/csv',
        )
else:
    st.info("Waiting for files to be uploaded...")
