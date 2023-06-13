import matplotlib.pyplot as plt

class terminal_service():
    def __init__(self):
        self.dict_pollution = dict()
        self.dict_wellness = dict()
        self.first = True
        self.data_points_pollution = {}  # Diccionario para almacenar los datos por ID
        self.data_points_wellness = {}  # Diccionario para almacenar los datos por ID

    def send_results(self, pollutionData, wellnessData, id_terminal):
        fig, (ax_pollution, ax_wellness) = plt.subplots(2, 1, figsize=(8, 6))

        for x in pollutionData:
            id = x.id
            if id not in self.data_points_pollution:
                self.data_points_pollution[id] = {'timestamps': [], 'coefficients': []}
            if x.timestamp in self.data_points_pollution[id]['timestamps']:
                index = self.data_points_pollution[id]['timestamps'].index(x.timestamp)
                self.data_points_pollution[id]['coefficients'][index] = x.coefficient
                continue  # Si el timestamp ya ha sido registrado para este ID, pasar al siguiente dato
            self.data_points_pollution[id]['timestamps'].append(x.timestamp)  # Almacenar el timestamp
            self.data_points_pollution[id]['coefficients'].append(x.coefficient)  # Almacenar el coeficiente
        for id, data in self.data_points_pollution.items():
            timestamps = [ts.seconds for ts in data['timestamps']]
            ax_pollution.plot(timestamps, data['coefficients'], marker='o', label=f'ID {id}')  # Graficar los puntos y asignar etiqueta a cada línea
        ax_pollution.set_title(f'Pollution, Terminal:{id_terminal}', loc="left", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax_pollution.legend()  # Mostrar leyenda con las etiquetas de las líneas

        for x in wellnessData:
            id = x.id
            if id not in self.data_points_wellness:
                self.data_points_wellness[id] = {'timestamps': [], 'coefficients': []}
            if x.timestamp in self.data_points_wellness[id]['timestamps']:
                index = self.data_points_wellness[id]['timestamps'].index(x.timestamp)
                self.data_points_wellness[id]['coefficients'][index] = x.coefficient
                continue  # Si el timestamp ya ha sido registrado para este ID, pasar al siguiente dato
            self.data_points_wellness[id]['timestamps'].append(x.timestamp)  # Almacenar el timestamp
            self.data_points_wellness[id]['coefficients'].append(x.coefficient)  # Almacenar el coeficiente
        for id, data in self.data_points_wellness.items():
            timestamps = [ts.seconds for ts in data['timestamps']]
            ax_wellness.plot(timestamps, data['coefficients'], marker='o', label=f'ID {id}')  # Graficar los puntos y asignar etiqueta a cada línea

        ax_wellness.set_title(f'Wellness, Terminal:{id_terminal}', loc="left", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax_wellness.legend()  # Mostrar leyenda con las etiquetas de las líneas

        plt.tight_layout()  # Ajustar el espacio
        plt.show()
        plt.close()

terminal_service = terminal_service()
