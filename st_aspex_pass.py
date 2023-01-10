import streamlit as st
import streamlit_authenticator as stauth
import streamlit as st
import pandas as pd
import altair as alt
import pickle
from pathlib import Path
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt

st.set_page_config(
    page_title= "ENlab Data", 
    page_icon = ":microscope:",
    layout = "wide",
    menu_items = {
        'About': "# Just a qucik way to  extract *information* from the EDX measurement"
    })

st.set_option('deprecation.showPyplotGlobalUse', False)
st.header(" ENLab data analysis web-app ")

# --- USER Authenticator ---
names = ['enlabor']
usernames = ['enlabor']

#load hashed passwords
file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
'lab', 'abc', cookie_expiry_days=1)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error("Username of Password is incorrect")
if authentication_status == None:
    st.warning("Please enter your user name and pasword")
if authentication_status:

    authenticator.logout("Logout", 'main')
    uploaded_files = st.file_uploader("Drag and drop Excel files here", type=["xlsx"], accept_multiple_files=True)
    uploaded_files_csv = st.file_uploader("Drag and drop Grain Size files here", type=["csv"], accept_multiple_files=True)


    data = pd.read_csv('words.csv')

    text = " ".join(i for i in data)
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    plt.figure( figsize=(15,10))
    plt.axis("off")
    plt.imshow(wordcloud, interpolation='bilinear')
    fig = plt.show()
    st.pyplot()
    
    # If a file is selected, read it into a DataFrame and count the pores
    if uploaded_files:
        result_data=[]
        for file in uploaded_files:
            if file is not None:
                # Read the Excel file into a DataFrame
                df = pd.read_excel(file, skiprows=1)
                # High Al content at the detected impurities indicates the presence of pores
                # Count the pores in the range 0.5 to 15um
                df_al75_05_15 = df[(df['PSEM_CLASS']=='Al 75') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_al50si5_05_15 = df[(df['PSEM_CLASS']=='Al 50 Si 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                total_05_15 = len(df_al75_05_15) + len(df_al50si5_05_15)
                
                # 15 to 30um
                df_al75_15_30 = df[(df['PSEM_CLASS']=='Al 75') & (df["DAVE"] >= 15) & (df['DAVE'] < 30.0)]
                df_al50si5_15_30 = df[(df['PSEM_CLASS']=='Al 50 Si 5') & (df["DAVE"] >= 15) & (df['DAVE'] < 30.0)]
                total_15_30= len(df_al75_15_30) + len(df_al50si5_15_30)
                # 30 to 75um
                df_al75_30_75 = df[(df['PSEM_CLASS']=='Al 75') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_al50si5_30_75 = df[(df['PSEM_CLASS']=='Al 50 Si 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                total_30_75= len(df_al75_30_75) + len(df_al50si5_30_75)
                # <75um
                df_al75_75 = df[(df['PSEM_CLASS']=='Al 75') & (df["DAVE"] >= 75)]
                df_al50si5_75 = df[(df['PSEM_CLASS']=='Al 50 Si 5') & (df["DAVE"] >= 75)]
                total_75= len(df_al75_75) + len(df_al50si5_75)
                #-------- Presence of Metal Oxides at the detected impurities indicates the total Al Oxides ------
                # 0.5 to 15
                df_Al50Fe5_05_15 = df[(df['PSEM_CLASS']=='Al 50 Fe 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_Al50O5_05_15 = df[(df['PSEM_CLASS']=='Al 50 Oth 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_Al50Cu5_05_15 = df[(df['PSEM_CLASS']=='Al 50 Cu 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_Al50Mn5_05_15 = df[(df['PSEM_CLASS']=='Al 50 Mn 5') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                total_AlO_05_15 = len(df_Al50Fe5_05_15) + len(df_Al50O5_05_15) + len(df_Al50Cu5_05_15) + len(df_Al50Mn5_05_15)
                
                # 15 to 30um
                df_Al50Fe5_15_30 = df[(df['PSEM_CLASS']=='Al 50 Fe 5') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_Al50O5_15_30 = df[(df['PSEM_CLASS']=='Al 50 Oth 5') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_Al50Cu5_15_30 = df[(df['PSEM_CLASS']=='Al 50 Cu 5') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_Al50Mn5_15_30 = df[(df['PSEM_CLASS']=='Al 50 Mn 5') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                total_AlO_15_30 = len(df_Al50Fe5_15_30) + len(df_Al50O5_15_30) + len(df_Al50Cu5_15_30) + len(df_Al50Mn5_15_30)
                # 30 to 75um
                df_Al50Fe5_30_75 = df[(df['PSEM_CLASS']=='Al 50 Fe 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_Al50O5_30_75 = df[(df['PSEM_CLASS']=='Al 50 Oth 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_Al50Cu5_30_75 = df[(df['PSEM_CLASS']=='Al 50 Cu 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                df_Al50Mn5_30_75 = df[(df['PSEM_CLASS']=='Al 50 Mn 5') & (df["DAVE"] >= 30) & (df['DAVE'] < 75.0)]
                total_AlO_30_75 = len(df_Al50Fe5_30_75) + len(df_Al50O5_30_75) + len(df_Al50Cu5_30_75) + len(df_Al50Mn5_30_75)
                # <75um
                df_Al50Fe5_75 = df[(df['PSEM_CLASS']=='Al 50 Fe 5') & (df["DAVE"] >= 75)]
                df_Al50O5_75 = df[(df['PSEM_CLASS']=='Al 50 Oth 5') & (df["DAVE"] >= 75)]
                df_Al50Cu5_75 = df[(df['PSEM_CLASS']=='Al 50 Cu 5') & (df["DAVE"] >= 75)]
                df_Al50Mn5_75 = df[(df['PSEM_CLASS']=='Al 50 Mn 5') & (df["DAVE"] >= 75)]
                total_AlO_75 = len(df_Al50Fe5_75) + len(df_Al50O5_75) + len(df_Al50Cu5_75) + len(df_Al50Mn5_75)
                #--------- The Other inclusions ---------
                # 0.5 to 15
                df_MgO10_05_15 = df[(df['PSEM_CLASS']=='MgO 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_NaCl_05_15 = df[(df['PSEM_CLASS']=='NaCl 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_CuSi10_05_15 = df[(df['PSEM_CLASS']=='Cu Si 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_SiMnFe10_05_15 = df[(df['PSEM_CLASS']=='Si Mn Fe 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                df_Cu10_05_15 = df[(df['PSEM_CLASS']=='Cu 10') & (df["DAVE"] >= 0.5) & (df['DAVE'] < 15.0)]
                total_other_05_15 = len(df_MgO10_05_15) + len(df_NaCl_05_15) + len(df_CuSi10_05_15) + len(df_SiMnFe10_05_15) + len(df_Cu10_05_15)
                #15 to 30
                df_MgO10_15_30 = df[(df['PSEM_CLASS']=='MgO 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_NaCl_15_30 = df[(df['PSEM_CLASS']=='NaCl 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_CuSi10_15_30 = df[(df['PSEM_CLASS']=='Cu Si 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_SiMnFe10_15_30 = df[(df['PSEM_CLASS']=='Si Mn Fe 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                df_Cu10_15_30 = df[(df['PSEM_CLASS']=='Cu 10') & (df["DAVE"] >= 15.0) & (df['DAVE'] < 30.0)]
                total_other_15_30 = len(df_MgO10_15_30) + len(df_NaCl_15_30) + len(df_CuSi10_15_30) + len(df_SiMnFe10_15_30) + len(df_Cu10_15_30)
                # 30 to 75
                df_MgO10_30_75 = df[(df['PSEM_CLASS']=='MgO 10') & (df["DAVE"] >= 30.0) & (df['DAVE'] < 75.0)]
                df_NaCl_30_75 = df[(df['PSEM_CLASS']=='NaCl 10') & (df["DAVE"] >= 30.0) & (df['DAVE'] < 75.0)]
                df_CuSi10_30_75 = df[(df['PSEM_CLASS']=='Cu Si 10') & (df["DAVE"] >= 30.0) & (df['DAVE'] < 75.0)]
                df_SiMnFe10_30_75 = df[(df['PSEM_CLASS']=='Si Mn Fe 10') & (df["DAVE"] >= 30.0) & (df['DAVE'] < 75.0)]
                df_Cu10_30_75 = df[(df['PSEM_CLASS']=='Cu 10') & (df["DAVE"] >= 30.0) & (df['DAVE'] < 75.0)]
                total_other_30_75 = len(df_MgO10_30_75) + len(df_NaCl_30_75) + len(df_CuSi10_30_75) + len(df_SiMnFe10_30_75) + len(df_Cu10_30_75)
                # >75
                df_MgO10_75 = df[(df['PSEM_CLASS']=='MgO 10') & (df["DAVE"] >= 75)]
                df_NaCl_75 = df[(df['PSEM_CLASS']=='NaCl 10') & (df["DAVE"] >= 75.0)]
                df_CuSi10_75 = df[(df['PSEM_CLASS']=='Cu Si 10') & (df["DAVE"] >= 75.0)]
                df_SiMnFe10_75 = df[(df['PSEM_CLASS']=='Si Mn Fe 10') & (df["DAVE"] >= 75.0)]
                df_Cu10_75 = df[(df['PSEM_CLASS']=='Cu 10') & (df["DAVE"] >= 75.0)]
                total_other_75 = len(df_MgO10_75) + len(df_NaCl_75) + len(df_CuSi10_75) + len(df_SiMnFe10_75) + len(df_Cu10_75)
                result_data.append({"File name": file.name,
                                    "Total pores": total_05_15 + total_15_30 + total_30_75 + total_75,
                                    "Number of Pores (0.5 to 15um)": total_05_15,
                                    "Number of Pores (15 to 30um)": total_15_30,
                                    "Number of Pores (30 to 75um)": total_30_75,
                                    "Number of Pores ( <75um )": total_75,
                                    "Total Oxides": total_AlO_05_15 + total_AlO_15_30 + total_AlO_30_75 + total_AlO_75,
                                    "Oxides (0.5 to 15um)": total_AlO_05_15,
                                    "Oxides (15 to 30um)": total_AlO_15_30,
                                    "Oxides (30 to 75um)": total_AlO_30_75,
                                    "Oxides( <75um )": total_AlO_75,
                                    "Total Other Inclusions": total_other_05_15 + total_other_15_30 + total_other_30_75 + total_other_75,
                                    "Other Inclusions (0.5 to 15um)": total_other_05_15,
                                    "Other Inclusions(15 to 30um)": total_other_15_30,
                                    "Other Inclusions (30 to 75um)": total_other_30_75,
                                    "Other Inclusions( <75um )": total_other_75,})
        df_result = pd.DataFrame(result_data)
        new_df = df_result.T
        st.table(new_df)
        
        st.markdown("Histogram graphs for data visualization 📊")
        #st.write(df_result.columns)
        #st.table(df.plot.bar(x="File name", y="Total pores", rot=0))
        #ax = df.plot.bar(x="File name", y="Total pores", rot=0)
        #st.table(ax)

    
        chart_pores = alt.Chart(df_result).mark_bar().encode(
            x=alt.X('File name', axis=alt.Axis(labelAngle= 0)),
            y='Total pores')
        
        chart_oxides = alt.Chart(df_result).mark_bar().encode(
            x=alt.X('File name', axis=alt.Axis(labelAngle= 0)),
            y='Total Oxides',)
    
        chart_other = alt.Chart(df_result).mark_bar().encode(
            x=alt.X('File name', axis=alt.Axis(labelAngle= 0)),
            y='Total Other Inclusions')

        st.caption('Comparison of the total pores')
        st.altair_chart(chart_pores, use_container_width=True)

        st.caption('Comparison of the Total Oxides')
        st.altair_chart(chart_oxides, use_container_width=True)

        st.caption('Comparison of the Total Other Inclusions')
        st.altair_chart(chart_other, use_container_width=True)


    if uploaded_files_csv:
        table_list=[]
        for filename in uploaded_files_csv:
            if filename is not None:
                # Read the CSV file into a DataFrame
                df1 = pd.read_csv(filename, index_col=0, skiprows=1)
                df_value= df1.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'], axis=1)
                df_value=df_value.rename(columns={'Unnamed: 4':'measurement'})
                mean_size = df_value.mean()
                std = df_value.std()
                #deviation = f'{std} mm'
                table_list.append({'Sample name' : filename.name,
                                  'Grain size (mm)' : mean_size.measurement.round(decimals=3),
                                  'Deviation (mm)' : std.measurement.round(decimals=4)})
        df_grain_size = pd.DataFrame(table_list)
        new_df_grain_size = df_grain_size.T
        st.table(df_grain_size)

        chart_grains = alt.Chart(df_grain_size).mark_bar().encode(
            x=alt.X('Sample name', axis=alt.Axis(labelAngle= 0)),
            y= 'Grain size (mm)')

        st.caption('Comparison of the Grain size measurement distribution')
        st.altair_chart(chart_grains, use_container_width=True)


