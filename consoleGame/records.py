import csv
import os


class Records:

    def __init__(self, records_file: str, clever_enemies: int, dum_enemies: int, strategy: str) -> None:
        super().__init__()
        self.clever_enemies = clever_enemies
        self.dum_enemies = dum_enemies
        self.strategy = strategy
        self.records = []
        self.records_file = records_file
        self.read_scores()

    def read_scores(self) -> None:
        if not os.path.isfile(self.records_file):
            return

        with open(self.records_file) as f:
            self.records = list(csv.reader(f))

    def write_scores(self, row) -> None:
        with open(self.records_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def get_scores(self):
        return tuple(self.records)

    def add_score(self, score: int, win: bool = False, time: int = 0) -> None:
        row = [score, win, self.clever_enemies, time]
        self.records.append(row)
        # self.records = sorted(self.records, key=lambda x: -x[0])[:10]
        self.write_scores(row)
