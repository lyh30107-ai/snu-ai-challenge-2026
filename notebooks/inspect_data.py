from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"

train_df = pd.read_csv(DATA_DIR / "train.csv")
test_df = pd.read_csv(DATA_DIR / "test.csv")


# pandas가 열 내용을 생략하지 않도록 설정
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 200)
pd.set_option("display.width", 2000)


print("=" * 80)
print("[학습 데이터 첫 번째 샘플]")
print("=" * 80)

first_row = train_df.iloc[0]

for column in train_df.columns:
    print(f"\n{column}:")
    print(first_row[column])


print("\n" + "=" * 80)
print("[Answer 값 예시]")
print("=" * 80)
print(train_df["Answer"].head(20).to_string(index=False))


print("\n" + "=" * 80)
print("[Answer 종류 개수]")
print("=" * 80)
print("고유 Answer 수:", train_df["Answer"].nunique())
print(train_df["Answer"].value_counts().head(30))


print("\n" + "=" * 80)
print("[No_ordering 분포]")
print("=" * 80)
print(train_df["No_ordering"].value_counts())
print(train_df["No_ordering"].value_counts(normalize=True))


print("\n" + "=" * 80)
print("[Input 열의 데이터 타입과 예시]")
print("=" * 80)

input_columns = ["Input_1", "Input_2", "Input_3", "Input_4"]

for column in input_columns:
    print(f"{column} 타입: {type(first_row[column])}")
    print(f"{column} 값: {first_row[column]}")