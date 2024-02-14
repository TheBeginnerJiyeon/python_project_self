# automaking decision making

from jikanpy import Jikan
import pandas as pd
import re

# not proper data
not_proper_data=[['Unknown'],[],None,""]

# basic keys and recomended keys
basic_keys=['title','genres','duration[num/min]','rating']
recommended_keys=['mal_id','url','title_english','title_japanese','type','source','episodes','status','airing','aired','score','rank','popularity','members','favorites','synopsis','season','year','demographics']


# when error or value range mismatch occurs
def min_max_error_prompt(min_val,max_val):
    if (min_val!=None) and (max_val!=None):
        print("enter the integer eqaul or btw {}-{}!".format(min_val,max_val))   
    elif min_val!=None:
        print("enter the integer equal or more than {}".format(min_val))
    elif max_val!=None:
        print("enter the integer equal or less than {}".format(max_val)) 
    else:
        print("there's no number limit. enter the right integer type of input!")


# make parent function for input number validation
def get_integer_input(what_number,min_val=None,max_val=None):
    print("min_value: ",min_val,"max_value: ",max_val)
    number=0
    while True:
        try:
            number=input("input the desired {} number!".format(what_number))
            if (number.isdigit()) and (((min_val==None)or(min_val<=int(number))) and ((max_val==None)or(int(number)<=max_val))):
                number=int(number)
                break
            else:
                min_max_error_prompt(min_val,max_val)

        except ValueError as v:
            print(v)
            min_max_error_prompt(min_val,max_val)
        except Exception as e:
            print(e)
            min_max_error_prompt(min_val,max_val)
    return number

# input sample anime number
def sample_num():
    sample_number=get_integer_input("sample",min_val=1)
    return sample_number

# input key number you want to know about anime. 4 keys are builtin.
def sorted_keys_num(keys):
    print("total key number is ",len(list(keys)),". you have 4 basic keys in the first place.")
    key_num=get_integer_input("sorted key",min_val=0,max_val=len(list(keys))-4)
    return key_num

# make not modified anime list and dictionary. dictionary don't have duplicate value. anime does. 
def original_anime_and_dict(sample_number,jikan,dictionary,animes,keys):
    for i in range(sample_number):
        while True:
            try:
                a=jikan.random(type='anime')['data']
                animes.update({i+1:a})
                for key in keys:
                    if a[key] in dictionary[key]:
                        continue
                    else:
                        dictionary[key].append(a[key])
                break
            except Exception as e:
                print(e,"wait!")
                continue


# have the modified version of each 3 keys to insert to animes and dict later
def anime_copy(animes,sample_number):
    anime_modified_genres=animes.copy()
    anime_modified_themes=animes.copy()
    anime_modified_demographics=animes.copy()
    for i in range(sample_number):
        try:
            a=animes[i+1]['genres'][0]['name'] 
        except IndexError as e:
            anime_modified_genres[i+1]['genres']=[]
        else:
            anime_modified_genres[i+1]['genres']=a

        try:
            b=animes[i+1]['themes'][0]['name'] 
        except IndexError as e:
            anime_modified_themes[i+1]['themes']=[]
        else:
            anime_modified_themes[i+1]['themes']=b

        try:
            c=animes[i+1]['demographics'][0]['name'] 
        except IndexError as e:
            anime_modified_demographics[i+1]['demographics']=[]
        else:
            anime_modified_demographics[i+1]['demographics']=c 

    return anime_modified_genres, anime_modified_themes, anime_modified_demographics

# insert the modified value to animes{}
def modify_anime(sample_number,animes):
    
    anime_modified_genres, anime_modified_themes, anime_modified_demographics=anime_copy(animes,sample_number)

    for i in range(sample_number):
        animes[i+1]['genres']=anime_modified_genres[i+1]['genres']
        animes[i+1]['themes']=anime_modified_themes[i+1]['themes']
        animes[i+1]['demographics']=anime_modified_demographics[i+1]['demographics']

# insert the modified value to dict
def modify_dict(sample_number,dictionary):
    modified_genres=[]
    modified_themes=[]
    modified_demographics=[]

    for i in range(sample_number):       
        try:   
            a=dictionary['genres'][i][0]['name'] 
            if a not in modified_genres:
                modified_genres.append(a)
            else: 
                continue
        except:
            continue

    for i in range(sample_number):       
        try:   
            a=dictionary['themes'][i][0]['name'] 
            if a not in modified_themes:
                modified_themes.append(a)
            else: 
                continue
        except:
            continue

    for i in range(sample_number):       
        try:   
            a=dictionary['demographics'][i][0]['name'] 
            if a not in modified_demographics:
                modified_demographics.append(a)
            else: 
                continue
        except:
            continue

    dictionary.update({'genres':modified_genres})
    dictionary.update({'themes':modified_themes})
    dictionary.update({'demographics':modified_demographics})

# change the duration value to integer minutes. original form: [1 hr 30 min 30 sec per ep]
    
def time_to_min(lenght, time2):
    for i in range(lenght):
        for ii in range(len(time2[i+1])):
            if time2[i+1][ii]=='hr':
                time2[i+1][ii]=60
            elif time2[i+1][ii]=='min':
                time2[i+1][ii]=1
            elif time2[i+1][ii]=='sec':
                time2[i+1][ii]=1/60

    time3=time2.copy()

    for i in range(lenght):
        
        for ii in range(0,len(time2[i+1])-1,2):
            if ii==0:
                time3[i+1]=int(time2[i+1][ii])*(time2[i+1][ii+1])
            elif ii>=2:
                time3[i+1]=time3[i+1]+int(time2[i+1][ii])*(time2[i+1][ii+1])
    return time3


# change dictionary time to min
def dict_time(dictionary,keys):
    times=dictionary['duration']

    time2={}
    for i in range(len(times)):
        time2.update({i+1:[]})

    for i in range(len(times)):
        time=times[i].split()
        for ti in time:
            if ti in ['per','ep']:
                continue
            else:
                time2[i+1].append(ti)

    time3=time_to_min(len(times), time2)
    
    dictionary.pop('duration')
    dictionary['duration[num/min]']=time3
    keys.remove('duration')
    keys.append('duration[num/min]')  


# change animes time to min
def anime_time(sample_number,animes):   

    time2={}
    for i in range(sample_number):
        time2.update({i+1:[]})

    for i in range(sample_number):
        time=animes[i+1]['duration'].split()
        for ti in time:
            if ti in ['per','ep']:
                continue
            else:
                time2[i+1].append(ti)

    time3=time_to_min(sample_number,time2)

    for i in range(sample_number):
        animes[i+1].pop('duration')
        animes[i+1]['duration[num/min]']=time3[i+1]



# user sorting key dictionary
def sorted_dict(dictionary,keys):

    sort_dict={}
    sort_dict.update({'title':dictionary['title']})
    sort_dict.update({'genres':dictionary['genres']})
    sort_dict.update({'duration[num/min]':dictionary['duration[num/min]']})
    sort_dict.update({'rating':dictionary['rating']})
    key_num=sorted_keys_num(keys)

    for i in range(key_num):
        print("you have basic keys already: {}".format(basic_keys))
        print(keys)
        
        print("recommended keys: ",recommended_keys)
        while True:
            key=input("input the one key you want to know!")
            if key not in keys:
                print("input the right key!")
                continue
            elif key not in recommended_keys:
                print("you have to add not existing keys!")
                continue
            sort_dict.update({key:dictionary[key]}) 
            print(sort_dict)
            break 

    return sort_dict

# make data to dataFrame
def make_df(animes):
    animes_df=pd.DataFrame.from_dict(animes,orient='index')
    return animes_df

# make 'output.csv' csv file
def file_to_csv(anime_df):      
    anime_df.to_csv("output.csv")

# when result have no desired attribute([]) then suggest restart!!!here!!
def check_empty_result(current_df,next_key):
    if current_df[next_key].empty or current_df[next_key].all==[]:

        print("no {} are available. check the file or try again?".format(next_key))
        return False
    else:
        return True

# ready for filtering data and check if genre is not available
def remake_df(animes,dictionary,keys):
    original_df=make_df(animes)
    sort_dict=sorted_dict(dictionary,keys)
    print(sort_dict)
    sorted_keys=list(sort_dict.keys())
    print(sorted_keys)
    animes_df=original_df[sorted_keys]
    print(animes_df)
    file_to_csv(animes_df)   

    next_key='genres'
    current_df=animes_df    
    result=check_empty_result(current_df,next_key) 
    
    return animes_df, sort_dict,result

# input genre you want to watch
def genres_choice(animes_df,dictionary):  
    
    genre_input=""
    while True:
        genre_input=input("what kind of genres do you want to watch based on your mood? check the csv file.")    
        lower_dict=[s.lower() for s in dictionary['genres']]    
        if genre_input.lower() not in lower_dict:
            print("please enter the correct genre name!")
            continue
        break

    genre_choice=animes_df[animes_df['genres'].str.lower()==genre_input.lower()]
    file_to_csv(genre_choice)

    next_key='duration[num/min]'
    current_df=genre_choice
    result=check_empty_result(current_df,next_key) 

    return genre_choice,result

# input max duration you want
def duration_choice(genre_choice):
    print(genre_choice['duration[num/min]'])
    duration_input=0
    while True:
        try:
            print("how long do you want to watch?")            
            duration_input2=float(input("input the min float time"))
            duration_input=float(input("input the max float time"))
            if duration_input2>duration_input:
                print("you might input the value opposite? try again")
                continue
        except Exception as e:
            print(e, " enter the integer time[min]!")
            continue
        break

    genre_choice=genre_choice[(genre_choice['duration[num/min]'].notna()==True) & (genre_choice['duration[num/min]'].isin(not_proper_data)==False)] 

    genre_choice=genre_choice[(genre_choice['duration[num/min]']<=duration_input) & (genre_choice['duration[num/min]']>=duration_input2)]
    print(genre_choice)  
    dur_choice=genre_choice    
    file_to_csv(dur_choice)

    next_key='rating'
    current_df=dur_choice
    result=check_empty_result(current_df,next_key) 


    return dur_choice,result

# list element to unique
def list_uni(input):
    return list(set(input))

# input the rate you can watch
def rate_choice(dur_choice):

    print(dur_choice['rating'])
    rate_num=get_integer_input("rate",1)
    input_box=[]
    for i in range(rate_num):
        rate_input=input("input the available rating: ")
        
        rate_input=rate_input.strip().lower().replace(" ","")[:5]
        input_box.append(rate_input)
        input_box=list_uni(input_box)
        print("input box: ",input_box)

    rt_choice=dur_choice[(dur_choice['rating'].str.strip().str.lower().str.replace(" ","").str[:5]).isin(input_box)]
    file_to_csv(rt_choice)

    next_key="rating"
    current_df=rt_choice
    result=check_empty_result(current_df,next_key) 

    return rt_choice,result


# input the row num if data
def last_choice(rt_choice,animes,animes_df,sort_dict):
    keys=list(sort_dict.keys())
    print(rt_choice[keys])
    file_to_csv(rt_choice)
    data_num=get_integer_input("total anime data",1,len(animes))
    row_num_list=[]
    print("last choice!")
    for i in range(data_num):
        last_input=get_integer_input("data row",1,len(animes))
        row_num_list.append(last_input)
    row_num_list=list_uni(row_num_list)
    for i in range(len(row_num_list)):
        row_num_list[i]=row_num_list[i]-1    

    ls_choice=animes_df.iloc[row_num_list,:]
    file_to_csv(ls_choice)

    next_key='rating'
    current_df=ls_choice
    result=check_empty_result(current_df,next_key) 

    return ls_choice,result

# main function 
def main_start():
    print("anime auto decision making began...")
    jikan=Jikan()
    keys=list(jikan.random(type='anime')['data'].keys())
    result=True
    
    dictionary={}
    for i in range(len(keys)):
        dictionary.update({keys[i]:[]})
    animes={}
    
    sample_number=sample_num()
    original_anime_and_dict(sample_number,jikan,dictionary,animes,keys)
    modify_anime(sample_number,animes)
    modify_dict(sample_number,dictionary)
    dict_time(dictionary,keys) 
    anime_time(sample_number,animes)

    animes_df,sort_dict,result=remake_df(animes,dictionary,keys)
    if result==False:
        return False
    genre_choice,result=genres_choice(animes_df,dictionary)
    if result==False:
        return False
    dur_choice,result=duration_choice(genre_choice)
    if result==False:
        return False
    rt_choice,result=rate_choice(dur_choice)
    if result==False:
        return False
    ls_choice,result=last_choice(rt_choice,animes,animes_df,sort_dict)
    if result==False:
        return False
    print(ls_choice,"\n")
    return result

# main + loop exit function
# when reult==[](empty data), main_start() stops
# when result !=[](not empty data, main_start() fully completed), ask whether want to exit the decision making.
def until_true():  

    while True:  
        result=True
        exit_loop=False
        result=main_start()
        if result==False:
            continue
        else:            
            while True:        
                a=input("do you want to exit? enter (y/n)")
                pattern_y=re.compile("^y.*")
                pattern_n=re.compile("^n.*")
                if bool(pattern_y.match(a.lower())):
                    exit_loop=True
                    break
                elif bool(pattern_n.match(a.lower())):
                    exit_loop=False
                    break
                else:
                    print("enter the right answer!(y/n)")
                    continue

            if exit_loop==False:
                until_true() 
            elif exit_loop==True:
                break      

# when not imported as module, execute
if __name__=="__main__": 
    until_true()
