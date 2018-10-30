#!/usr/bin/env python3


##---------------------------------------------------------------------------------
#------------ FORECASTING Coefficient of Performance (COP) of a Chiller -----------
#VERSION No.    : 1
#VERSION Name   : Creating Classes & Mapping each to respective Quadratic Coefficients
##---------------------------------------------------------------------------------


# Importing Libraries
import pandas as pd
from statistics import *
from datetime import datetime
import numpy as np
import json
import requests
import sys


output_passed= {}
output_list= []


try: #File_Input
    file_path= str(sys.argv[1])
    df= pd.read_csv(file_path)
    
    
    try: #Class Duration Entered by User
        input_data= sys.argv[2]
        input_json= json.loads(input_data)
        x= df.iloc[0:,1]
        min_class_gap= float(input_json["input"][0])
        max_class_gap= float(input_json["input"][1])
            
        
        if (min_class_gap < max_class_gap): #Checking whether the max_class_gap is greater than min_class_gap or not
            
            try: #Finding Minimum & Maximum WBT    
                wbt_data= list(map(float, df.iloc[0:,1].tolist())) 
                wbt_data.sort()
                max_wbt= wbt_data[-1]
                min_wbt= wbt_data[0]
            
            
                try: #Computing Class Gap
                    
                    # Computing Class Gap as per User Input
                    for gap in np.arange(min_class_gap, max_class_gap, 0.1): 
                        score= 0
                        for temp_vals in np.arange(min_wbt, max_wbt, gap):
                            if (len(df.iloc[0:,1][(x >= temp_vals) & (x < (temp_vals + gap))]) < 10): #[0-10), [10-20)....
                                break
                            else:
                                score+=1
                                
                        if (round((max_wbt-gap-min_wbt)/gap, 0) <= score):
                            #print(round((max_wbt-gap-min_wbt)/gap))
                            final_gap= round(gap, 2)
                            #print(final_gap)
                            break
                        else:
                            continue
                            
                    
                    # Computing Class Gap as per Default Input
                    if (final_gap == ''):
                        for gap in np.arange(min_class_gap, max_class_gap*1.5, 0.1): 
                            score= 0
                            for temp_vals in np.arange(min_wbt, max_wbt, gap):
                                if (len(df.iloc[0:,1][(x >= temp_vals) & (x < (temp_vals + gap))]) < 10): #[0-10), [10-20)....
                                    break
                                else:
                                    score+=1
                                    
                            if (round((max_wbt-gap-min_wbt)/gap, 0) <= score):
                                #print(round((max_wbt-gap-min_wbt)/gap))
                                final_gap= round(gap, 2)
                                #print(final_gap)
                                break
                            else:
                                continue
                    
                    
                    try: #Computation Block-1 involving- Creating Class & Subsetting Dataframe 
                        xy_dict= {}
                        class_log= []
                        key= 0
                        for each_class in np.arange(min_wbt, max_wbt, final_gap):
                            if ((each_class+final_gap) < max_wbt):
                                x_ref= df.iloc[0:,1]
                                class_name= str(round(each_class, 2)) + "-" + str(round(each_class+final_gap, 2))
                                class_log.append(class_name)
                                x_rough= df.iloc[0:,2][(x_ref >= each_class) & (x_ref < (each_class + final_gap))].tolist()
                                x= [float(rec.split("%")[0]) for rec in x_rough ] 
                                y= df.iloc[0:,3][(x_ref >= each_class) & (x_ref < (each_class + final_gap))].tolist()
                                date_rough= df.iloc[0:,0][(x_ref >= each_class) & (x_ref < (each_class + final_gap))]
                                date_rough= pd.to_datetime(date_rough, dayfirst=True)
                                date= date_rough.dt.strftime("%m/%d/%Y_%H:%M").tolist()              
                                xy_dict[key]=[date,x,y]
                                key+= 1
                                
                        
                        try: #DIY3 Interaction & Values Fecthing
                            url = 'api url removed for privacy reasons'
                            class_coeff= []
                            x_final= []
                            x_min= []
                            x_max= []
                            final_score= 0
                            for each_class in xy_dict:   
                                data_send= {}
                                overall_data= {}
                                overall_data["kpi"]= "Y"
                                overall_data["inputvals"]= xy_dict[each_class][1][5]
                                overall_data["filepath"]= []
                                x_list= []
                                x_list.append(xy_dict[each_class][1])
                                x_list= np.array(x_list)
                                x_final.append(( np.max(x_list), np.min(x_list) ))
                                x_min.append(np.min(x_list))
                                x_max.append(np.max(x_list))
                                
                                for each_row in range(len(xy_dict[each_class][0])):
                                    class_data= {}
                                    class_data["Date"]= xy_dict[each_class][0][each_row]
                                    class_data["X"]= xy_dict[each_class][1][each_row]
                                    class_data["Y"]= xy_dict[each_class][2][each_row]
                                    overall_data["filepath"].append(class_data)
                                    
                                data_send["dataset"]= json.dumps(overall_data, ensure_ascii = 'False')
                                request_send = requests.post(url,data_send)
                                request_message= json.loads(request_send.text)
                                class_coeff.append(request_message["data"]["splits"])   
                                #print(request_message)
                                
                            range_vals= (np.min(np.array(x_max)) , np.max(np.array(x_min)))
                            
                            
                            try: #Computation Block-2 involving- Checking Which X Values falls within the Range
                                x_rough= df.iloc[0:,2].tolist()      
                                x_rough= [x.split("%")[0] for x in x_rough]  
                                x_unique= set(x_rough)
                                for x in x_unique:
                                    if ((range_vals[0] > np.float(x) > range_vals[1]) or (range_vals[0] < np.float(x) < range_vals[1])):
                                        forecast_x= np.float(x)
                                        break                                    
                                    else:
                                        continue
                                                         
                                try: #Computation Block-3 involving- Mapping Class with X's Peak Values & Quadratic Coeff's 
                                    reqd_dict= {}    
                                    for each_log in range(len(class_log)):
                                        reqd_dict[class_log[each_log]]= class_coeff[each_log]

                                    output_passed["status"]= "success"
                                    output_passed["message"]= ""
                                    output_passed["data"]= reqd_dict
                                    output_passed["code"]= 200    
                                    
                                     
                                except: #Computation Block-3 :: Error Handling
                                    output_passed["status"]= "error"
                                    output_passed["message"]= "Computation Block-3 Error while Mapping Class with X's Peak Values & Coeff"
                                    output_passed["data"]= ""
                                    output_passed["code"]= 401    
                            
                            
                            except: #Computation Block-2 :: Error Handling
                                output_passed["status"]= "error"
                                output_passed["message"]= "Computation Block-2 Error while Checking Which X Values falls within the Range"
                                output_passed["data"]= ""
                                output_passed["code"]= 401    
                            
                        
                        except: #DIY3 Interaction & Values Fecthing:: Error Handling
                            output_passed["status"]= "error"
                            output_passed["message"]= "Error while Fetching Values from DIY3"
                            output_passed["data"]= ""
                            output_passed["code"]= 401    
                        
                        
                    except: #Computation Block-1 :: Error Handling
                        output_passed["status"]= "error"
                        output_passed["message"]= "Computation Block-1 Error while Creating Class & Subsetting Dataframe"
                        output_passed["data"]= ""
                        output_passed["code"]= 401    
            
            
                except: #Class Duration:: Error Handling
                    output_passed["status"]= "error"
                    output_passed["message"]= "Error while computing Class Gap"
                    output_passed["data"]= ""
                    output_passed["code"]= 401              
                
            
            except: #Missing_Value_while_computing_Max_Min_WBT:: Error Handling
                output_passed["status"]= "error"
                output_passed["message"]= "CSV File contains Missing Data, Fix it"
                output_passed["data"]= ""
                output_passed["code"]= 401 
            
            
        else: #Min & Max Class Gap Comparison
            output_passed["status"]= "error"
            output_passed["message"]= "Make sure that Maximum Class Gap is greater than Minimum Class Gap, Example- [0.1, 2]"
            output_passed["data"]= ""
            output_passed["code"]= 401     

    
    except: #Class_Duration_Input:: Error Handling
        output_passed["status"]= "error"
        output_passed["message"]= ""
        output_passed["data"]= "Float not Entered"
        output_passed["code"]= 401

    
except: #File_Input:: Error Handling
    output_passed["status"]= "error"
    output_passed["message"]= "please provide the csv file path or check the file name entered"
    output_passed["data"]= ""
    output_passed["code"]= 401


# Very Important Line
output_json = json.dumps(output_passed, ensure_ascii = 'False')
print(output_json)




 #-----------------------------
 #|| written by AAYUSH GADIA ||
 #-----------------------------
    
