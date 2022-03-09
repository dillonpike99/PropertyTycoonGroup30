from openpyxl import load_workbook

class Parser:

    def __init__(self):
        wb = load_workbook("Data/PropertyTycoonBoardData.xlsx")
        self.sheet = wb["Sheet1"]

    def getData(self):
        columns = ["A", "B", "D", "F", "H", "I", "K", "L", "M", "N", "O"]
        tiles = []
        for i in range(5, 45):
            values = []
            for j in columns:
                values.append(self.sheet[f"{j}{i}"].value)
                if j == "F" and values[-1] == "No":
                    break
                elif j == "H":
                    if values[2] in ["Station", "Utilities"]:
                        break
            tiles.append(values)
        return tiles