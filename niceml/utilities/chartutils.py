from typing import List, Optional
from nicegui import ui
import pandas as pd


class Chart:
    def __init__(
            self,
            source,
            metric,
            name_list
    ):
        self.source = source
        self.metric = metric
        self.name_list = name_list
        self.chart = None
    def generate_chart(self) -> None:

        self.chart = ui.chart(options={
            'chart': {
                'type': 'line'
            },
            'title': {
                'text': self.metric
            },
            'xAxis': {
                'title': 'epoch'
            },
            'yAxis': {
                'title': self.metric
            },
            'plotOptions': {
                'line': {
                    'marker': {
                        'enabled': True
                    }
                }
            },
            'series': [{
                'name': name,
                'data': [
                    [self.source[self.source["name"] == name]["epoch"][idx],
                     self.source[self.source["name"] == name][self.metric][idx]
                     ]
                for idx in range(len(self.source[self.source["name"] == name]))]
            } for name in self.name_list]
        }).classes("w-full object-center")
        self.chart.update()


