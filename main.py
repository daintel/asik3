import os
import csv
import json


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"File not found: {self.filename}")
            return False

    def create_output_folder(self, folder="output"):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder created: {folder}")
        else:
            print(f"Folder already exists: {folder}")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                self.students = list(reader)
                print(f"Data loaded successfully: {len(self.students)} students")
                return self.students
        except FileNotFoundError:
            print(f"File not found: {self.filename}")
            self.students = []
            return self.students

    def preview(self, n=5):
        print("First 5 rows:")
        print("-----------------------------")
        for row in self.students[:n]:
            print(
                row['student_id'], "|",
                row['age'], "|",
                row['gender'], "|",
                row['country'], "|",
                "GPA:", row['GPA']
            )
        print("-----------------------------")


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        gpas = []
        count = 0
        for row in self.students:
            gpas.append(float(row['GPA']))
        max_gpa = max(gpas)
        min_gpa = min(gpas)
        average_gpa = sum(gpas) / len(gpas)
        for gpa in gpas:
            if gpa > 3.5:
                count += 1
        self.result = {
            'Total students': len(self.students),
            "Highest GPA": max_gpa,
            "Lowest GPA": min_gpa,
            "Average GPA": average_gpa,
            "Student gpa>3.5": count
        }
    def print_results(self):
        print("-----------------------------")
        print("GPA Analysis")
        print("-----------------------------")
        for key, value in self.result.items():
            print(f"{key} : {value}")
        print("-----------------------------")


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, mode="w", encoding="utf-8") as f:
                json.dump(self.result, f, indent=4)
            print(f"Result saved to: {self.output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

fm = FileManager("students.csv")

if not fm.check_file():
    print("Stopping program.")
    exit()

fm.create_output_folder()

dl = DataLoader("students.csv")
dl.load()
dl.preview()

analyser = DataAnalyser(dl.students)
analyser.analyse()
analyser.print_results()

saver = ResultSaver(analyser.result, "output/result.json")
saver.save_json()