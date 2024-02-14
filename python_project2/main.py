import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


# constant
font1 = {'family':'serif','color':'grey','size':50,'fontweight': 'bold'}
font2 = {'family':'serif','color':'lightblue','size':30,'fontweight': 'bold'}

# page title
st.header(":rainbow[# Welcome to the budget nagging🎈]",divider=True)
st.sidebar.markdown("# Main page 🎈")

# file path and name

def file_path(): 
    file=st.text_input("Input your file name and path!!",placeholder="/Users/jiyeon/무제 폴더/python_project2/1000_BT_Records.csv") 
    "/Users/jiyeon/무제 폴더/python_project2/1000_BT_Records.csv"
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

chart_datas=pd.DataFrame({"description":[1,2,3]})

if file and session_name:
    df=pd.read_csv(file)
    chart_datas=chart_data(df)
     

# full log

def full_log(chart_datas):
    if file and  st.session_state.name:
        chart_datas
    else:
        st.write("check the input values...")

    check1=st.checkbox("Full Log")
    if check1:
        full_log(chart_datas)

# group by time freqeuncy
def time_freq(chart_datas,freq):
    if  file and st.session_state.name:        
        b=chart_datas[["deposit","withdrawls","balance"]]
        b["margin"]=b["deposit"]-b["withdrawls"]      
        freq2=freq[0]
        b.index=b.index.asfreq(freq=freq2)   
        b=b.groupby(b.index).sum()
        # b is dataframe b.index is period index
        return b

    elif not st.session_state.name:
        st.write("enter your name!")
        return False
    elif st.session_state.name!="jy":
        st.write("we don't have your info..")
        return False
        

# line chart
def line_chart(b, check2):          
    if  check2 and st.session_state.name:    
        fig,axs=plt.subplots(1,1,figsize=(30,10)) 
  
        y=b[["deposit","withdrawls","balance","margin"]]
        
        axs.plot(y,linewidth=8.0,label=b.columns)
        # if want to hide xticks for day freq, use plt.xticks([])
        plt.title("Line Chart", fontdict=font1)
        plt.xlabel("Time Frequency",fontdict=font2)
        plt.ylabel("$",fontdict=font2,rotation=0)
        plt.tight_layout()
        plt.legend()
        st.pyplot(fig)            

    elif check2 and not st.session_state.name:
        st.write("enter your name!")
    elif check2 and st.session_state.name!="jy":
        st.write("we don't have your info..")


# bar chart
def bar_chart(b,check3):        
    if  check3 and st.session_state.name:       

        fig,ax=plt.subplots(1,1,figsize=(30,10))
        x=b.index

        ax.bar(x, b['deposit'].to_numpy(), label='Deposit', color='green')
        ax.bar(x, b['withdrawls'].to_numpy(),bottom=b['deposit'], label='Withdrawals', color='red')
        ax.bar(x, b['balance'].to_numpy(), bottom=b['deposit'] + b['withdrawls'],label='Balance', color='blue')
        ax.bar(x, b['margin'].to_numpy(), bottom=b['deposit'] + b['withdrawls']+b['balance'],label='Margin', color='yellow')
        

        plt.title("Bar Chart", fontdict=font1)

        plt.xlabel("Time Frequency",fontdict=font2)
        plt.ylabel("$",fontdict=font2,rotation=0)
        plt.legend()
    
        st.pyplot(fig)            
    
    elif check3 and not st.session_state.name:
        st.write("enter your name!")
    elif check3 and st.session_state.name!="jy":
        st.write("we don't have your info..")

# implement all grouping functions
if file and session_name:
    check4=st.checkbox("Group by Time Frequency")
    if check4:
        freq = st.selectbox('time frequency',['Month', 'Week', 'Day'])
        check2=st.checkbox('Show me the full Line Graph')
        check3=st.checkbox('Show me the full Bar Graph')
     
        try:
            b=time_freq(chart_datas,freq)
            if freq=="Month":
                b.index=b.index.strftime("%Y-%m")
            b
            if freq!="Month":
                b.index=b.index.to_timestamp()
        except Exception as e:
            st.write(e)
        else:
            line_chart(b,check2)
            bar_chart(b,check3)
    else:
        st.write("check the input values...")


    
    








