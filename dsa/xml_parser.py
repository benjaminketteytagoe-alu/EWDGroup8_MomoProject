import re
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

#raw xml file
xml_file = 'momo_sms.xml'
file_path = xml_file

#patterns for money transfers
m_transfers = [
    {
        'name' : 'Sending p2p',
        'pattern' : re.compile(r'\*165\*S\*([\d,]+)\s*RWF transferred to (.+?)\s*\((\d+)\).*?Fee was:\s*([\d,]+)\s*RWF.*?New balance:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name' : 'Receiving p2p',
        'pattern' : re.compile(r'You have received ([\d,]+)\s*RWF from (.+?)\s*\(([\*\d]+)\).*?Your new balance:?\s*([\d,]+)\s*RWF.*?Financial Transaction Id:\s*(\d+)', re.I)
    }
]

#patterns for cash management. Only for physical cash to momo or the other way round
cash_mngt = [
    {
        'name' : 'Deposit', #physical cash in
        'pattern' : re.compile(r'You have received ([\d,]+)\s*RWF from.*?Cash Deposit.*?new balance:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name' : 'Withdrawal', #physical cash out
        'pattern' : re.compile(r'(?:withdrawn|amount)\s*([\d,]+)\s*RWF.*?new balance:\s*([\d,]+)\s*RWF.*?Fee paid:\s*([\d,]+)\s*RWF', re.I)
    }
]

#patterns for bills, airtime, and merchant payments
payments = [
    {
        'name' : 'Code Payment',
        'pattern' : re.compile(r'(?:TxId:\s*(\d+)\.\s*Your payment of|[\*]164[\*]S[\*]Y\'ello,A transaction of)\s*([\d,]+)\s*RWF (?:to|by)\s+(.+?)\s+(?:(\d+)\s+has been completed|on your MOMO account).*?new balance:\s*([\d,]+)\s*RWF(?:\.\s*Fee was\s*([\d,]+))?', re.I)
    },
    {
        'name' : 'Bundles and Packs',
        'pattern' : re.compile(r'TxId[:\s*]*(\d+).*?payment of\s*([\d,]+)\s*RWF to\s*(.*?)\s*has been.*?new balance:\s*([\d,]+)'r'|'r'Umaze kugura\s*(.*?)\s*igura\s*([\d,]+)\s*(?:RWF|FRW)', re.I)
    },
    {
        'name' : 'Airtime',
        'pattern' : re.compile(r'\*162\*TxId:(\d+)\*S\*Your payment of ([\d,]+)\s*RWF to Airtime.*?new balance:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name' : 'Water bill',
        'pattern' : re.compile(r'(?:You paid|Your payment of)\s*([\d,]+)\s*RWF for (?:WASAC|water).*?bill number\s*([\w-]+).*?new balance:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name' : 'Electricity bill',
        'pattern' : re.compile(r'Your payment of ([\d,]+)\s*RWF to MTN Cash Power with token ([\d-]+).*?new balance:\s*([\d,]+)\s*RWF', re.I)
    }
]

#transactions between bank and momo accounts
financial_srvcs = [
    {
        'name' : 'Bank to moMo', 
        'pattern' : re.compile(r'\*113\*R\*A (bank) deposit of ([\d,]+)\s*RWF.*?NEW BALANCE\s*:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name': 'Reversal',
        'pattern': re.compile(r'Your transaction to (.*?)\s*\((\d+)\) with ([\d,]+)\s*RWF has been reversed.*?new balance is ([\d,]+)\s*RWF', re.I)
    },
    {
        'name': 'Momo to bank',
        'pattern': re.compile(r'You have transferred ([\d,]+)\s*RWF to your (.+?)\s+(?:bank\s+)?account.*?new balance:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name': 'Loan request',
        'pattern': re.compile(r'Your loan request of ([\d,]+)\s*RWF has been credited.*?new balance:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name': 'Loan repayment',
        'pattern': re.compile(r'You have repaid your MoKash loan of ([\d,]+)\s*RWF.*?new balance:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name': 'Savings transfer',
        'pattern': re.compile(r'You have transferred ([\d,]+)\s*RWF to your MoKash savings account.*?new balance:\s*([\d,]+)\s*RWF', re.I)
    }
]

#other trans: salary,virtual cards
other_services = [
    {
        'name': 'Virtual Card Funding',
        'pattern': re.compile(r'You have funded your Virtual Card by MoMo with ([\d,]+)\s*RWF.*?new balance:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name': 'Bulk Payment Received',
        'pattern': re.compile(r'(.+?)\s+has paid you ([\d,]+)\s*RWF for (.+?)\..*?new balance:\s*([\d,]+)\s*RWF', re.I)
    },
    {
        'name': 'Salary Payment',
        'pattern': re.compile(r'(.+?)\s+has paid you ([\d,]+)\s*RWF for salary.*?new balance:\s*([\d,]+)\s*RWF', re.I)
    }
]

#combine all into one dict 
Trns_types = {
    'MONEY_TRANSFER': m_transfers,
    'CASH_MANAGEMENT': cash_mngt,
    'PAYMENTS': payments,
    'FINANCIAL_SERVICES': financial_srvcs,
    'OTHER_SERVICES': other_services
}

#main parser engine
def parse_xml_file(file_path):
    print(f"Parsing XML file: {file_path}")
    
    if not os.path.exists(file_path):
        open(file_path, 'w').close()
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.parseError as e:
        print(f"Error parsing xml file: {e}")

    sms_list = []
    all_sms = root.findall('sms')
    print(f"Total SMS found: {len(all_sms)}")

    for sms in all_sms:
        # address = sms.get('address', '')
        #get only M-Money messages
        # if address == 'M-Money': 
        sms_data = {
            # 'address': address,
            'body': sms.get('body', ''),
            'date': sms.get('date', ''),
            'readable_date': sms.get('readable_date', '')
        }
        sms_list.append(sms_data)
    print(f"Extracted {len(sms_list)} M-Money SMS messages")
    return sms_list

# find out what kind of transaction a m-money is
def classify_transactions(sms_body):
    for keys, values in Trns_types.items():
        for i in values:
            pattern = i['pattern']
            match = pattern.search(sms_body)
            if match:
                sub_type = i['name']
                return (keys, sub_type, match, i)
    return ('UNKNOWN', None, None, None)

#get amount and convert to int
def extract_amount(amnt_str):
    if not amnt_str:
        return 0
    amnt_str=str(amnt_str)
    amnt_str = amnt_str.replace(',', '').strip()
    try:
        return int(amnt_str)
    except ValueError:
        print(f"Could not convert amount: {amnt_str} to int")
        return 0
    
#get phone numbers, even ones with ****
def extract_number(text):
    if not text:
        return None
    phone_pattern = r'\(([\*\d]+)\)'
    match = re.search(phone_pattern, text)
    return match.group(1) if match else None

#extract the id. Either TxID or financial Transacton Id
def extract_transaction_id(text):
    if not text:
        return None
    txid_pattern = r'(?:TxId\s*[:*]\s*|Financial Transaction Id\s*:\s*)(\d+)'
    match = re.search(txid_pattern, text, re.IGNORECASE)
    return match.group(1) if match else None

#convert timestamp into readable date and time
def extract_timestamp(timestamp_ms):
    if not timestamp_ms:
        return ""
    try:
        timestamp_s = int(timestamp_ms) / 1000
        dt = datetime.fromtimestamp(timestamp_s)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return ""
    
#get the name of the other party in the transaction
def extract_recipient_sender(text):
    if not text:
        return None
    pattern = r'(?:from|to)\s+(.+?)\s+\('
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None

def main():
    print("\n" + "="*40)
    print("MTN MOBILE MONEY TRANSACTION PARSER")
    print("="*40 + "\n")
    
    sms_list = parse_xml_file(file_path)
    
    if not sms_list:
        print("No messages found. Exiting.\n")
        return
    
    all_transactions = []
    print(f"Processing {len(sms_list)} transactions...\n")
    
    for sms in sms_list:
        # match text to the patterns
        category, sub_type, match, pattern_info = classify_transactions(sms['body'])
        
        
        # set ddetails needed for the database.
        transaction = {
            'date': extract_timestamp(sms['date']),
            'transaction_type': category,
            'sub_type': sub_type or 'Unknown',
            'amount': 0,
            'fee': 0,
            'new_balance': 0,
            'recepient_sender': '',
            'phone_number': extract_number(sms['body']),
            'transaction_id': extract_transaction_id(sms['body'])
        }
        
        """ get specific info based on the transaction type
        we're using the regex groups to extract needed details depending on the transaction"""
        if match and sub_type:
            groups = match.groups()
            
            if sub_type == 'Sending p2p':
                transaction['amount'] = extract_amount(groups[0])
                transaction['recepient_sender'] = groups[1].strip()
                transaction['phone_number'] = groups[2]
                transaction['fee'] = extract_amount(groups[3])
                transaction['new_balance'] = extract_amount(groups[4])
            
            elif sub_type == 'Receiving p2p':
                transaction['amount'] = extract_amount(groups[0])
                transaction['recepient_sender'] = groups[1].strip()
                transaction['phone_number'] = groups[2]
                transaction['new_balance'] = extract_amount(groups[3])
                transaction['transaction_id'] = groups[4]
            
            elif sub_type == 'Deposit':
                transaction['amount'] = extract_amount(groups[0])
                transaction['new_balance'] = extract_amount(groups[1])
            
            elif sub_type == 'Withdrawal':
                transaction['amount'] = extract_amount(groups[0])
                transaction['new_balance'] = extract_amount(groups[1])
                transaction['fee'] = extract_amount(groups[2])
            
            elif sub_type == 'Code Payment':
                transaction['transaction_id'] = groups[0] if groups[0] else None
                transaction['amount'] = extract_amount(groups[1])
                transaction['recepient_sender'] = groups[2].strip()
                transaction['phone_number'] = groups[3] if groups[3] else None
                transaction['new_balance'] = extract_amount(groups[4])
                transaction['fee'] = extract_amount(groups[5]) if groups[5] else 0
            
            elif sub_type == 'Airtime':
                transaction['transaction_id'] = groups[0]
                transaction['amount'] = extract_amount(groups[1])
                transaction['new_balance'] = extract_amount(groups[2])
                transaction['recepient_sender'] = 'Airtime'

            elif sub_type == 'Bundles and Packs':
                if groups[0]:
                    transaction['transaction_id'] = groups[0]
                    transaction['amount'] = extract_amount(groups[1])
                    transaction['recepient_sender'] = groups[2].strip()
                    transaction['new_balance'] = extract_amount(groups[3])
                else: 
                    transaction['recepient_sender'] = groups[4].strip() 
                    transaction['amount'] = extract_amount(groups[5]) 
                    transaction['new_balance'] = 0 

            elif sub_type == 'Water bill':
                transaction['amount'] = extract_amount(groups[0])
                transaction['description'] = f"Bill: {groups[1]}"
                transaction['new_balance'] = extract_amount(groups[2])
                transaction['recepient_sender'] = 'WASAC'

            elif sub_type == 'Electricity bill':
                transaction['amount'] = extract_amount(groups[0])
                transaction['description'] = f"Token: {groups[1]}"
                transaction['new_balance'] = extract_amount(groups[2])
                transaction['recepient_sender'] = 'MTN Cash Power'

            elif sub_type in ['Bank to moMo', 'Momo to bank']:
                if sub_type == 'Bank to moMo':
                    transaction['recepient_sender'] = groups[0].strip() 
                    transaction['amount'] = extract_amount(groups[1]) 
                    transaction['new_balance'] = extract_amount(groups[2])
                else:
                    transaction['amount'] = extract_amount(groups[0])
                    transaction['recepient_sender'] = groups[1].strip()
                    transaction['new_balance'] = extract_amount(groups[2])
            
            elif sub_type == 'Reversal':
                transaction['recepient_sender'] = groups[0].strip()
                transaction['phone_number'] = groups[1]
                transaction['amount'] = extract_amount(groups[2])
                transaction['new_balance'] = extract_amount(groups[3])

            elif sub_type in ['Loan request', 'Loan repayment', 'Savings transfer']:
                transaction['amount'] = extract_amount(groups[0])
                transaction['new_balance'] = extract_amount(groups[1])
                transaction['recepient_sender'] = 'MoKash'

            elif sub_type in ['Bulk Payment Received', 'Salary Payment']:
                transaction['recepient_sender'] = groups[0].strip()
                transaction['amount'] = extract_amount(groups[1])
                transaction['description'] = groups[2] 
                transaction['new_balance'] = extract_amount(groups[3])

            elif sub_type == 'Virtual Card Funding':
                transaction['amount'] = extract_amount(groups[0])
                transaction['new_balance'] = extract_amount(groups[1])
                transaction['recepient_sender'] = 'Virtual Card'

        #check again for Id and phone number. They are importanat
        if not transaction['transaction_id']:
            transaction['transaction_id'] = extract_transaction_id(sms['body'])
            
        if not transaction['phone_number']:
            transaction['phone_number'] = extract_number(sms['body'])
        
        all_transactions.append(transaction)
    
    #save all the transactions to one json file
    path = os.path.join('all_transactions.json')
    with open(path, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_transactions, jsonfile, ensure_ascii=False, indent=4)

    print("="*40)
    print("completed. transactions saved in: all_transactions.json")
    print("="*40 + "\n")

if __name__ == '__main__':
    main()
