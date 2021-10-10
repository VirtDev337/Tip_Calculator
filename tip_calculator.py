# encoding: utf-8
# Take input of the total amount
# input of number of people tipping
# input of percentage for tip
# calculate tip from total
# Change the percentage of tip per person
# Define the list variable for the values provided at the prompt and the list to hold the results
values = []
processed = []
split_option, rate_option = 0, 0
# Defines the welcome message, beginning of the message for input requests and tax
welcome = "\nWelcome to the Tip Calculator.\n------------------------------\nPlease refrain from entering anything but numbers and dollars.\nYou can end at any time by typing quit or q."
message = "\nPlease provide the"

necessary = {
    'bill' : f"{message} total amount of the bill: $ ",
    'party' : f"{message} size of your party: # ",
    'tip' : f"{message} percentage for the tip: % "
}
optional = {
            'obligation' : f"\n{message} percentage of each persons obligation (comma delimited, not to exceed 100%): % ",
            'service' : f"\n{message} quality of service which adjusts the tip up to 5% higher or lower(1-2 Poor, 3 Acceptable, 4 Good, 5 Great, 6+ Amazing): # ",
            'additional' : "\nWould you like to provide information for the options of obligation and service rating? y/n ",
            'which' : '\nWhich option would you like to define (split, rate or both): ',
            'again' : '\nWould you like to run the tip calculator again? y/n ',
        }
error_msgs = {
    'positive' : 'Positive numbers are required.\n',
    'numeric' : 'Please enter a numeric value.',
    'zero' : 'It is mathmatically impossible to split zero'
}

def intify(lst):   # Converts input into integers
    tmp = []
    for itm in lst:
        try:
            tmp.append(abs(int(itm)))
        except:
            # Runs if input is not converted to a integer.
            print(error_msgs['numeric'])
            tmp.append('error')
            return tmp
    # Return the converted list
    return tmp

def dictify(lst):   # Converts the list into a dictionary
    i = 0
    tmp = {}
    
    # Iterate over the list assigning both the key and the value
    while i < len(lst):
        tmp[f'item{i}'] = lst[i]
        i += 1
    return tmp

def listify(dct):   # Converts the dictionary into a list
    lst = []
    i = 0
    
    # Iterate over the dictionary appending the values to the list
    while i < len(dct):
        lst.append(dct[f'item{i}'])
        i += 1
    return lst

def verify(lst):   # Checks the values in the list for symbols and removing them
    
    # Ternary anonymous function that evaluates for a symbol and returns the symbol
    tern = lambda itm : ','if ',' in itm else '$' if '$' in itm else '%' if '%' in itm else 'q' if 'q' in itm else ''
    symb = ''
    
    # Convert the list into a dictionary
    dct = dictify(lst)   # Execution: Changes the list into a dictionary for processing
    
    # Iterate over the dictionary
    for i in dct:
        tmp = ''
        
        # Assign symb with the symbol in use
        symb = tern(dct[i])
        
        if 'q' in symb: exit(0)
        
        # If symb variable has anything other than an empty string
        if symb != '':
            
            # Assign tmp with the value without the symbol
            tmp = dct[i].replace(symb, '')
        else:
            
            # The value had no symbol, assign it to tmp
            tmp = dct[i]
        
        # Assign the value of tmp to dictionary in i key
        dct[i] = tmp
        
    return listify(dct)   # Execution: Return the list converted from the symbol-less dictionary

def get_int_input(key):   # Function to query user for the integer input
    value = 0
    if 'both' == key: key = 'service'
    
    # Since the message may be provided from either dictionary, key is evaluated and returns the proper message
    msg = necessary[key] if 'party' == key else optional[key]
    
    while value <= 0:
        
        # The input is requested outside of the try block in case a q is entered, otherwise execution would continue with an numeric error being returned
        value = input(msg).lower()
        if 'q' in value: exit(0)
        
        # Attempts to convert the value into an integer and catches any errors
        try: 
            value = int(value)
            
            # Should the value evaluate to negative, error.  abs wouldn't work well here because a converted value may not be the intended value 
            # (negative for a bad experience).
            if value < 0: 
                print(error_msgs['positive'])
        except:
            # Runs if input is not converted to a integer.
            print(error_msgs['numeric'])
        
    return value

def get_float_input(key):   # Function to query user for the float input
    value = -1

    # Since a tip of zero must be allowed, the compare bool variable is used for the while loop. It's value is based on the key evaluation
    # and then the value evaluation
    compare = value < 0 if 'tip' == key else value <= 0
    while compare:
        
        # The input is requested outside of the try block in case a q is entered, otherwise execution would continue with an numeric error being returned
        value  = input(necessary[key]).lower()
        if 'q' in value: exit(0)
        
        try:
            value = float(value)
            if value < 0: print(error_msgs['positive'])
        except:
            # Runs if input is not converted to a float.
            print(error_msgs['numeric'])

        compare = value < 0 if 'tip' == key else value <= 0
    return value

def get_list_input(key, lst):   #Function to query user for list of values
    error = 1
    while error:
        if 'both' == key:
            key = 'obligation'
        
        # Asks for list of input and splits into a list
        lst.append(input(optional[key]).lower().split(' '))
        
        # Remove symbols $, %, , from the input and convert each string into an integer
        lst[-1] = intify(verify(lst[-1]))   # Execution: Uses intify function to convert the dictionary returned by the verify function        
        
        if lst[-1] == 'error':
            error = 1
            lst.remove('error')
        else:
            error = 0

def get_necessary_values(require):   # Function to get and convert required input
    provided = 0.0
    
    # Backend formatting due to the variuous inputs necessary to run the program
    if 'party' == require:   # If party
        
        provided = get_int_input(require)   # Execution: Uses get_int_input to ask for the party value
    else:   # If tip or bill
        
        provided = get_float_input(require)   # Execution: Uses get_float_input to ask for the bill, tip and split values
    if 'tip' == require:
        if provided >= 1: provided *= 0.01
    return provided

def get_optional_values(opt, provd = []):   # Function to get and convert optional input by type
    both = False
    if opt == 'both':
        both = True
    
    # Backend formatting due to the variuous optional inputs necessary to run the program if chosen
    if both:
        get_list_input(opt, provd)   # Execution: Uses get_list_input to ask for the list of percentages
        return get_int_input(opt)   # Execution: Uses get_int_input to ask for the rating value
    
    if 'obligation' in opt:
        if provd[2] > 0:
            get_list_input(opt, provd)   # Execution: Uses get_list_input to ask for the list of percentages
        else:
            print(error_msgs['zero'])
    
    if 'service' in opt:
        
        return get_int_input(opt)   # Execution: Uses get_int_input to ask for the rating value

def optional_itms(answr = ""):  # Function to determine if additional features are requested
    so = 0
    ro = 0
    
    # Obtain what optional features to use
    answr = input(optional['which']).lower()
    if 'q' in answr: exit()
    
    # Set the both variable according to the answer so the answr variable can be used to pass the required syntax
    if answr == 'both':
        # Define the split_option and rate_option variables for option evaluation in calculate function
        so = ro = 1
        
        # Ask for the input for the option of obligation and service
        values.append(get_optional_values(answr, values))   # Execution: Uses the get_optional_values function to ask for values of the provided options
    if 'split' in answr: 
        answr = 'obligation'
        
        # Define the split_option variable for option evaluation in calulate function
        so = 1
        
        # Ask for the input for the option of obligation and store in values list
        get_optional_values(answr, values)   # Execution: Uses the get_optional_values function to ask for values for the split option
    if 'rate' in answr:
        answr = 'service'
        
        # Define the rate_option variable for option evaluation in calculate function
        ro = 1
        
        # Ask for the input for the option of service rating and store in values list
        values.append(get_optional_values(answr))   # Execution: Uses the get_optional_values function to ask for values for the rate option
    return so, ro

def rating_adjustment(tp, sr):   # Adjusts the tip according to the rate option
    # Condidtional to adjust the tip in the range of -.05 to .05 depending on service rating
    if sr >= 6:
        tp += .05
    elif sr == 5:
        tp += .03
    elif 5 > sr > 2:
        tp += .01
    elif sr == 2:
        tp -= .03
    elif sr <= 1:
        tp -= .05
    return tp

def split_tip(lst, ind_amt, tip, cost):   # Calculates the percetage of the tip according to the percentages provided
    cnt = 0
    
    # Iterate over the percentages provided from input
    for percentage in lst:
        cnt += 1
        
        # If percentage isn't a float, convert from previous type
        if not isinstance(percentage, float):
            percentage = float(percentage)
        
        # Multiply by .01 to provide proper decimal placement if not already a decimal
        if percentage >= 1: percentage *= .01
        
        # Get the portion of the tip specified by the percentage
        percentage *= tip
        
        # Add the amount of that portion of the tip to the new list
        ind_amt.append(cost * percentage)
    return cnt

def calculate(lst):   # Funcion to evaluate options and calculate accordingly
    # Define the variables necessary for this function
    total = []
    individual_amt = []
    cost = lst[0]   # This is the value of the bill
    tax = 0.10
    tx = cost * tax + cost
    party = lst[1]   # This is the value of the party size
    tip = lst[2]   # This is the value of the tip
    rating = 0
    # The index of the last item is the rate if both are chosen
    indx = -1
    
    # Evaluate and adjust tip obligation
    # This option is run first because it is the last item if both options are chosen
    if rate_option:
        # Optional service rating processed before total bill for adjustment
        # Assigns the iput for the rating evaluation to srv
        rating = lst[indx]
        
        # Modify indx to -2 if the rate option is utilized, changing the index in which split option may reside
        indx -= 1
        
        # As long as the srv has value
        if rating >= 0:
            # Evaluate the rating and return the modified tip to tip
            tip = rating_adjustment(tip, rating)
    
    # Add the total amount, with tax and tip, to the first index of total list
    if tip > 0:
        total.append(cost * tip)
        total.append(cost * tip + tx)
    else:
        total.append(0)
        total.append(tx)
    
    # The obligation option to split the tip
    if split_option:
        # count is to store the number of iterations, indicating whether the tip applied to all participants or if the rest are splitting the bill without tip
        count = 0
        tmp = tx
        
        # If lst index 3 has value or that the type of the value in it is a list
        if lst[indx] or isinstance(lst[indx], list):
            
            # Assign list index 3 value to per, reversed due to a reversal of input
            count = split_tip(lst[indx], individual_amt, tip, cost)
            
            ind_total = tx / party
            # Iterate over the new list and add that to the per person amount added to the total list
            for amt in individual_amt:
                total.append(ind_total + amt or 0)
                tmp -= (ind_total + amt)
            if count != party:   # If the tip is covered, what amount everyone else will pay
                total.append(tmp / (party - count))
    else:
        # Should a split tip not be requested, offer each persons portion
        # It is not greater than or equal to one because the total was already appended, which is one person's obligation
        if party > 1: total.append(total[1] / party)
    return total

def display(procd):   # The formatting of the output for the results
    # cnt provides a way to track which itm is being processed and what header, if any, to print
    cnt = 0
    for itm in procd:
        if not cnt:
            print("\nThe tip is: ")
        elif cnt == 1:
            print("\nThe total of your bill, including tax and tip, is: ")
        elif cnt == 2:
            if values[1] > 1: print("\nThe bill per person is: ")
        
        # Formats and prints each itm
        print('${:,.2f}'.format(itm))
        cnt += 1
    print("------------------------------------------------------------------\n")

########################################################################################################################################################
########################################################################################################################################################
#######################################################    MAIN PROCESS    #############################################################################
# The main loop that continues until the option not to continue is entered
# Execution: This is the beginning of the program
again = 1
while again:   # Loop to run the tip_calculator app again until chosen to exit.
    # Prints the welcome message
    print(welcome)
    
    # Runs through the necessary dictionary returning the values needed for the calculation
    for required in necessary:
        values.append(get_necessary_values(required))   # Execution:  For each required value, the get_necessary_values function is called
    
    # print(values)   # For testing value placement
    answr = ''
    # Queries whether to request info for the optional input
    answr = input(optional['additional']).lower()
    
    # Exit if the value contains q
    if 'q' in answr: exit(0)
    
    # If the above query contains y
    if "y" in answr:
        # Accesses the optional dictionary and returns the options chosen while storing the values in the optional dictionary
        split_option, rate_option = optional_itms()   # Execution:  For the options chosen, optional_items handle the allocation of values
    
    # Returns the calculated values of tip, bill and each individuals obligation of the bill
    processed = calculate(values)
    
    # Displays the calculated values
    display(processed)
    
    # Requests the user to decide if they wish to run it again
    answer = input(f"\n{optional['again']}").lower()
    
    if 'q' in answer or 'n' in answer:
        again = 0
        exit(0)
    else:
        # Zeroes all values for the next iteration
        values = []
        answr = ''
        split_option, rate_option = int(), int()
        processd = []
        answer = ''