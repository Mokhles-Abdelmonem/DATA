import pandas as pd






df = pd.read_csv("mydocs/test.csv", error_bad_lines=False,sep=',')
count_row, count_col = df.shape
count_null = df.isnull().values.sum().sum()
df.drop("Column 2", axis=1, inplace=True)
df.to_csv("mydocs/test.csv")
dupnum = df.info()

print("\n befor \n")
print()
print("\n after \n ")
print()
def test():
    print( 'test')

def test2():
    print( 'test2')

test = {'test':'blabla','test2':'blabla2'}
for key, val in test.items():
    key() # Here i want to call the function with the key name, how can i do so?