import json
import time

# fetch transaction from the json file into a list here
with open('all_transactions.json', 'r') as file:
    trans_list = json.load(file)

# converting the list into a dictionary for dict_search
trans_dict = {} 

for item in trans_list:
    """transaction id is used as the keys in the dictionary"""
    key = item['transaction_id']
    trans_dict[key] = item


# Linear search engine
def linear_search(trans_list, id):
    for transaction in trans_list:
        if transaction['transaction_id'] == id:
            return transaction
    return None

# Dict search engine
def dict_search(id):
    return trans_dict.get(id)


def main():
    # more IDs can be added
    ids = ["13515849108", "15722120949", "26484890740", "74637643766", "74110530634", 
           "35751352205", "90362526943", "44149221556", "41602878997", "14739625447",
           "60173686359", "92109248895", "91472495825", "67819295386", "85850951309",
           "81424789154", "82008869453", "49470186297", "41885909187", "47955567230"]

    # Linear search for 20 transactions
    found = 0
    not_found = []
    start_linear = time.perf_counter()
    for id in ids:
        search = linear_search(trans_list= trans_list, id= id)
        if search:
            found += 1
        else:
            not_found.append(id)
    stop_linear = time.perf_counter() - start_linear
    print(f"Linear search for {len(ids)} transactions took an average of: {stop_linear/len(ids):.10f} seconds")
    print(f"We found: {found}, but didn't find: {len(not_found)}:")
    print(not_found)

    # Dictionary search for 20 transactions
    FOUND = 0
    NOT_FOUND = []
    start = time.perf_counter()
    for id in ids:
        srch = dict_search(id= id)
        if srch:
            FOUND += 1
        else:
            NOT_FOUND.append(id)
    stop = time.perf_counter() - start
    print(f"Dictionary search for {len(ids)} searches took an average of: {stop/len(ids):.10f} seconds")
    print(f"Dictionary search found: {FOUND}, but didn't find: {len(NOT_FOUND)}:")
    print(NOT_FOUND)

if __name__ == "__main__":
    main()

