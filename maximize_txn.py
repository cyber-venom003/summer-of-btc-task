#Importing libraries
import pandas as pd
import os

#For relative file path (independent of platform)
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './mempool.csv')

#Opening mempool.csv file
mempool_file = open(filename , 'r')

#Converting CSV Data to pandas dataframe
mempool = pd.read_csv(mempool_file)

tx_id = []

def isNan(num):
    return num != num

#Sorting dataframe according to max fee and least weight
mempool = mempool.sort_values(by=['fee', 'weight'], ascending=[False,True])

## Calculation for valid transactions for maximizing fee start here
max_valid_tx = []
curr_weight = 0

for row in mempool.iterrows():
    tx = row[1].values
    tx_id.append(tx[0])

for row in mempool.iterrows():
    tx = row[1].values
    if isNan(tx[3]):
        if(curr_weight < 4000000):
            curr_weight = curr_weight + tx[2]
            max_valid_tx.append(tx[0])
        if(curr_weight >= 4000000):
            break
    else:
        parents = tx[3].split(';')
        count = 0
        for parent in parents:
            parent_txn = mempool.iloc[tx_id.index(parent)]
            if(curr_weight < 4000000):
                curr_weight = curr_weight + parent_txn[2]
                max_valid_tx.append(parent_txn[0])
            if(curr_weight >= 4000000):
                break
        if(curr_weight < 4000000):
            curr_weight = curr_weight + tx[2]
            max_valid_tx.append(tx[0])
        if(curr_weight >= 4000000):
            break

total_fee = 0

for row in mempool.iterrows():
    tx = row[1].values
    if tx[0] in max_valid_tx:
        total_fee = total_fee + tx[1]

#Printing maximum total fee possible
print("Maximum Fee for " + str(len(max_valid_tx)) + " valid transactions is " + str(total_fee) + " satoshies")

#Creating block.txt file
block = open('block.txt' , 'w')

#Writing result to block.txt file
for txn in max_valid_tx:
    block.write(txn)
    block.write('\n')

#Closing block.txt file
block.close()