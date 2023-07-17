from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):
    def parse(self, blob):
        relationships = []

        print(type(blob))
        # can we process just first line...?

        # obtain [#] #####
        for pid_line in self.line(blob):
            # process
            pid_val = pid_line.strip()

            for mp in self.mappers:
                relationships.append(
                    Relationship(source=Fact(trait=mp.source, value=pid_val), edge=mp.edge, target=Fact(mp.target, '')))

            exit

        return relationships