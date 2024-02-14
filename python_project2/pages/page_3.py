import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.ticker as ticker

# page title
st.header(":rainbow[# Data Summary❄️]",divider=True)
st.sidebar.markdown("# Data Summary❄️")

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
    {
        "date": pd.to_datetime(df["Date"]).dt.to_period(freq="D"),
        "description":df["Description"],
        "deposit":(df["Deposits"].str.replace(",","")).astype(float).round(),
        "withdrawls":(df["Withdrawls"].str.replace(",","")).astype(float).round(),
        "balance":(df["Balance"].str.replace(",","")).astype(float).round()
    }
)
    chart_data["date"]=chart_data["date"]
    chart_data["margin"]=chart_data["deposit"]-chart_data["withdrawls"]
    chart_desc=chart_data.describe().round()
    return chart_data, chart_desc


# total summary

def total_summary():
    check1=st.checkbox("Total Summary")
    if check1 and st.session_state.name:
        chart_desc
        st.download_button("Press to Download",chart_desc.to_csv(),"desc.csv","text/csv",key='download-csv')

        # histogram and gaussian fit 
        
        num_col=["deposit","withdrawls","balance","margin"]
        colors=["green","red","blue","yellow"]
        fig,ax=plt.subplots()
        bin_num=st.number_input(label="how many bins do you want?",min_value=1,step=1,value=6)
       
        _,bins,_=plt.hist(chart_data[num_col],bins=bin_num,density=True,label=chart_data.columns[2:],color=colors,alpha=0.6)


        for i,col in enumerate(num_col):
            mean = np.mean(chart_data[col])
            variance = np.var(chart_data[col])
            sigma = np.sqrt(variance)
            x = np.linspace(np.min(chart_data[col]), np.max(chart_data[col]), 100)
            plt.plot(x, norm.pdf(x, mean, sigma),color=colors[i])
        
        plt.title('probability density function')
        plt.xlabel("Money")
        plt.legend()
        left, right = plt.xlim()  

        min=chart_data[num_col].min(axis=None,numeric_only=True)
        max=chart_data[num_col].max(axis=None,numeric_only=True)
        plt.xticks(np.arange(start=min, stop=max, step=(max-min)//5))

        def thousand(x, pos):
            return f'{x:,.0f}$'

        ax.xaxis.set_major_formatter(thousand)
        st.pyplot(fig)


# customizing 
def custom(chart_data):
    check2=st.checkbox("Customize Summary!")
    chart_group=chart_data

    if check2 and st.session_state.name:
        option1 = st.selectbox(
        'Choose the standard group',
        ['date','description', 'deposit', 'withdrawls', 'balance','margin'])
        option2 = st.selectbox(
        'Choose the operation',
        ['Sum','Mean','Max','Min','Std'])

        chart_group=chart_data

        if option1=='date':
            chart_group.pop("description") 
            freqq=st.selectbox('Choose the period freq',['Month',"Week","Day"])   
            chart_group["date"]=chart_group["date"].dt.asfreq(freq=freqq[0])
            if freqq=="Month":
                chart_group["date"]=chart_group["date"].dt.strftime("%Y-%m")
        
        elif option1=='description':
            chart_group.pop("date")
        else:
            chart_group.pop("date")
            chart_group.pop("description")
        
        chart_group=chart_data.groupby(option1)
        
        chart_group=chart_group.apply(f"{option2.lower()}").round()
        st.write(f"Group by : :rainbow[#{option1}] // Operation : :rainbow[#{option2}]")
        
        chart_group
        st.download_button("Download Summary Data",chart_group.to_csv(),"custom_summary.csv","text/csv",key='download-csv2')

# implement all grouping functions
if file and session_name:
    df=pd.read_csv(file)
    chart_data, chart_desc=chart_data(df)
    total_summary()
    custom(chart_data)





