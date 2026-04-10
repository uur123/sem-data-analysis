import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import altair as alt
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pyarrow  # Required for the custom hashing fix

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ENlab Data", 
    page_icon=":microscope:",
    layout="wide",
    menu_items={
        'About': "# Just a quick way to extract *information* from the EDX measurement"
    })

#st.set_option('deprecation.showPyplotGlobalUse', False)
st.header(" ENLab data analysis web-app ")

# --- HELPER FOR CACHING PYARROW OBJECTS ---
# This fixes the "UnhashableTypeError: Cannot hash object of type pyarrow.lib.Buffer"
def hash_arrow_buffer(buffer):
    return buffer.to_pybytes()

# --- USER Authenticator ---
names = ['enlabor']
usernames = ['enlabor']

# Load hashed passwords
file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                    'lab', 'abc', cookie_expiry_days=1)

# Handle login
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status is False:
    st.error("Username or Password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your user name and password")
elif authentication_status:
    authenticator.logout("Logout", 'main')

    # --- FILE UPLOADERS ---
    uploaded_files = st.file_uploader("Drag and drop the Aspex data files here, csv", type=["csv"], accept_multiple_files=True)
    uploaded_files1 = st.file_uploader("Drag and drop the Aspex data files here, pxz", type=["pxz"], accept_multiple_files=True)
    uploaded_files_csv = st.file_uploader("Drag and drop Grain Size files here, csv", type=["csv"], accept_multiple_files=True)
    uploaded_files_csv_axioscope = st.file_uploader("Drag and drop Grain Size files here_Axioscope, csv", type=["csv"], accept_multiple_files=True)
    uploaded_files_csv_phenom = st.file_uploader("Drag and drop the Phenom csv data here, csv only", type=["csv"], accept_multiple_files=True)

    # --- PROCESSING ASPEX DATA ---
    if uploaded_files:
        result_data = []
        for file in uploaded_files:
            if file is not None:
                # Read the CSV
                df = pd.read_csv(file)
                
                # --- SOLUTION 1: CONVERT POTENTIAL LARGEUTF8 TYPES ---
                # We force all object/string columns to standard Python strings
                # This prevents the "Unrecognized type: LargeUtf8" error in the browser
                for col in df.columns:
                    if pd.api.types.is_object_dtype(df[col]) or 'string' in str(df[col].dtype):
                        df[col] = df[col].astype(str)

                # --- FILTRATION LOGIC ---
                # High Al content indicates pores
                df_al75_05_15 = df[(df['PSEM_CLASS'] == 'Al 75') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_al50si5_05_15 = df[(df['PSEM_CLASS'] == 'Al 50 Si 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                total_05_15 = len(df_al75_05_15) + len(df_al50si5_05_15)
                
                df_al75_15_30 = df[(df['PSEM_CLASS'] == 'Al 75') & (df["DAVE"] >= 15) & (df['DAVE'] < 30.0)]
                df_al50si5_15_30 = df[(df['PSEM_CLASS'] == 'Al 50 Si 5') & (df["DAVE"] >= 15) & (df['DAVE'] < 30.0)]
                total_15_30 = len(df_al75_15_30) + len(df_al50si5_15_30)
                
                df_al75_30_75 = df[(df['PSEM_CLASS'] == 'Al 75') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_al50si5_30_75 = df[(df['PSEM_CLASS'] == 'Al 50 Si 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                total_30_75 = len(df_al75_30_75) + len(df_al50si5_30_75)
                
                df_al75_75 = df[(df['PSEM_CLASS'] == 'Al 75') & (df["DAVE"] >= 75)]
                df_al50si5_75 = df[(df['PSEM_CLASS'] == 'Al 50 Si 5') & (df["DAVE"] >= 75)]
                total_75 = len(df_al75_75) + len(df_al50si5_75)

                # Al Oxides
                df_Al50Fe5_05_15 = df[(df['PSEM_CLASS'] == 'Al 50 Fe 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_Al50O5_05_15 = df[(df['PSEM_CLASS'] == 'Al 50 Oth 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_Al50Cu5_05_15 = df[(df['PSEM_CLASS'] == 'Al 50 Cu 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_Al50Mn5_05_15 = df[(df['PSEM_CLASS'] == 'Al 50 Mn 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                total_AlO_05_15 = len(df_Al50Fe5_05_15) + len(df_Al50O5_05_15) + len(df_Al50Cu5_05_15) + len(df_Al50Mn5_05_15)
                
                df_Al50Fe5_15_30 = df[(df['PSEM_CLASS'] == 'Al 50 Fe 5') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_Al50O5_15_30 = df[(df['PSEM_CLASS'] == 'Al 50 Oth 5') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_Al50Cu5_15_30 = df[(df['PSEM_CLASS'] == 'Al 50 Cu 5') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_Al50Mn5_15_30 = df[(df['PSEM_CLASS'] == 'Al 50 Mn 5') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                total_AlO_15_30 = len(df_Al50Fe5_15_30) + len(df_Al50O5_15_30) + len(df_Al50Cu5_15_30) + len(df_Al50Mn5_15_30)

                df_Al50Fe5_30_75 = df[(df['PSEM_CLASS'] == 'Al 50 Fe 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_Al50O5_30_75 = df[(df['PSEM_CLASS'] == 'Al 50 Oth 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_Al50Cu5_30_75 = df[(df['PSEM_CLASS'] == 'Al 50 Cu 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_Al50Mn5_30_75 = df[(df['PSEM_CLASS'] == 'Al 50 Mn 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                total_AlO_30_75 = len(df_Al50Fe5_30_75) + len(df_Al50O5_30_75) + len(df_Al50Cu5_30_75) + len(df_Al50Mn5_30_75)

                df_Al50Fe5_75 = df[(df['PSEM_CLASS'] == 'Al 50 Fe 5') & (df["DAVE"] >= 75)]
                df_Al50O5_75 = df[(df['PSEM_CLASS'] == 'Al 50 Oth 5') & (df["DAVE"] >= 75)]
                df_Al50Cu5_75 = df[(df['PSEM_CLASS'] == 'Al 50 Cu 5') & (df["DAVE"] >= 75)]
                df_Al50Mn5_75 = df[(df['PSEM_CLASS'] == 'Al 50 Mn 5') & (df["DAVE"] >= 75)]
                total_AlO_75 = len(df_Al50Fe5_75) + len(df_Al50O5_75) + len(df_Al50Cu5_75) + len(df_Al50Mn5_75)

                # Other Inclusions
                df_MgO10_05_15 = df[(df['PSEM_CLASS'] == 'MgO 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_NaCl_05_15 = df[(df['PSEM_CLASS'] == 'NaCl 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_CuSi10_05_15 = df[(df['PSEM_CLASS'] == 'Cu Si 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_SiMnFe10_05_15 = df[(df['PSEM_CLASS'] == 'Si Mn Fe 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_Cu10_05_15 = df[(df['PSEM_CLASS'] == 'Cu 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                total_other_05_15 = len(df_MgO10_05_15) + len(df_NaCl_05_15) + len(df_CuSi10_05_15) + len(df_SiMnFe10_05_15) + len(df_Cu10_05_15)

                df_MgO10_15_30 = df[(df['PSEM_CLASS'] == 'MgO 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_NaCl_15_30 = df[(df['PSEM_CLASS'] == 'NaCl 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_CuSi10_15_30 = df[(df['PSEM_CLASS'] == 'Cu Si 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_SiMnFe10_15_30 = df[(df['PSEM_CLASS'] == 'Si Mn Fe 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_Cu10_15_30 = df[(df['PSEM_CLASS'] == 'Cu 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                total_other_15_30 = len(df_MgO10_15_30) + len(df_NaCl_15_30) + len(df_CuSi10_15_30) + len(df_SiMnFe10_15_30) + len(df_Cu10_15_30)

                df_MgO10_30_75 = df[(df['PSEM_CLASS'] == 'MgO 10') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_NaCl_30_75 = df[(df['PSEM_CLASS'] == 'NaCl 10') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_CuSi10_30_75 = df[(df['PSEM_CLASS'] == 'Cu Si 10') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_SiMnFe10_30_75 = df[(df['PSEM_CLASS'] == 'Si Mn Fe 10') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_Cu10_30_75 = df[(df['PSEM_CLASS'] == 'Cu 10') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                total_other_30_75 = len(df_MgO10_30_75) + len(df_NaCl_30_75) + len(df_CuSi10_30_75) + len(df_SiMnFe10_30_75) + len(df_Cu10_30_75)

                df_MgO10_75 = df[(df['PSEM_CLASS'] == 'MgO 10') & (df["DAVE"] >= 75)]
                df_NaCl_75 = df[(df['PSEM_CLASS'] == 'NaCl 10') & (df["DAVE"] >= 75)]
                df_CuSi10_75 = df[(df['PSEM_CLASS'] == 'Cu Si 10') & (df["DAVE"] >= 75)]
                df_SiMnFe10_75 = df[(df['PSEM_CLASS'] == 'Si Mn Fe 10') & (df["DAVE"] >= 75)]
                df_Cu10_75 = df[(df['PSEM_CLASS'] == 'Cu 10') & (df["DAVE"] >= 75)]
                total_other_75 = len(df_MgO10_75) + len(df_NaCl_75) + len(df_CuSi10_75) + len(df_SiMnFe10_75) + len(df_Cu10_75)

                # Store Results
                result_data.append({
                    "File name": file.name,
                    "Total pores": total_05_15 + total_15_30 + total_30_75 + total_75,
                    "Number of Pores (0.5 to 15um)": total_05_15,
                    "Number of Pores (15 to 30um)": total_15_30,
                    "Number of Pores (30 to 75um)": total_30_75,
                    "Number of Pores ( >75um )": total_75,
                    "Total Oxides": total_AlO_05_15 + total_AlO_15_30 + total_AlO_30_75 + total_AlO_75,
                    "Oxides (0.5 to 15um)": total_AlO_05_15,
                    "Oxides (15 to 30um)": total_AlO_15_30,
                    "Oxides (30 to 75um)": total_AlO_30_75,
                    "Oxides( >75um )": total_AlO_75,
                    "Total Other Inclusions": total_other_05_15 + total_other_15_30 + total_other_30_75 + total_other_75,
                    "Other Inclusions (0.5 to 15um)": total_other_05_15,
                    "Other Inclusions(15 to 30um)": total_other_15_30,
                    "Other Inclusions (30 to 75um)": total_other_30_75,
                    "Other Inclusions( >75um )": total_other_75
                })

        # --- CACHED DOWNLOAD AND DISPLAY ---
        @st.cache_data(hash_funcs={pyarrow.lib.Buffer: hash_arrow_buffer})
        def convert_df(df_to_convert):
            # Final safety conversion before CSV generation
            for col in df_to_convert.columns:
                if df_to_convert[col].dtype == object:
                    df_to_convert[col] = df_to_convert[col].astype(str)
            return df_to_convert.to_csv(index=False).encode('utf-8')

        if result_data:
            summary_df = pd.DataFrame(result_data)
            st.write("### Aspex Data Summary")
            st.dataframe(summary_df)

            csv_file = convert_df(summary_df)
            st.download_button(
                label="Download Summary as CSV",
                data=csv_file,
                file_name='aspex_summary.csv',
                mime='text/csv',
            )

    # --- FOOTER ---
    st.info("Ensure your requirements.txt includes: streamlit, pandas, pyarrow, streamlit-authenticator")

