# esa-obs-stats utility
# author: Michaela Honkova

import xmltodict
import pandas as pd
import pathlib
import math
import csv
import os


WORKING_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
DATA_DIRECTORY = WORKING_DIR.joinpath("obs-data")


def load_obs_file(file_path: pathlib.Path) -> list[dict]:

    with open(file_path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    observations = data_dict["ades"]["obsBlock"]["obsData"].get("optical", [])

    # If only one observation, convert it to a list for consistency
    if not isinstance(observations, list):
        observations = [observations]

    data = []
    for observation in observations:
        data.append(
            {
                "file": file_path.name,
                "trkSub": observation.get("trkSub"),
                "provID": observation.get("provID"),
                "permID": observation.get("permID"),
                "obsTime": observation.get("obsTime"),
                "mag": observation.get("mag"),
                "exp": observation.get("exp"),
            }
        )
    return data


def process_data(df: pd.DataFrame) -> list[dict]:

    def format_v_mag(v_mag):
        if math.isnan(v_mag):
            return ''
        else:
            return round(v_mag, 1)

    df[["trkSub", "provID", "permID"]] = df[["trkSub", "provID", "permID"]].fillna('')
    df["TARGET"] = df["trkSub"] + df["provID"] + df["permID"]
    df[["exp", "mag"]] = df[["exp", "mag"]].astype(float)

    records = []
    grouped = df.groupby(['TARGET'])
    for target, group in grouped:
        records.append(
            {
                "TARGET": ''.join(target),
                "V mag": format_v_mag(group["mag"].mean()),
                "Time on sky": round(group["exp"].sum(), 2),
                "Reported to the MPC?": 'Y',
            }
        )
    return records


def save_result_as_csv(records: list[dict], file_name: str = 'result.csv') -> None:
    keys = records[0].keys()
    with open(WORKING_DIR.joinpath(file_name), 'w+', newline='') as csv_file:
        dict_writer = csv.DictWriter(csv_file, keys, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(records)


def save_result_as_txt(records: list[dict], file_name: str = 'result.txt') -> None:
    with open(WORKING_DIR.joinpath(file_name), 'w+') as txt_file:
        header = "TARGET".ljust(15) + "V mag".ljust(7) + "Time on sky".ljust(12) + \
                 "Reported to the MPC?".ljust(20) + '\n'
        txt_file.write(header)
        txt_file.write("=" * 55 + '\n')
        for record in records:
            line = record["TARGET"].ljust(15) + str(record["V mag"]).ljust(7) + \
                   str(record["Time on sky"]).ljust(12) + record["Reported to the MPC?"].ljust(20) + '\n'
            txt_file.write(line)


if __name__ == "__main__":

    print("Running Esa Obs Stats.")
    print(f"Loading .xml files from /{DATA_DIRECTORY}/..")

    # Load
    data = []
    files = [f for f in DATA_DIRECTORY.iterdir() if f.is_file()]
    for file_path in files:
        file_data = load_obs_file(file_path)
        data.extend(file_data)

    print("Files loaded successfully.")
    print("Processing loaded data..")

    # Transform
    df = pd.DataFrame(data)
    data = process_data(df)
    df = pd.DataFrame(data)

    print("Processing done.")
    print("Writing the results..")

    # Save
    save_result_as_txt(data)

    print("Result file was written.")
    input("Press any key to exit...")
