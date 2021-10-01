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
# Defines the beginning of the message and tax
message = "Please provide the "
tax = 0.10
# Function to get and convert input
def get_values(msg):
    provided = 0.0
    provd = []
    if necessary[1] in msg or optional[1] in msg:
        while provided == 0:
            try:
                provided = int(input(msg))
            except:
                print("Non numeric values not permitted")
    elif optional[0] in msg:
        provd = input(msg).split(' ')
        for prov in provd:
            provd.append(int(prov))
            provd.remove(prov)
    else:
        while provided == 0.0:
            try:
                provided  = float(input(msg))
                if necessary[2] in msg:
                    provided *= .01
            except:
                print("Non numeric values not permitted")
    if provided > 0:
        return provided
    else:
        return provd

def msg_end(option):
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
    answr = input("Would you like to have the tip split: ")
    if "y" in answr or "Y" in answr:
        values.append(get_values(message + msg_end(optional[0])))
        split_option = 1
    answr = ""
    answr = input("Would you like to rate the service: ")
    if "y" in answr or "Y" in answr:
        values.append(get_values(message + msg_end(optional[1])))
        rate_option = 1

def rating_adjustment(tp, sr):
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
    total = []
    individual_amt = []
    cost = lst[0]
    tx = cost * tax + cost
    party = lst[1]
    tip = lst[2]
    per = []
    srv = 0
    if split_option:
        if lst[3] or isinstance(lst[3], list):
            per = lst[3]
            for p in per:
            # figure tip per person based on percentage
                if not isinstance(p, float):
                    p *= .01
                p *= tip
                individual_amt.append((cost * p))
            for amt in individual_amt:
                total.append((tx / party) + amt or 0)
    elif rate_option:
        # Optional service rating processed before total bill for adjustment
        if lst[4]:
            srv = lst[4]
        if srv >= 0:
            tip = rating_adjustment(tip, srv)
    if not split_option:
        total.append(((cost * tip) + cost) + tx)
        total.append(total[0] / party)
    return total

def display(procd):
    for itm in procd:
        print(itm)


for nec in necessary:
    values.append(get_values(message + msg_end(nec)))
optional_itms()
processed = calculate(values)
display(processed)