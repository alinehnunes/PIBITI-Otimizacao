from PyQt5.QtWidgets import QLabel
from BaseDados import Basedados
from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries

class GraficoParametro(Basedados):

    def __init__(self, title, nomearquivo, nomeplanilha, parent=None):
        super().__init__(nomearquivo, nomeplanilha, parent)
        self.x = ["Selecione o parâmetro a ser comparado na tabela acima"]
        self.y = [0]

        info = QLabel("Selecione o Parâmetro para ser comparado na tabela acima")
        self.layout.addWidget(info)
        self.creategraph(self.x, self.y)

    def creategraph(self, x, y):
        series = QBarSeries()

        for i in range(len(x)):
            set = QBarSet(x[i])
            set.append([float(y[i])])
            series.append(set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Comparação das Propreidades')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisY = QValueAxis()
        axisY.setRange(0, float(max(y)))

        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        self.layout.addWidget(chartView)

    def atualizegraph(self, x, y, graf):
        graf.widget().deleteLater()
        self.creategraph(x,y)

    def eventFilter(self, source, event):
        if self.tablewidget.selectedIndexes() != []:

            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    selectedcolumn = self.tablewidget.currentColumn()
                    print(f'coluna selecionada é {selectedcolumn}')
                    row = self.tablewidget.rowCount()
                    column = self.tablewidget.columnCount()
                    if selectedcolumn == 0:
                        pass
                    else:
                        self.x = []
                        self.y = []
                        graf = self.layout.itemAt(2)
                        for i in range(row):
                            nomevar = self.tablewidget.item(i, 0).text()
                            self.x.append(nomevar)
                            valorvar = self.tablewidget.item(i, selectedcolumn).text()
                            self.y.append(valorvar)
                        self.atualizegraph(self.x, self.y, graf)
        return QtCore.QObject.event(source, event)
