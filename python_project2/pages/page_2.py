import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# page title
st.header(":rainbow[# Category Analysis - Total❄️]",divider=True)
st.sidebar.markdown("# Category - Total❄️")

# file path and name

def file_path(): 
    file=st.text_input("Input your file name and path!!") 
    if file:           
        try:
            df=pd.read_csv(file)
        except Exception as e:
            st.text(f"{e}, try again!!")
            return False
        else:
            st.write("File Path is Correct ^-^")           
            return file
    else:
        return False

file=file_path()


# input user name

def session_name():
    """ st.text_input("Your name", key="name") """
    st.session_state.name="jy"
    if session_name:
        return True
    else:
        return False

session_name=session_name()

# chart data

def chart_data(df):
    df=df.dropna()
    chart_data=pd.DataFrame(
        {   "description":df["Description"],
            "deposit":(df["Deposits"].str.replace(",","")).astype(float).round(),
            "withdrawls":(df["Withdrawls"].str.replace(",","")).astype(float).round(),
            "balance":(df["Balance"].str.replace(",","")).astype(float).round()
        }
    )
    chart_data.index=pd.to_datetime(df["Date"])
    chart_data.index=chart_data.index.to_period(freq="D")
    chart_data.to_csv("chart_data.csv")
    return chart_data


chart_datas=pd.DataFrame({"description":[1]})
lists=["All"]
if file and session_name:
    df=pd.read_csv(file)
    chart_datas=chart_data(df)

    # description list
    
    for i in chart_datas["description"]:
        if i in lists:
            continue
        else:
            lists.append(i)


# grouped_data
def group_sum_data(chart_datas):
    group_sum_data=pd.DataFrame(
        {
            "deposit":np.round(chart_datas.groupby("description")["deposit"].sum()),
            "withdrawls":np.round(chart_datas.groupby("description")["withdrawls"].sum()),
        }
    )
    group_sum_data["margin"]=group_sum_data["deposit"]-group_sum_data["withdrawls"]
    return group_sum_data



# description choice
def description_choice(chart_datas):
    
    group_sum_datas=group_sum_data(chart_datas)
    desc = st.selectbox(
    'description(Total)', [i for i in lists])
    if desc=="All":
        group_sum_datas
    else:
        group_sum_datas.loc[desc]  

    check=st.checkbox('Show me the Scatter Graph')
    check2=st.checkbox('Show me the Line Graph')
    check3=st.checkbox('Show me the Bar Graph')
    check4=st.checkbox('Show me the Pie chart')

    return check, check2, check3, check4


# scatter chart
def scatter_chart(group_sum_datas,check):
    if  check and st.session_state.name:
        st.divider()
        check_color=st.checkbox("want to change a color?")    
        if check_color:
            colour1=st.color_picker("deposit color!","#0328fc")
            colour2=st.color_picker("withdrawls color!",'#fc0303')
            colour3=st.color_picker("margin color!",'#24fc03')
            st.scatter_chart(group_sum_datas,y=["deposit","withdrawls","margin"],color=[colour1,colour2,colour3])
        elif not check_color:
            st.scatter_chart(group_sum_datas,y=["deposit","withdrawls","margin"],color=['#0328fc','#fc0303','#24fc03'])
    elif check and not st.session_state.name:
        st.write("enter your name!")
    elif check and st.session_state.name!="jy":
        st.write("we don't have your info..")
    elif not check:
        st.write("")

# line chart
def line_chart(group_sum_datas,check2):
    if  check2 and st.session_state.name:
        st.line_chart(group_sum_datas[["deposit","withdrawls","margin"]])
    elif check2 and not st.session_state.name:
        st.write("enter your name!")
    elif check2 and st.session_state.name!="jy":
        st.write("we don't have your info..")
    elif not check2:
        st.write("")

# bar chart
def bar_chart(group_sum_datas,check3):
    if  check3 and st.session_state.name:
        st.bar_chart(group_sum_datas)
    elif check3 and not st.session_state.name:
        st.write("enter your name!")
    elif check3 and st.session_state.name!="jy":
        st.write("we don't have your info..")
    elif not check3:
        st.write("")


# pie chart
def pie_chart(group_sum_datas,check4):
    if  check4 and st.session_state.name:
        desc2 = st.radio(
        "What kind of description do you want to see?",
        [f"{i}" for i in lists])     
        group_positive=group_sum_datas.abs()   

        if desc2=="All":            
            fig,axs=plt.subplots(4,4,figsize=(15,15)) 
            for i, choice in enumerate(group_positive.index):                 
                axs[i//4,i%4].pie(group_positive.loc[choice],labels=group_positive.columns,autopct='%1.1f%%')
                axs[i//4,i%4].set_title(f"{choice}")      

            plt.tight_layout()
            st.pyplot(fig)

        else:
            fig, ax = plt.subplots()
            ax.pie(group_positive.loc[desc2],labels=group_positive.columns,autopct='%1.1f%%')
            ax.set_title(f"{desc2}")
            st.pyplot(fig)

    elif check4 and not st.session_state.name:
        st.write("enter your name!")
    elif check4 and st.session_state.name!="jy":
        st.write("we don't have your info..")

# implement all grouping functions
if file and session_name:
    check, check2, check3, check4=description_choice(chart_datas)
    group_sum_datas=group_sum_data(chart_datas)

    scatter_chart(group_sum_datas,check)
    line_chart(group_sum_datas,check2)
    bar_chart(group_sum_datas,check3)
    pie_chart(group_sum_datas,check4)

