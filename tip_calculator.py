# TODO  Take input of the total amount
# TODO  input of number of people tipping
# TODO  input of percentage for tip
# TODO  calculate tip from total
# TODO  Change the percentage of tip per person
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

def get_values(msg):
    # Function to get and convert input
    provided = 0.0
    provd = []
    # Backend formatting due to the variuous inputs necessary to run the program
    if necessary[1] in msg or optional[1] in msg:
        while provided == 0:
            # Asks for input and then converts to integer else prints error and re-asks until proper input provided
            try: 
                provided = int(input(msg))
            except:
                print("Non numeric values not permitted")
    elif optional[0] in msg:
        # Asks for list of input and splits into a list
        provd = input(msg).split(' ') 
        for prov in provd:
            # Converts input into integers and adds to provd list
            provd.append(int(prov))
            # Removes string version from provd list
            provd.remove(prov)
    else:
        while provided == 0.0:
            try:
                # Asks for input and converts to a float
                provided  = float(input(msg))
            except:
                # Runs if anything input is not converted to a float.
                print("Non numeric values not permitted")
            # If tip percentage option
            if necessary[2] in msg:
                    # Converts whole number to decimal
                    provided *= .01
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
    # Queries whether to request info for the optional input
    answr = input("\nWould you like to have the tip split: ")
    # If the above query contains y
    if "y" in answr or "Y" in answr:
        # Ask for the input for the option of obligation and store in values list
        values.append(get_values(message + msg_end(optional[0])))
        # Define the split_option variable for option evaluation in calulate function
        split_option = 1
    # Clear the answr variable for the next query and ask to rate the quality of service provided
    answr = ""
    answr = input("\nWould you like to rate the service: ")
    if "y" in answr or "Y" in answr:
        # Ask for the input for the option of srvc rate and add to the values list
        values.append(get_values(message + msg_end(optional[1])))
        # Define the rate_option variable for option evaluation in calculate function
        rate_option = 1

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
    
    # Evaluate and adjust tip obligation
    if rate_option:
        # Optional service rating processed before total bill for adjustment
        # Assigns the iput for the rating evaluation to srv
        srv = lst[4]
        # As long as the srv has value
        if srv >= 0:
            # Evaluate the rating and return the modified tip to tip
            tip = rating_adjustment(tip, srv)
    # Add the total amount, with tax and tip, to the first index of total list
    total.append(((cost * tip) + tx))
    
    if split_option:
        # If lst index 3 has value or that the type of the value in it is a list
        if lst[3] or isinstance(lst[3], list):
            # Assign list index 3 value to per
            per = lst[3]
            # Iterate over the list in per
            for p in per:
                # If p isn't a float, multiply by .01 to convert it and provide proper decimal placement
                if not isinstance(p, float):
                    p *= .01
                # Get the portion of the tip specified in this location of the list
                p *= tip
                # Add the amount of that portion of the tip to the new list
                individual_amt.append((cost * p))
            # Iterate over the new list and add that to the per person amount added to the total list
            for amt in individual_amt:
                total.append((tx / party) + amt or 0)
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
        print(itm)
        cnt += 1
    print("------------------------------------------------------------------\n")

print(welcome)
for nec in necessary:
    values.append(get_values(message + msg_end(nec)))
optional_itms()
processed = calculate(values)
display(processed)