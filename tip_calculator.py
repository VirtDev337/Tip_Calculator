# Take input of the total amount
# input of number of people tipping
# input of percentage for tip
# calculate tip from total
# Change the percentage of tip per person
# Define the list variable for the values provided at the prompt and the list to hold the results
values = []
processed = []
split_option, rate_option = 0, 0
# Define the list variable 'necessary' to provide expandability and ensure functionality
necessary = ["bill", "party", "tip"]
# Defines an optional part of the challenge, to divide the tip according to input and a service rating to adjust the tip
optional = ["obligation", "srvc rate"]
# Defines the welcome message, beginning of the message for input requests and tax
welcome = "\nWelcome to the Tip Calculator.\n------------------------------\nPlease refrain from entering anything but numbers and dollars.\n"
message = "\nPlease provide the "
tax = 0.10

def intify(lst):
    for itm in lst:
        # Converts input into integers and adds to lst list
        lst.append(int(itm))
        # Removes string version from lst list
        lst.remove(itm)
    return lst

def verify(lst):
    tmp = ''
    symbols = [',', '$', '%']
    for itm in lst:
        for symbol in symbols:
            if symbol in itm:
                for i in itm:
                    if symbol != i:
                        tmp = ''.join(tmp + i)
                    else:
                        break
                lst.append(tmp)
                lst.remove(itm)
    return lst

def get_values(msg):
    # Function to get and convert input
    provided = 0.0
    provd = []
    # Backend formatting due to the variuous inputs necessary to run the program
    if necessary[1] in msg or optional[1] in msg:   #if party or service rate option
        while provided <= 0:
            # Asks for input and then converts to integer else prints error and re-asks until proper input provided
            try: 
                provided = int(input(msg))
                if provided < 0: print("Positive numbers are required.\n")
            except:
                print("Please enter a numeric value.")
    elif optional[0] in msg:  # If tip split option
        # Asks for list of input and splits into a list
        provd = input(msg).split(' ')
        # Remove symbols $, %, , from the input
        provd = verify(provd)   # NOTE: Unsuccessful in adding filter for symbols
        # Convery each string into an integer
        provd = intify(provd)
    elif necessary[2] in msg:   # If tip
        provided = -1
        while provided < 0.0:
            try:
                # Asks for input and converts to a float
                provided  = float(input(msg))
                if provided < 0: print("Positive numbers are required.\n")
            except:
                # Runs if anything input is not converted to a float.
                print("Please enter a positive numeric value.")
        # Converts whole number to decimal
        if provided >= 1: provided *= .01
    else:
        while provided <= 0.0:
            try:
                # Asks for input and converts to a float
                provided  = float(input(msg))
                if provided < 0: print("Positive numbers are required.\n")
            except:
                # Runs if anything input is not converted to a float.
                print("Please enter a positive numeric value.")
    if provided > 0:
        # Return provided if it has a value
        return provided
    else:
        # Return the list provd if provided has no value
        return provd

def msg_end(option): 
    # Set the end part of the message for input according to the option at the time
    if "bill" == option:
        return "total amount of the bill: "
    elif "party" == option:
        return "size of your party: "
    elif "tip" == option:
        return "percentage for the tip: "
    elif "obligation" == option:
        return "percentage of each persons obligation (space delimited, not to exceed 100%): "
    elif "srvc rate" == option:
        return "quality of service (1-2 Poor, 3 Acceptable, 4 Good, 5 Great, 6+ Amazing): "

def optional_itms():
    so = 0
    ro = 0
    # Queries whether to request info for the optional input
    answr = input("\nWould you like to have the tip split: ")
    # If the above query contains y
    if "y" in answr or "Y" in answr:
        # Define the split_option variable for option evaluation in calulate function
        so= 1
        # Ask for the input for the option of obligation and store in values list
        values.append(get_values(message + msg_end(optional[0])))
    # Clear the answr variable for the next query and ask to rate the quality of service provided
    answr = ""
    answr = input("\nWould you like to rate the service: ")
    if "y" in answr or "Y" in answr:
        # Ask for the input for the option of srvc rate and add to the values list
        values.append(get_values(message + msg_end(optional[1])))
        # Define the rate_option variable for option evaluation in calculate function
        ro = 1
    return so, ro

def rating_adjustment(tp, sr):
    # Condidtional to adjust the tip in the range of -.02 to .02 depending on service rating
    if sr >= 6:
        tp += .02
    elif sr == 5:
        tp += .01
    elif sr == 2:
        tp -= .01
    elif sr <= 1:
        tp -= .02
    return tp

def split_tip(lst, ind_amt, tip, cost):
    cnt = 0
    # Iterate over the list in lst
    for l in lst:
        cnt += 1
        # If p isn't a float, convert from previous type
        if not isinstance(l, float):
            l = float(l)
        # Multiply by .01 to provide proper decimal placement
        if l >= 1: l *= .01
        # Get the portion of the tip specified in this location of the list
        l *= tip
        # Add the amount of that portion of the tip to the new list
        ind_amt.append(cost * l)
    return cnt

def calculate(lst):
    # Funcion to evaluate options and calculate accordingly
    # Define the variables necessary for this function
    total = []
    individual_amt = []
    cost = lst[0]
    tx = cost * tax + cost
    party = lst[1]
    tip = lst[2]
    per = []
    srv = 0
    indx = -1
    # Evaluate and adjust tip obligation
    if rate_option:
        # Optional service rating processed before total bill for adjustment
        # Assigns the iput for the rating evaluation to srv
        srv = lst[indx]
        # Modify indx to -2 if the rate option is utilized, changing the index in which split option may reside
        indx -= 1
        # As long as the srv has value
        if srv >= 0:
            # Evaluate the rating and return the modified tip to tip
            tip = rating_adjustment(tip, srv)
    # Add the total amount, with tax and tip, to the first index of total list
    if tip:
        total.append((cost * tip) + tx)
    else:
        total.append(tx)
    if split_option:
        count = 0       
        # If lst index 3 has value or that the type of the value in it is a list
        if lst[indx] or isinstance(lst[indx], list):
            # Assign list index 3 value to per, reversed due to a reversal of input
            count = split_tip(lst[indx], individual_amt, tip, cost)
            # Iterate over the new list and add that to the per person amount added to the total list
            ind_total = tx / party
            for amt in individual_amt:
                total.append(ind_total + amt or 0)
            if count != party:
                total.append(ind_total)
    else:
        # Should a split tip not be requested, offer each persons portion
        total.append(total[0] / party)
    return total

def display(procd):
    cnt = 0
    for itm in procd:
        if not cnt:
            print("\nThe total of your bill with tax and tip is: ")
        elif cnt == 1:
            print("\nThe bill per person is: ")
        print('%.2f', itm)
        cnt += 1
    print("------------------------------------------------------------------\n")

print(welcome)
for nec in necessary:
    values.append(get_values(message + msg_end(nec)))
split_option, rate_option = optional_itms()
processed = calculate(values)
display(processed)