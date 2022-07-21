from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
import sys
import sqlite3


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class Ui(QMainWindow):
    def __init__(self, database):
        super(Ui, self).__init__()
        self.formvendas = uic.loadUi('formVendas.ui', self)
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.setFixedSize(307, 230)
        self.btnEnviar.clicked.connect(self.enviar)
        self.btnConsul.clicked.connect(self.consultar)
        self.btnLimp.clicked.connect(self.limpar)
        self.lista = uic.loadUi('formLista.ui')
        self.lista.btnExcluir.clicked.connect(self.excluir)
        self.table = self.lista.TableVendas
        self.formvendas.show()

    def enviar(self):
        prod = self.lineProd.text()
        prec = self.linePreco.text()
        vend = self.lineName.text()
        env = 'INSERT INTO Vendas (Produto, Preco, Vendedor) VALUES (?, ?, ?)'
        self.cursor.execute(env, (prod, prec, vend))
        self.conn.commit()
        self.statusBar.showMessage('Dados enviados!', 5000)
        self.lineProd.setText('')
        self.linePreco.setText('')
        self.lineName.setText('')


    def consultar(self):
        self.cursor.execute('SELECT * FROM Vendas')
        data = self.cursor.fetchall()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.lista.show()

    def limpar(self):
        self.lineProd.setText('')
        self.linePreco.setText('')
        self.lineName.setText('')

    def excluir(self):
        self.lista.close()
        iden = self.lista.lineExcl.text()
        line = f'DELETE FROM Vendas WHERE id = {iden}'
        self.cursor.execute(line)
        self.conn.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui('database.db')
    app.exec()
