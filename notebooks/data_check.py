from pathlib import Path

import pandas as pd


# 현재 파일 위치:
# SNU_2026/notebooks/data_check.py
#
# parents[1]을 사용하면 SNU_2026 폴더를 찾을 수 있다.
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"

TRAIN_PATH = DATA_DIR / "train.csv"
TEST_PATH = DATA_DIR / "test.csv"
SUBMISSION_PATH = DATA_DIR / "sample_submission.csv"


def check_file(path: Path) -> None:
    """파일 존재 여부와 경로를 출력한다."""
    print(f"{path.name}: {path.exists()}")
    print(f"경로: {path}")


def main() -> None:
    print("=" * 60)
    print("프로젝트 폴더:", PROJECT_DIR)
    print("데이터 폴더:", DATA_DIR)
    print("=" * 60)

    check_file(TRAIN_PATH)
    check_file(TEST_PATH)
    check_file(SUBMISSION_PATH)

    required_files = [TRAIN_PATH, TEST_PATH, SUBMISSION_PATH]

    missing_files = [
        path.name
        for path in required_files
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "다음 파일을 data 폴더에 넣어주세요: "
            + ", ".join(missing_files)
        )

    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)
    submission_df = pd.read_csv(SUBMISSION_PATH)

    print("\n[데이터 크기]")
    print("train:", train_df.shape)
    print("test:", test_df.shape)
    print("sample_submission:", submission_df.shape)

    print("\n[train.csv 컬럼]")
    print(train_df.columns.tolist())

    print("\n[test.csv 컬럼]")
    print(test_df.columns.tolist())

    print("\n[sample_submission.csv 컬럼]")
    print(submission_df.columns.tolist())

    print("\n[train.csv 앞부분]")
    print(train_df.head())

    print("\n[train.csv 결측값]")
    print(train_df.isnull().sum())

    print("\n[test.csv 앞부분]")
    print(test_df.head())

    print("\n[sample_submission.csv 앞부분]")
    print(submission_df.head())


if __name__ == "__main__":
    main()