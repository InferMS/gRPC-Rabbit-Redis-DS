import matplotlib
matplotlib.use('TkAgg')  # o 'Qt5Agg'

import matplotlib.pyplot as plt

class terminal_service():
    def __init__(self):
        self.dict_pollution = dict()
        self.dict_wellness = dict()
        self.first = True
        self.data_points_pollution = {}
        self.data_points_wellness = {}
        self.colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
        self.color_index = 0
        self.fig, self.ax_pollution, self.ax_wellness = None, None, None

    def send_results(self, pollutionData, wellnessData, id_terminal):
        if self.first == True:
            self.fig, (self.ax_pollution,self.ax_wellness) = plt.subplots(2, 1, figsize=(8, 6))

        for x in pollutionData:
            id = x.id
            if id not in self.data_points_pollution:
                self.first = True
                self.data_points_pollution[id] = {'timestamps': [], 'coefficients': []}
            if x.timestamp in self.data_points_pollution[id]['timestamps']:
                index = self.data_points_pollution[id]['timestamps'].index(x.timestamp)
                self.data_points_pollution[id]['coefficients'][index] = x.coefficient
                continue
            self.data_points_pollution[id]['timestamps'].append(x.timestamp)
            self.data_points_pollution[id]['coefficients'].append(x.coefficient)
        if self.first==True:
            self.ax_pollution.clear()
        for id, data in self.data_points_pollution.items():
            timestamps = [ts.seconds for ts in data['timestamps']]
            color = self.get_color(id)
            self.ax_pollution.plot(timestamps, data['coefficients'], marker='o',
                                   label=f'ID {id}',
                                   color=color)


        if self.first == True:

            self.ax_pollution.set_title(f'Pollution, Terminal:{id_terminal}', loc="left",
                                        fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
            self.ax_pollution.legend()


        for x in wellnessData:
            id = x.id
            if id not in self.data_points_wellness:
                self.first = True
                self.data_points_wellness[id] = {'timestamps': [], 'coefficients': []}
            if x.timestamp in self.data_points_wellness[id]['timestamps']:
                index = self.data_points_wellness[id]['timestamps'].index(x.timestamp)
                self.data_points_wellness[id]['coefficients'][index] = x.coefficient
                continue
            self.data_points_wellness[id]['timestamps'].append(x.timestamp)
            self.data_points_wellness[id]['coefficients'].append(x.coefficient)

        if self.first==True:
            self.ax_wellness.clear()
        for id, data in self.data_points_wellness.items():
            timestamps = [ts.seconds for ts in data['timestamps']]
            color = self.get_color(id)
            self.ax_wellness.plot(timestamps, data['coefficients'], marker='o',
                                  label=f'ID {id}',
                                  color=color)
        if self.first == True:

            self.ax_wellness.set_title(f'Wellness, Terminal:{id_terminal}', loc="left",
                                       fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
            self.ax_wellness.legend()

            self.first = False

        plt.tight_layout()
        plt.draw()
        plt.pause(2)

    def get_color(self, id):
        if id in self.dict_pollution:
            return self.dict_pollution[id]
        else:
            color = self.colors[self.color_index]
            self.dict_pollution[id] = color
            self.color_index = (self.color_index + 1) % len(
                self.colors)
            return color

terminal_service = terminal_service()
