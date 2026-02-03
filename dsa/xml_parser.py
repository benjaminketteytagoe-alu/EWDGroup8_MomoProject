import re
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime


xml_file = 'momo_sms.xml'
# DIR = 'momo_transactions'
file_path = xml_file

m_transfers = [
    {
        'name' : 'sending p2p',
        'pattern' : re.compile(r'\*165\*S\*(\d+)\s*RWF transferred to (.+?)\s*\((\d+)\).*?Fee was:\s*(\d+)\s*RWF.*?New balance:\s*(\d+)\s*RWF')
    },
    {
        'name' : 'receiving p2p',
        'pattern' : re.compile(r'You have received (\d+)\s*RWF from (.+?)\s*\(([\*\d]+)\).*?Your new balance:(\d+)\s*RWF.*?Financial Transaction Id:\s*(\d+)')
    }
]

cash_mngt = [
    {
        'name' : 'deposit',
        'pattern' : re.compile(r'\*113\*R\*A bank deposit of (\d+)\s*RWF has been added.*?NEW BALANCE\s*:(\d+)\s*RWF')
    },
    {
        'name' : 'withdrawal',
        'pattern' : re.compile(r'withdrawn (\d+)\s*RWF from your mobile money account.*?new balance:\s*(\d+)\s*RWF.*?Fee paid:\s*(\d+)\s*RWF.*?Financial Transaction Id:\s*(\d+)')
    }
]

payments = [
    {
        'name' : 'Merchants, the guys with code',
        'pattern' : re.compile(r'TxId:\s*(\d+)\.\s*Your payment of ([\d,]+)\s*RWF to (.+?)\s+(\d+)\s+has been completed.*?new balance:\s*([\d,]+)\s*RWF.*?Fee was (\d+)\s*RWF')
    },
    {
        'name' : 'Airtime',
        'pattern' : re.compile(r'\*162\*TxId:(\d+)\*S\*Your payment of (\d+)\s*RWF to Airtime.*?new balance:\s*(\d+)\s*RWF')
    },
    {
        'name' : 'water',
        'pattern' : re.compile(r'(?:You paid|Your payment of)\s*(\d+)\s*RWF for (?:WASAC|water).*?bill number\s*([\w-]+).*?new balance:\s*(\d+)\s*RWF')
    },
    {
        'name' : 'electricity',
        'pattern' : re.compile(r'Your payment of (\d+)\s*RWF to MTN Cash Power with token ([\d-]+).*?new balance:\s*(\d+)\s*RWF')
    }
]

financial_srvcs = [
    {
        'name': 'bank transfer to bank',
        'pattern': re.compile(r'You have transferred (\d+)\s*RWF to your (.+?)\s+(?:bank\s+)?account.*?new balance:\s*(\d+)\s*RWF')
    },
    {
        'name': 'bank transfer from bank',
        'pattern': re.compile(r'You have transferred (\d+)\s*RWF from your (.+?)\s+(?:bank\s+)?account.*?new balance:\s*(\d+)\s*RWF')
    },
    {
        'name': 'loan request',
        'pattern': re.compile(r'Your loan request of (\d+)\s*RWF has been credited to your Mobile Money account.*?new balance:\s*(\d+)\s*RWF')
    },
    {
        'name': 'loan repayment',
        'pattern': re.compile(r'You have repaid your MoKash loan of (\d+)\s*RWF.*?new balance:\s*(\d+)\s*RWF')
    },
    {
        'name': 'savings transfer',
        'pattern': re.compile(r'You have transferred (\d+)\s*RWF to your MoKash savings account.*?new balance:\s*(\d+)\s*RWF')
    }
]

other_services = [
    {
        'name': 'virtual card funding',
        'pattern': re.compile(r'You have funded your Virtual Card by MoMo with (\d+)\s*RWF.*?new balance:\s*(\d+)\s*RWF')
    },
    {
        'name': 'bulk payment received',
        'pattern': re.compile(r'(.+?)\s+has paid you (\d+)\s*RWF for (.+?)\..*?new balance:\s*(\d+)\s*RWF')
    },
    {
        'name': 'salary payment',
        'pattern': re.compile(r'(.+?)\s+has paid you (\d+)\s*RWF for salary.*?new balance:\s*(\d+)\s*RWF')
    }
]

Trns_types = {
    'MONEY_TRANSFER': m_transfers,
    'CASH_MANAGEMENT': cash_mngt,
    'PAYMENTS': payments,
    'FINANCIAL_SERVICES': financial_srvcs,
    'OTHER_SERVICES': other_services
}

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
        address = sms.get('address', '')
        body = sms.get('body', '')
        date = sms.get('date', '')
        readable_date = sms.get('readable_date', '')

        if address == 'M-Money':
            sms_data = {
                'address': address,
                'body': body,
                'date': date,
                'readable_date': readable_date
            }
            sms_list.append(sms_data)
    print(f"Extracted {len(sms_list)} M-Money SMS messages")
    return sms_list

def classify_transactions(sms_body):
    for keys, values in Trns_types.items():
        for i in values:
            pattern = i['pattern']
            match = pattern.search(sms_body)
            if match:
                sub_type = i['name']
                return (keys, sub_type, match, i)
    return ('UNKNOWN', None, None, None)

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
    
def extract_number(text):
    if not text:
        return None
    
    phone_pattern = r'\(([\*\d]+)\)'
    match = re.search(phone_pattern, text)
    
    if match:
        return match.group(1)
        
    return None

def extract_transaction_id(text):
    if not text:
        return None
    txid_pattern = r'(?:TxId\s*[:*]\s*|Financial Transaction Id\s*:\s*)(\d+)'
    match = re.search(txid_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def extract_timestamp(timestamp_ms):
    if not timestamp_ms:
        return ""
    try:
        timestamp_ms = int(timestamp_ms)
        timestamp_s = timestamp_ms / 1000
        dt = datetime.fromtimestamp(timestamp_s)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        print(f"Could not convert timestamp: {timestamp_ms} to datetime")
        return ""
    
def extract_recipient_sender(text):
    if not text:
        return None
    pattern = r'(?:from|to)\s+(.+?)\s+\('
    match = re.search(pattern, text)
    if match:
        name = match.group(1).strip()
        return name
    return None


def main():
    print("\n" + "="*40)
    print("MTN MOBILE MONEY TRANSACTION PARSER")
    print("="*40 + "\n")
    
    counts = {}
    
    sms_list = parse_xml_file(file_path)
    
    if not sms_list:
        print("No messages found. Exiting.\n")
        return
    
    
    
    all_transactions = []
    
    
    
    print(f"Processing {len(sms_list)} transactions...\n")
    
    for sms in sms_list:
        category, sub_type, match, pattern_info = classify_transactions(sms['body'])
        
        if category not in counts:
            counts[category] = 0
        counts[category] += 1

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
        
        
        if match and sub_type:
            groups = match.groups()
            
            if sub_type == 'sending p2p':
                transaction['amount'] = extract_amount(groups[0])
                transaction['recepient_sender'] = groups[1].strip()
                transaction['phone_number'] = groups[2]
                transaction['fee'] = extract_amount(groups[3])
                transaction['new_balance'] = extract_amount(groups[4])
            
            elif sub_type == 'receiving p2p':
                transaction['amount'] = extract_amount(groups[0])
                transaction['recepient_sender'] = groups[1].strip()
                transaction['phone_number'] = groups[2]
                transaction['new_balance'] = extract_amount(groups[3])
                transaction['transaction_id'] = groups[4]
            
            elif sub_type == 'deposit':
                transaction['amount'] = extract_amount(groups[0])
                transaction['new_balance'] = extract_amount(groups[1])
            
            elif sub_type == 'withdrawal':
                transaction['amount'] = extract_amount(groups[0])
                transaction['new_balance'] = extract_amount(groups[1])
                transaction['fee'] = extract_amount(groups[2])
                transaction['transaction_id'] = groups[3]
            
            elif sub_type == 'Merchants, the guys with code':
                transaction['transaction_id'] = groups[0]
                transaction['amount'] = extract_amount(groups[1])
                transaction['recepient_sender'] = groups[2].strip()
                transaction['phone_number'] = groups[3]
                transaction['new_balance'] = extract_amount(groups[4])
                transaction['fee'] = extract_amount(groups[5])
            
            elif sub_type == 'Airtime':
                transaction['transaction_id'] = groups[0]
                transaction['amount'] = extract_amount(groups[1])
                transaction['new_balance'] = extract_amount(groups[2])
                transaction['recepient_sender'] = 'Airtime'

            elif sub_type == 'water':
                transaction['amount'] = extract_amount(groups[0])
                transaction['description'] = f"Bill: {groups[1]}"
                transaction['new_balance'] = extract_amount(groups[2])
                transaction['recepient_sender'] = 'WASAC'

            elif sub_type == 'electricity':
                transaction['amount'] = extract_amount(groups[0])
                transaction['description'] = f"Token: {groups[1]}"
                transaction['new_balance'] = extract_amount(groups[2])
                transaction['recepient_sender'] = 'MTN Cash Power'

            elif 'bank transfer' in sub_type:
                transaction['amount'] = extract_amount(groups[0])
                transaction['recepient_sender'] = groups[1].strip()
                transaction['new_balance'] = extract_amount(groups[2])

            elif 'loan' in sub_type or sub_type == 'savings transfer':
                transaction['amount'] = extract_amount(groups[0])
                transaction['new_balance'] = extract_amount(groups[1])
                transaction['recepient_sender'] = 'MoKash'

            elif sub_type in ['bulk payment received', 'salary payment']:
                transaction['recepient_sender'] = groups[0].strip()
                transaction['amount'] = extract_amount(groups[1])
                transaction['description'] = groups[2]
                transaction['new_balance'] = extract_amount(groups[3])

            elif sub_type == 'virtual card funding':
                transaction['amount'] = extract_amount(groups[0])
                transaction['new_balance'] = extract_amount(groups[1])
                transaction['recepient_sender'] = 'Virtual Card'

        if not transaction['transaction_id']:
            transaction['transaction_id'] = extract_transaction_id(sms['body'])
            
        if not transaction['phone_number']:
            transaction['phone_number'] = extract_number(sms['body'])
        
        
        all_transactions.append(transaction)
    
    path = os.path.join('all_transactions.json')
    with open(path, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_transactions, jsonfile, ensure_ascii=False, indent=4)


   
    print("="*40)
    print("completed. transactions saved in: all_transactions.json")
    print("="*40 + "\n")

if __name__ == '__main__':
    main()
