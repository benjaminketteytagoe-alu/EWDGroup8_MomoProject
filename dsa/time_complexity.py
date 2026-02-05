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

    # Linear and dictionary search table 
       
    print("Searching.. Time taken is in micro seconds (µs)")
    print("===================================================================")
    print("ID                 Linear Search Time      Dictionary Search Time")
    print("===================================================================")

    found = 0
    not_found = []
    l_time = []
    d_time = []

    for id in ids:
        # Linear search through IDs with time recorded in micro seconds
        start_linear = time.perf_counter()
        search = linear_search(trans_list= trans_list, id= id)
        stop_linear = time.perf_counter() - start_linear
        l_time.append(stop_linear * 1_000_000)
        
        # Dict search for through IDs with time recorded in micro seconds
        d_start = time.perf_counter()
        srch = dict_search(id= id)
        d_stop = time.perf_counter() - d_start
        d_time.append(d_stop * 1_000_000)

        # accounting for IDs that are found and not found during the search    
        if srch and search:
            found += 1
        else:
            not_found.append(id)          
        print(f"{id}          {stop_linear * 1_000_000:8.2f} µs             {d_stop * 1_000_000:8.2f} µs")
    print(f"Found {found} / {len(ids)}. Not found: {not_found}")    
    
    # summary section 
    l_average = sum(l_time) / len(l_time)
    d_average = sum(d_time) / len(d_time)
    print("=========================================")
    print(f"Average Linear Search Time: {l_average:.2f} µs")
    print(f"Average Dictionary Search Time: {d_average:.2f} µs")
    print("=========================================")


if __name__ == "__main__":
    main()
