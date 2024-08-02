import streamlit as st
import streamlit_authenticator as stauth
import streamlit as st
import pandas as pd
import altair as alt
import pickle
from pathlib import Path
#from wordcloud import WordCloud
#from wordcloud import ImageColorGenerator
#from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

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
    #uploaded_files = st.file_uploader("Drag and drop the Aspex data files here, Excel", type=["xlsx"], accept_multiple_files=True)
    uploaded_files = st.file_uploader("Drag and drop the Aspex data files here, csv", type=["csv"], accept_multiple_files=True)  #test

    uploaded_files1 = st.file_uploader("Drag and drop the Aspex data files here, pxz", type=["pxz"], accept_multiple_files=True)  #test
    
    uploaded_files_csv = st.file_uploader("Drag and drop Grain Size files here, csv", type=["csv"], accept_multiple_files=True)

    uploaded_files_csv_axioscope = st.file_uploader("Drag and drop Grain Size files here_Axioscope, csv", type=["csv"], accept_multiple_files=True)


    #data = pd.read_csv('words.csv')

    #text = " ".join(i for i in data)
    #stopwords = set(STOPWORDS)
    #wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    #plt.figure( figsize=(15,10))
    #plt.axis("off")
    #plt.imshow(wordcloud, interpolation='bilinear')
    #fig = plt.show()
    #st.pyplot()
    
    # If a file is selected, read it into a DataFrame and count the pores
    if uploaded_files:
        result_data=[]
        for file in uploaded_files:
            if file is not None:
                # Read the Excel file into a DataFrame
                #df = pd.read_excel(file, skiprows=1)
                df = pd.read_csv(file)   #test
                
                
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
        df_sorted = new_df.sort_values(by=new_df.index[0], ascending=True, axis=1)
        
        st.table(df_sorted)

        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')
        
        csv = convert_df(df_sorted)
        st.download_button(
            "Press to Download",
            csv,
            "aspex_data.csv",
            "text/csv",
            key='browser-data'
        )

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
    
    # for the pxz data
    if uploaded_files1:
        result_data1=[]
        for file in uploaded_files1:
            if file is not None:
                # Read the Excel file into a DataFrame
                #df = pd.read_excel(file, skiprows=1)
                

                fields = ['PART#', 'FIELD#', 'MAGFIELD#', 'X_ABS', 'Y_ABS', 'X_CG', 'Y_CG', 'X_FERET','Y_FERET', 'DAVE', 'DMAX', 'DMIN', 'DPERP', 'ASPECT', 'AREA', 'PERIMETER','ORIENTATION', 'MAG', 'MAG_INDEX', 'ACTION', 'FIRST_ELEM', 'SECOND_ELEM',
    'THIRD_ELEM', 'FOURTH_ELEM', 'FIRST_CONC', 'SECOND_CONC', 'THIRD_CONC',
    'FOURTH_CONC', 'FIRST_PCT', 'SECOND_PCT', 'THIRD_PCT', 'FOURTH_PCT',
    'VIDEO', 'LIVE_TIME', 'COUNTS', 'TYPE(4ET)#', 'DENSITY', 'PSEM_CLASS',
    'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Mn', 'Fe', 'Ni', 'Cu']


                df = pd.read_csv(file, names=fields, header=None, delim_whitespace=True)   #test
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(9, 'Al 50 Oth 5')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(0, '{Unclassified}')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(1, 'NaCl 10')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(10, 'Al 75')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(11, 'MgO 10')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(2, 'Cu Si 10')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(3, 'Cu 10')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(4, 'Al 50 Mn 5')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(5, 'Al 50 Fe 5')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(6, 'Al 50 Cu 5')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(7, 'Al 50 Si 5')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(8, 'Si Mn Fe 10')
                df['PSEM_CLASS'] = df['PSEM_CLASS'].replace(12, '{Unclassified}')
                
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
                result_data1.append({"File name": file.name,
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
        df_result1 = pd.DataFrame(result_data1)
        new_df1 = df_result1.T
        df_sorted1 = new_df1.sort_values(by=new_df1.index[0], ascending=True, axis=1)
        
        st.table(df_sorted1)

        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')
        
        csv = convert_df(df_sorted1)
        st.download_button(
            "Press to Download",
            csv,
            "aspex_data.csv",
            "text/csv",
            key='browser-data2'
        )

        st.markdown("Histogram graphs for data visualization 📊")
        #st.write(df_result.columns)
        #st.table(df.plot.bar(x="File name", y="Total pores", rot=0))
        #ax = df.plot.bar(x="File name", y="Total pores", rot=0)
        #st.table(ax)

    
        chart_pores1 = alt.Chart(df_result1).mark_bar().encode(
            x=alt.X('File name', axis=alt.Axis(labelAngle= 0)),
            y='Total pores')
        
        chart_oxides1 = alt.Chart(df_result1).mark_bar().encode(
            x=alt.X('File name', axis=alt.Axis(labelAngle= 0)),
            y='Total Oxides',)
    
        chart_other1 = alt.Chart(df_result1).mark_bar().encode(
            x=alt.X('File name', axis=alt.Axis(labelAngle= 0)),
            y='Total Other Inclusions')

        st.caption('Comparison of the total pores')
        st.altair_chart(chart_pores1, use_container_width=True)

        st.caption('Comparison of the Total Oxides')
        st.altair_chart(chart_oxides1, use_container_width=True)

        st.caption('Comparison of the Total Other Inclusions')
        st.altair_chart(chart_other1, use_container_width=True)


    def remove_extremes(data, n):
        sorted_data = np.sort(data)
        return sorted_data[n:-n]

    
    if uploaded_files_csv:
        table_list=[]
        for filename in uploaded_files_csv:
            if filename is not None:
                # Read the CSV file into a DataFrame
                df1 = pd.read_csv(filename, index_col=0, skiprows=1, delimiter=';')
                df_value= df1.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'], axis=1)
                df_value=df_value.rename(columns={'Unnamed: 4':'measurement'})
                mean_size = df_value.mean()
                std = df_value.std()

                #corrected data 
                data = df_value['measurement'].values
                cleaned_data = remove_extremes(data, 5)

                mean_cleaned = np.mean(cleaned_data)
                std_cleaned = np.std(cleaned_data)
                max_value = np.max(cleaned_data)
                min_value = np.min(cleaned_data)
                
                #deviation = f'{std} mm'
                table_list.append({ 'Sample name' : filename.name,
                                    'Grain size (μm)' : mean_size.measurement.round(decimals=3),
                                    'Deviation (μm)' : std.measurement.round(decimals=4),
                                    'Corrected_Grain size (μm)' : mean_cleaned.round(decimals=3),
                                    'Corrected_Standard Deviation (μm)' : std_cleaned.round(decimals=4),
                                    'Max value': max_value,
                                    'Min value': min_value})
        df_grain_size = pd.DataFrame(table_list)
        new_df_grain_size = df_grain_size.T
        st.table(df_grain_size)

        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')

        csv1 = convert_df(df_grain_size)
        st.download_button(
            "Press to Download Kim!!",
            csv1,
            "grain_size.csv",
            "text/csv",
            key='browser-data3'
        )

        chart_grains = alt.Chart(df_grain_size).mark_bar().encode(
            x=alt.X('Sample name', axis=alt.Axis(labelAngle= 0)),
            y= 'Grain size (μm)',
            yError='Deviation (μm)')

        st.caption('Comparison of the Grain size measurement distribution_ Axiovision data')
        st.altair_chart(chart_grains, use_container_width=True)


    if uploaded_files_csv_axioscope:
        table_list4=[]
        for filename in uploaded_files_csv_axioscope:
            if filename is not None:
                # Read the CSV file into a DataFrame
                df1 = pd.read_csv(filename, index_col=0, skiprows=1, sep=';', decimal=',')
                df_value= df1.drop(['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 4'], axis=1)
                df_value=df_value.rename(columns={'Unnamed: 2':'measurement'})
                mean_size = df_value.mean()
                std = df_value.std()

                #corrected data 
                data = df_value['measurement'].values
                cleaned_data = remove_extremes(data, 5)

                mean_cleaned = np.mean(cleaned_data)
                std_cleaned = np.std(cleaned_data)
                max_value = np.max(cleaned_data)
                min_value = np.min(cleaned_data)
                
                #deviation = f'{std} mm'
                table_list4.append({ 'Sample name' : filename.name,
                                    'Grain size (μm)' : mean_size.measurement.round(decimals=3),
                                    'Deviation (μm)' : std.measurement.round(decimals=4),
                                    'Corrected_Grain size (μm)' : mean_cleaned.round(decimals=3),
                                    'Corrected_Standard Deviation (μm)' : std_cleaned.round(decimals=4),
                                    'Max value': max_value,
                                    'Min value': min_value})
        df_grain_size = pd.DataFrame(table_list4)
        new_df_grain_size = df_grain_size.T
        st.table(df_grain_size)

        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')

        csv1 = convert_df(df_grain_size)
        st.download_button(
            "Press to Download",
            csv1,
            "grain_size.csv",
            "text/csv",
            key='browser-data4'
        )

        
        chart_grains = alt.Chart(df_grain_size).mark_bar().encode(
            x=alt.X('Sample name', axis=alt.Axis(labelAngle= 0)),
            y='Grain size (μm)',
            yError='Deviation (μm)')

        
        chart_grains2 = alt.Chart(df_grain_size).mark_bar().encode(
            x=alt.X('Sample name', axis=alt.Axis(labelAngle= 0)),
            y='Corrected_Grain size (μm)',
            yError='Corrected_Standard Deviation (μm)')

        st.caption('Measured data')
        st.altair_chart(chart_grains, use_container_width=True)

        st.caption('Corrected data')
        st.altair_chart(chart_grains2, use_container_width=True)

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;' href="https://www.linkedin.com/in/ugurkayran/" target="_blank">Ugur Kayran</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
