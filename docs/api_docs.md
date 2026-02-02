# **Transactions API Documentation**

## **Base URL**

```
http://localhost:3000/api/transactions
```

---

## **1. Create a Transaction**

**Endpoint:** `POST /api/transactions`  
**Method:** `POST`

### **Request Example:**

```json
{
  "user_id": 1,
  "category_id": 2,
  "transaction_type": "expense",
  "receipient_sender": "Amazon",
  "amount": 49.99,
  "fee": 0.0,
  "new_balance": 950.01
}
```

### **Response Example (Success - 201 Created):**

```json
{
  "message": "Transaction created successfully",
  "transaction_id": 3
}
```

---

## **2. Get All Transactions**

**Endpoint:** `GET /api/transactions`  
**Method:** `GET`

### **Response Example (Success - 200 OK):**

```json
[
  {
    "Txid": 1,
    "user_id": 1,
    "category_id": 2,
    "receipient_sender": "prince mukunzi",
    "amount": "5000.00",
    "fee": "100.00",
    "new_balance": "15000.00",
    "Tx_date": "Mon, 01 Jan 2024 12:00:00 GMT"
  },
  {
    "Txid": 2,
    "user_id": 2,
    "category_id": 5,
    "receipient_sender": "Eelaf Adam",
    "amount": "100000.00",
    "fee": "250.00",
    "new_balance": "500000.00",
    "Tx_date": "Mon, 01 Jan 2024 12:00:00 GMT"
  }
]
```

---

## **3. Get Transaction by ID**

**Endpoint:** `GET /api/transactions/{id}`  
**Method:** `GET`  
**Path Parameter:** `id` (Transaction ID)

### **Request Example:**

```
GET /api/transactions/2
```

### **Response Example (Success - 200 OK):**

```json
{
  "Txid": 2,
  "user_id": 2,
  "category_id": 5,
  "receipt_sender": "Eelaf Adam",
  "amount": "100000.00",
  "fee": "250.00",
  "new_balance": "500000.00",
  "Tx_date": "Mon, 01 Jan 2024 12:00:00 GMT"
}
```

---

## **4. Update Transaction**

**Endpoint:** `PUT /api/transactions/{id}`  
**Method:** `PUT`  
**Path Parameter:** `id` (Transaction ID)

### **Request Example:**

```json
{
  "user_id": 1,
  "category_id": 2,
  "transaction_type": "expense",
  "receipt_sender": "Claude",
  "amount": 90.99,
  "fee": 0.0,
  "new_balance": 950.01
}
```

### **Response Example (Success - 200 OK):**

```json
{
  "message": "Transaction updated successfully",
  "transaction_id": 3
}
```

### **Response Example (Error - 404 Not Found):**

When attempting to update a non-existent transaction (e.g., ID 4):

```
HTTP/1.1 404 NOT FOUND
Not Found
The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
```

---

## **Error Codes**

| Code | Status       | Description                                   |
| ---- | ------------ | --------------------------------------------- |
| 200  | OK           | Request succeeded (GET, PUT)                  |
| 201  | Created      | Resource created successfully (POST)          |
| 404  | Not Found    | Transaction ID does not exist                 |
| 5xx  | Server Error | Internal server error (not shown but implied) |

---

## **Notes:**

1. The API uses inconsistent field naming:
   - `receipient_sender` (in POST and GET all)
   - `receipt_sender` (in GET by ID and PUT)
   - `receiptender` (in failed PUT attempt)
