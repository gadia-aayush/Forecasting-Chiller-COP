## README- Forecasting-Chiller-COP


### **BRIEF DESCRIPTION:**

  - Basically when given CSV Sheet having Chiller Data comprising of Timestamps, Wet Bulb Temperature, Chiller Network CU % & Chiller COP and we have to find the different classes of Wet Bulb Temperature along with the Quadratic Equation Coeff. which is unique for each class, it is then when our program comes into picture.
  
  - In Version 1 of our Forecasting COP of Chiller Program basically we user are simply entering the duration gap / frequency it wants, it just enters the range viz minimum & maximum value. The program automatically computes the best possible freuency making sure that gap is such in each group atleast 10 records are there. 10 records are actually necessary for DIY3 for computing the Quadratic Coefficients.
  
  - After Finding the Frequency or the Duration Gap of Classes the Program makes an API Call to DIY3 after subsetting data as per class gaps and API returns the Quadratic Coeff's of that particular class & we map the Classes along with their Quadratic Coefficients & returns it as an Output in JSON.


-------------------------------------------------------------------------------------------------------------------


### **PREREQUISITES:**

  - written for LINUX Server.
  - written in  Python 3.6 .
  - supporting packages required- pandas, numpy, statistics, datetime, json, sys, requests.


-------------------------------------------------------------------------------------------------------------------


### **CLIENT-END FULFILMENTS:**

The below format must be followed for the successful running of the script:  

1. **File Path ::**
   - it must be a CSV File Path.
   - it must be passed in the second argument of sys.argv.
   
   ----------------------------------------------------------------------------------------------------------------
   
2. **CSV File Data ::**

    - Make sure that the 1st Column is Timestamps Data.
    - Make sure that the 2nd Column is Wet Bulb Temperature Data.
    - Make sure that the 3rd Column is Chiller Network CU % (with % written).
    - Make sure that the 4th Column is COP.

      ***NOTE :: Timestamps should have Date portion starting with Day.***
   
   ----------------------------------------------------------------------------------------------------------------   

3. **Input String ::**

    - it must be passed in the third argument of sys.argv. 
    - it must be passed as JSON String.

    - the inputs must be passed in a list, with the minimum frequency being the first argument of list & maximum frequency being the second argument of list.  
    
      ***NOTE :: Minimum Value then Maximum Value. DO FOLLOW THIS ORDER.***  
      
    - **the JSON String, alternatively the dictionary data structure should have the following Key Names::**  
        `a. input :: it must contain the range. Example :: {"input" : [0.1, 2]}`

        **CAUTION: The above Key Names are case-sensitive, so use exactly as written above.**

   ---------------------------------------------------------------------------------------------------------------


4. **Output String ::**  
    - it is passed as a JSON String.  
    - here the **Keys represent the Class and the Values of the Keys represents the Quadratic Coefficients viz unique for that particular class.**  
    - **Quadratic Coefficients viz in the list [a,b,c] are in the same order of (a, b ,c ) of (ax2 + bx + c).**  

-------------------------------------------------------------------------------------------------------------------	

### **OUTPUT SAMPLE:**
  -	Please refer the Output Screenshots Folder.
  

-------------------------------------------------------------------------------------------------------------------	

### **AUTHORS:**

  -	coded by AAYUSH GADIA.

   
					  

