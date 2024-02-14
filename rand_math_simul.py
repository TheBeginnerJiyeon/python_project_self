import random
import time
import operator

operations={"+":operator.add,"-":operator.sub,"*":operator.mul, "/":operator.truediv}
operations_keys=operations.keys()
keys_list=list(operations_keys)

def is_integer():
    while True:
        print("")    
        variable_num=input("Choose the variable + integer number to be calculated! 2 or more : " )
        print("")
        if variable_num=="":
            print('variable_num==""!! please enter some numeric value, not just pressing enter..',"\n")
        elif variable_num!=None and (variable_num[0]=="+"):
            print("variable_num!=None and (variable_num[0]=="+")","\n")            
            return (variable_num[1:]).isdigit(),variable_num            
        elif variable_num!=None and (variable_num[0]=="-"):
            print("You have to choose + side integer","\n")
        elif variable_num!=None:
            return variable_num.isdigit(), variable_num
        else:
            print("maybe you didn't enter anything!","\n")

def string_to_int(digit_string):    
    return int(digit_string)

def random_fnum_gen():    
    return round(random.uniform(0,10),2)

def random_oper_gen():    
    global keys_list
    i=random.randint(0,3)
    return operations[keys_list[i]],keys_list[i]

def return_vari_num():
    while True:
        is_dig, variable_num=is_integer()

        if is_dig:
            variable_num=string_to_int(variable_num)  
            if variable_num>=2:
                return variable_num                
        else:
            print("please enter the number type..")
            continue


def return_oper_history_by_two(variable_list):

    operation_history=[]
    result=0

    while True:        
        try:
            result_func,op_history_item=random_oper_gen()
            result=result_func(variable_list[0],variable_list[1])
            operation_history.append(op_history_item)
        except ZeroDivisionError as zd:
            print(zd,"other operator will be used")
            operation_history=[]
            result=0
            continue
        except Exception as e:
            print(e,"other operator will be used")
            operation_history=[]
            result=0
            continue
        else:            
            return operation_history, result, variable_list

         
def return_vari_list(variable_num):

    variable_list=[0 for i in range(variable_num)] 

    for i in range(variable_num):
        variable_list[i]=random_fnum_gen()
    return variable_list

def return_oper_history_by_three_more(variable_num,result,operation_history,variable_list):    

    if variable_num==2:
        result=round(result,2)
        return operation_history, result
    else:
        while True:
            try: #
                for i in range(2,variable_num):
                    result_func,op_history_item =random_oper_gen()
                    result=result_func(result,variable_list[i])
                    operation_history.append(op_history_item)
            except ZeroDivisionError as zd:
                print(zd,"other operator will be used")
                result_func=0
                op_history_item=0
                operation_history=[]
                result=0
                continue
            except Exception as e:
                print(e,"other operator will be used")
                result_func=0
                op_history_item=0
                operation_history=[]
                result=0
                continue
            else:
                return operation_history, result
               



def random_op_simul():
   
    variable_num=return_vari_num()     
    variable_list=return_vari_list(variable_num)

    operation_history,result,variable_list=return_oper_history_by_two(variable_list)        
    operation_history,result= return_oper_history_by_three_more(variable_num,result,operation_history,variable_list)    
        
    result=round(result,2)
    print("result: ",result,"\n")
    
    return variable_num, variable_list, operation_history,result



def make_expression():
    variable_num, variable_list, operation_history,result=random_op_simul()
    print("variable_list: ",variable_list,"\n")
    print("operation_history",operation_history,"\n")    
    print("variable num",variable_num,"\n")
    expression="({}{}{})".format(variable_list[0],operation_history[0],variable_list[1])
    if variable_num>=3:
        for i in range(variable_num-2):
            expression="({}{}{})".format(expression,operation_history[i+1],variable_list[i+2])

    return variable_list,operation_history,expression,result,variable_num

def time_cal():
    variable_list, operation_history,expression,result,variable_num=make_expression()
    start_time=time.time()    

    while True:
        try:
            user_input=float(input("The problem is this. {}=? enter the answer!".format(expression)))
            print("")
            if result==user_input:
                operation_history=[]
                variable_list=[]
                break   
            else:
                print("try again,,\n")

        except ValueError as ve:
            print(ve,"Maybe you didn't answer number? please try with number.\n")

        except Exception as ee:
            print(ee,"error happened!try again.\n")

    end_time=time.time()
    duration_time=end_time-start_time    
    duration_time=round(duration_time,2)
    
    print("congratulations! the solving time is {} seconds.\n".format(duration_time))


time_cal()










    

    
    


        


    
    