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

    def write_scores(self) -> None:
        with open(self.records_file, 'w') as f:
            writer = csv.writer(f)
            for record in self.records:
                writer.writerow(record)
            # for record in self.records[:-1]:
            #     print(record, file=f)
            # print(self.records[-1], file=f, end='')

    def get_scores(self):
        return tuple(self.records)

    def add_score(self, score: int, win: bool = False, time: int = 0) -> None:
        self.records.append([score, win, self.clever_enemies, self.dum_enemies, self.strategy, time])
        # self.records = sorted(self.records, key=lambda x: -x[0])[:10]
        self.write_scores()
