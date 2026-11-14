from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser
import re


DATA_SET_RE = re.compile(r"^\[\*\]\s+Read\s+(\w+(?:\s+\w+)?)\s+\((\d+)\s+found,\s+starting\s+at\s+address\s+(\d+)\)(?:\s+\[Device:\s*\d+\])?$")


class Parser(BaseParser):
    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            facts = self._parse_data_set(match)
            if not facts:
                continue

            for mp in self.mappers:
                source = facts.get(mp.source)
                target = facts.get(mp.target)

                if mp.edge and (source == None or target == None):
                    continue

                relationships.append(
                    Relationship(
                        source=Fact(mp.source, source),
                        edge=mp.edge,
                        target=Fact(mp.target, target),
                    )
                )
        return relationships

    @staticmethod
    def _parse_data_set(line):
        facts = {}
        m = DATA_SET_RE.fullmatch(line.strip())
        if not m:
            return facts

        section_type = m.group(1).lower()
        count = m.group(2)
        start_address = m.group(3)

        if 'coil' in section_type:
            register_type = "coil"
        elif 'discrete input' in section_type:
            register_type = "discrete_input"
        elif 'holding register' in section_type:
            register_type = "holding_register"
        elif 'input register' in section_type:
            register_type = "input_register"
        else:
            register_type = section_type

        facts[f"modbus.{register_type}.count"] = count
        facts[f"modbus.{register_type}.start_address"] = start_address
        
        return facts