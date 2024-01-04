import csv
import os

header: list = [
    "name",
    "regno",
    "email",
    "password",
    "phone",
    "receiptno",
    "uniqid",
    "sequence",
    "current_question",
]


def check_if_exists_in_directory(file_or_folder_name: str, directory: str = "") -> bool:
    current_working_dir = os.getcwd()
    try:
        if directory:
            os.chdir(directory)
        return file_or_folder_name in os.listdir()
    except FileNotFoundError:
        return False
    finally:
        os.chdir(current_working_dir)


def write_to_csv(data: dict, row, filename: str = "spaceRegistrations.csv"):
    global header
    file_exists = check_if_exists_in_directory(filename)
    with open(filename, "a") as csv_file_obj:
        csv_write = csv.writer(csv_file_obj, delimiter=",", lineterminator="\n")
        if file_exists:
            csv_write.writerow(row)
        else:
            csv_write.writerow(header)
            csv_write.writerow(row)


def check_user_exists_in_csv(
    regno: str, uniqid: str, filename: str = "spaceRegistrations.csv"
):
    if not check_if_exists_in_directory(filename):
        return False
    else:
        with open(filename, "r") as csv_file_obj:
            csv_reader = csv.DictReader(csv_file_obj)
            for row in csv_reader:
                if regno == row["regno"]:
                    return True
                elif uniqid == row["uniqid"]:
                    return True
            return False
