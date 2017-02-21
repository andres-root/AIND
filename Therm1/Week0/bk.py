def naked_twins(self, values):
        # unit_values = [{box: values[box] for box in unit if len(values[box]) == 2} for unit in self.unitlist]
        unit_values = [{box: values[box] for box in unit} for unit in self.unitlist]
        # twin_values = [e for e in [
        #     {k: v for (k, v) in unit.items() if list(unit.values()).count(v) > 1}
        #     for unit in unit_values] if len(e) > 1
        # ]
        for unit in unit_values:
            # twins = [e for e in {k: v for (k, v) in unit.items() if list(unit.values()).count(v) > 1} if len(e) > 0]
            twins = {k: v for (k, v) in unit.items() if len(v) == 2 if list(unit.values()).count(v) > 1}
            if len(twins) > 0:
                # twin_boxes = [b for u in twins for b in list(u.keys())]
                twin_boxes = list(twins.keys())
                for k, v in twins.items():
                    for box in unit.keys():
                        if box not in twin_boxes:
                            values[box] = values[box].replace(v[0], '')
                            values[box] = values[box].replace(v[1], '')