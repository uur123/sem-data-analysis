import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import pickle
from pathlib import Path

# --- AUTH SETUP ---
names = ['enlabor']
usernames = ['enlabor']
file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames": {usernames[i]: {"name": names[i], "password": hashed_passwords[i]} for i in range(len(usernames))}}
authenticator = stauth.Authenticate(credentials, "enlab_cookie", "signature_key", 30)

# --- LOGIN ---
authenticator.login(location='main')

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", location='main')
    st.header("ENLab PXZ Data Analysis")

    # --- FILE UPLOADER ---
    pxz_files = st.file_uploader("Upload PXZ files", type=["pxz", "csv"], accept_multiple_files=True)

    if pxz_files:
        all_results = []
        
        for file in pxz_files:
            # Assuming PXZ can be read like a CSV for this example
            # If PXZ is XML, replace this with your XML parsing logic
            df = pd.read_csv(file)
            
                # --- PROCESSING ASPEX DATA ---
    if uploaded_files:
        result_data = []
        for file in uploaded_files:
            df = pd.read_csv(file)
            
            # Data cleaning for LargeUtf8 fix
            for col in df.columns:
                if pd.api.types.is_object_dtype(df[col]):
                    df[col] = df[col].astype(str)

            # --- FILTRATION LOGIC ---
            # Pores
            total_05_15 = len(df[df['PSEM_CLASS'].isin(['Al 75', 'Al 50 Si 5']) & (df["DAVE"].between(0.5, 14.99))])
            total_15_30 = len(df[df['PSEM_CLASS'].isin(['Al 75', 'Al 50 Si 5']) & (df["DAVE"].between(15, 29.99))])
            total_30_75 = len(df[df['PSEM_CLASS'].isin(['Al 75', 'Al 50 Si 5']) & (df["DAVE"].between(30, 74.99))])
            total_75    = len(df[df['PSEM_CLASS'].isin(['Al 75', 'Al 50 Si 5']) & (df["DAVE"] >= 75)])

            # Oxides
            oxide_classes = ['Al 50 Fe 5', 'Al 50 Oth 5', 'Al 50 Cu 5', 'Al 50 Mn 5']
            total_AlO_05_15 = len(df[df['PSEM_CLASS'].isin(oxide_classes) & (df["DAVE"].between(0.5, 14.99))])
            total_AlO_15_30 = len(df[df['PSEM_CLASS'].isin(oxide_classes) & (df["DAVE"].between(15, 29.99))])
            total_AlO_30_75 = len(df[df['PSEM_CLASS'].isin(oxide_classes) & (df["DAVE"].between(30, 74.99))])
            total_AlO_75    = len(df[df['PSEM_CLASS'].isin(oxide_classes) & (df["DAVE"] >= 75)])

            # Others
            other_classes = ['MgO 10', 'NaCl 10', 'Cu Si 10', 'Si Mn Fe 10', 'Cu 10']
            total_other_05_15 = len(df[df['PSEM_CLASS'].isin(other_classes) & (df["DAVE"].between(0.5, 14.99))])
            total_other_15_30 = len(df[df['PSEM_CLASS'].isin(other_classes) & (df["DAVE"].between(15, 29.99))])
            total_other_30_75 = len(df[df['PSEM_CLASS'].isin(other_classes) & (df["DAVE"].between(30, 74.99))])
            total_other_75    = len(df[df['PSEM_CLASS'].isin(other_classes) & (df["DAVE"] >= 75)])

            # Store Results
            result_data.append({
                "File name": file.name,
                "Total pores": total_05_15 + total_15_30 + total_30_75 + total_75,
                "Total Oxides": total_AlO_05_15 + total_AlO_15_30 + total_AlO_30_75 + total_AlO_75,
                "Total Others": total_other_05_15 + total_other_15_30 + total_other_30_75 + total_other_75
            })

        # --- PLOTTING AND DISPLAY ---
        if result_data:
            summary_df = pd.DataFrame(result_data)
            st.write("### Analysis Results")
            st.dataframe(summary_df)
            
            # This generates the automatic graph
            st.write("### Inclusion Comparison")
            chart_df = summary_df.set_index("File name")
            st.bar_chart(chart_df)

            # Adjust 'PSEM_CLASS' to match your actual PXZ column name
            pore_count = len(df[df['PSEM_CLASS'].str.contains('Al 75|Al 50 Si 5', na=False)])
            oxide_count = len(df[df['PSEM_CLASS'].str.contains('Al 50 Fe 5|Al 50 Oth 5', na=False)])
            
            all_results.append({
                "Filename": file.name,
                "Pores": pore_count,
                "Oxides": oxide_count
            })

        # --- DISPLAY & PLOT ---
        summary_df = pd.DataFrame(all_results)
        
        st.subheader("Data Summary")
        st.dataframe(summary_df)

        st.subheader("Visual Analysis")
        # Plots a simple bar chart comparing Pores vs Oxides per file
        chart_data = summary_df.set_index("Filename")
        st.bar_chart(chart_data)

elif st.session_state["authentication_status"] is False:
    st.error("Invalid credentials")
else:
    st.warning("Please log in to continue")
