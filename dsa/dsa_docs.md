#DSA Integration: Search Efficiency Reflection

##1. Comparative Analysis
In this implementation, we compared Linear Search against Dictionary Lookup using a dataset of transaction records. By measuring the execution time for 20 specific lookups, the following observations were made:

|       Algorithm       | Average Time Complexity |                  Performance Observation                    |
| :-------------------- | :---------------------- | :---------------------------------------------------------- |
| **Linear Search**     |        $O(n)$           | Time increases linearly with the number of transactions.    |
| **Dictionary Lookup** |        $O(1)$           | Retrieval time remains constant regardless of dataset size. |

---

## 2. Why is Dictionary Lookup faster?
The performance gap between the two methods is due to how data is accessed in memory:

* **Linear Search**: This method performs an exhaustive scan. It starts at the first index and compares the target ID against every element until a match is found. In the worst-case scenario (if the ID is at the very end or missing), the algorithm must perform $n$ comparisons.
* **Dictionary Lookup**: Python dictionaries utilize a **Hash Table**. When an ID is stored, a mathematical "hash function" converts the ID into a specific memory address (index). When searching, the computer re-hashes the ID and jumps directly to that address. This eliminates the need to "browse" through the data, resulting in nearly instantaneous retrieval.



---

## 3. Alternative Data Structures for Efficiency

### Binary Search Tree (BST) or AVL Tree
If the transactions need to be searched by a **range** (e.g., "find all IDs between 500 and 1000") rather than a specific key, a Balanced Binary Search Tree would be more efficient.
* **Efficiency**: $O(\log n)$
* **Benefit**: Keeps the data sorted, allowing for efficient range queries that a Dictionary cannot perform.

##Binary Search Implementation Snippet

def binary_search(trans_list, target_id):
    # Requirement: trans_list must be sorted by 'transaction_id'
    low = 0
    high = len(trans_list) - 1

    while low <= high:
        mid = (low + high) // 2
        # Accessing the ID at the midpoint
        mid_id = trans_list[mid]['transaction_id']

        if mid_id == target_id:
            return trans_list[mid] # Record found
        elif mid_id < target_id:
            low = mid + 1 # Search the upper half
        else:
            high = mid - 1 # Search the lower half
            
    return None # Record not found
