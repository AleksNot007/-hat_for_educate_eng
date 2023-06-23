import pandas as pd
import openpyxl as px
df1 = pd.read_excel('EnglishWords.xlsx', sheet_name=4)
randomrow = df1.sample(n=1)
print(randomrow)
columnNedeed = randomrow.iloc[0,0].lower()

"""sheets = df1.sheetnames
for sheet_name in sheets:
    print(sheet_name)
"""

def ChooseWord(part, word):
    df1 = pd.read_excel('EnglishWords.xlsx', sheet_name=part)
    randomrow = df1.sample(n=1)
    columnNedeed = randomrow.iloc[0,0].lower()
    columnCheck = randomrow.iloc[0,1]

data = {
    "English word": [],
    "Translate": []
}
english_word = ()
translate = ()
data["English word"].append(english_word)
data["Translate"].append(translate)
