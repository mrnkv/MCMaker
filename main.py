#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import codecs
import sys
#import ooutils
import string
from ConfigParser import SafeConfigParser
from datetime import date
from PyQt4.QtGui import QApplication, QDialog, QMainWindow, QFileDialog
from PyQt4.QtGui import QTableWidgetItem, QAbstractItemView, QMessageBox
from PyQt4.QtCore import *
from Forms.ui_mainwindow import Ui_MainWindow
from Forms.ui_groups import Ui_GroupDialog
from Forms.ui_groups_mvc import Ui_GroupDialogMVC
from Forms.ui_komand import Ui_Komand
from Forms.ui_position import Ui_Position
from Forms.ui_dept import Ui_Dept
from Forms.ui_empls import Ui_Employee
from Forms.ui_sltask import Ui_SlTask
from Forms.ui_selectemployee import Ui_SelectEmployee
from entities import *

SLTASK_TEMPLATE = 'file:///home/mrnkv/MCMaker/Templates/SlTask.odt'

data = {}

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.model = KomandModel(self.komandTableView)
        self.sltaskmodel = SlTaskModel(self.servrecTableView)
        self.komandTableView.setModel(self.model)
        self.servrecTableView.setModel(self.sltaskmodel)
        self.connect(self.groups, SIGNAL("triggered()"), self.groupsDialogShow)
        self.connect(self.employees, SIGNAL("triggered()"), self.employeesDialogShow)
        self.connect(self.positions, SIGNAL("triggered()"), self.positionsDialogShow)
        self.connect(self.depts, SIGNAL("triggered()"), self.deptsDialogShow)
        self.komandTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.servrecTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.komandTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.servrecTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.komandTableView.selectRow(0)
        self.readConfig()

    def readConfig(self):
        parser = SafeConfigParser()
        # Open the file with the correct encoding
        with codecs.open(os.path.expanduser('~/.MCMaker.cfg'), 'rw', encoding='utf-8') as self.f:
            parser.readfp(self.f)
        self.dataFileName = parser.get('files','database_file')
        if self.dataFileName == '':
            self.dataFileName = QFileDialog.getOpenFileName(self, 
                    u"Выбрать файл базы данных")

            print self.dataFileName
            with codecs.open(os.path.expanduser('~/.MCMaker.cfg'), 'rw', encoding='utf-8') as self.f:
                parser.write(self.f)
        
    def addSlTask(self):
        index = self.komandTableView.currentIndex()
        print 'INDEX', index.row()
        if not index.isValid():
            print 'Index is not valid'
            QMessageBox.warning(self, u"Добаление записки", u"Сделайте выбор командировки")
            return
        selEmplDialog = SelectEmployeeDialog()
        if not selEmplDialog.exec_():
            return
        index = selEmplDialog.tableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        employee = selEmplDialog.model.data[row]
        komand = self.model.data[index.row()]
        dialog = SlTaskDialog()
        dialog.dateEdit.setDate(QDate.currentDate())
        dialog.lineEdit_9.setText(komand.komand_zadan)
        dialog.lineEdit_6.setText(komand.komand_addr)
        dialog.lineEdit_7.setText(komand.komand_org)
        dialog.dateEdit_2.setDate(komand.komand_start)
        dialog.dateEdit_3.setDate(komand.komand_end)
        dialog.lineEdit_8.setText(komand.komand_cos)
        dialog.lineEdit_2.setText(employee.family+' '+employee.name+' '+employee.sname)
        dialog.lineEdit_3.setText(str(employee.tab_num))
        position = session.query(Position).filter_by(pos_id = employee.position).one()
        dialog.lineEdit_5.setText(position.pos_name)
        dept = session.query(Dept).filter_by(dept_id = position.dept).one()
        group = session.query(Group).filter_by(group_id = position.group).one()
        dialog.lineEdit_4.setText(dept.dept_long_name+' '+group.group_long_name)
        if not dialog.exec_():
            print 'Not Add slTask'
            return
        servrecord = ServRecord(
                komand.komand_id, 
                int(unicode(dialog.lineEdit.text())), #record_num 
                date(dialog.dateEdit.date().year(),
                    dialog.dateEdit.date().month(),
                    dialog.dateEdit.date().day()), #record_date 
                unicode(dialog.lineEdit_2.text()), #record_fio 
                int (dialog.lineEdit_3.text()), #record_tabnum
                unicode(dialog.lineEdit_4.text()), #record_str_podr 
                unicode(dialog.lineEdit_5.text()), #record_dolg 
                unicode(dialog.lineEdit_6.text()), #record_addr 
                unicode(dialog.lineEdit_7.text()), #record_ org
                date(dialog.dateEdit_2.date().year(), 
                    dialog.dateEdit_2.date().month(), 
                    dialog.dateEdit_2.date().day()), #record_start
                date(dialog.dateEdit_3.date().year(), 
                    dialog.dateEdit_3.date().month(), 
                    dialog.dateEdit_3.date().day()), #record_end 
                unicode(dialog.lineEdit_9.text()), #record_zadan
                unicode(dialog.lineEdit_8.text()), #record_osn 
                unicode(dialog.lineEdit_10.text()),#record_ruk_str_otpr_dolg, 
                unicode(dialog.lineEdit_11.text()),#record_ruk_str_otpr_fio, 
                unicode(dialog.lineEdit_12.text()),#record_ruk_str_prin_dolg, 
                unicode(dialog.lineEdit_13.text()),#record_ruk_str_prin_fio, 
                unicode(dialog.lineEdit_14.text()),#record_ruk_org_dolg, 
                unicode(dialog.lineEdit_15.text())#record_ruk_org_fio
                )
        self.sltaskmodel.emit(SIGNAL("layoutAboutToBeChanged()"))
        session.add(servrecord)
        session.commit()
        self.sltaskmodel.data = session.query(SlTask).all()
        self.sltaskmodel.emit(SIGNAL("layoutChanged()"))
        self.servrecTableView.reset()


    def delSlTask(self):
        index = self.servrecTableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        self.sltaskmodel.emit(SIGNAL("layoutAboutToBeChanged()"))
        session.delete(self.sltaskmodel.data[row])
        session.commit()
        self.sltaskmodel.data = session.query(SlTask).all()
        self.sltaskmodel.emit(SIGNAL("layoutChanged()"))

    def printSlTask(self):
        index = self.servrecTableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        sltask = self.sltaskmodel.data[row]
        global data
        #data={}
        data['$record_num']= sltask.record_num
        data['$record_date']= sltask.record_date.strftime('%d.%m.%Y')+u'г.'
        data['$record_fio']= sltask.record_fio
        data['$record_tabnum']= sltask.record_tabnum
        data['$record_str_podr']= sltask.record_str_podr
        data['$record_dolg']= sltask.record_dolg
        data['$record_addr']= sltask.record_addr
        data['$record_org']= sltask.record_org
        data['$record_start']= sltask.record_start.strftime('%d.%m.%Y')+u'г.'
        data['$record_end']= sltask.record_end.strftime('%d.%m.%Y')+u'г.'
        data['$record_duration'] =(sltask.record_end - sltask.record_start).days + 1 
        data['$record_zadan']= sltask.record_zadan
        data['$record_osn']= sltask.record_osn
        data['$record_ruk_str_otpr_dolg']= sltask.record_ruk_str_otpr_dolg
        data['$record_ruk_str_otpr_fio']= sltask.record_ruk_str_otpr_fio
        data['$record_ruk_str_prin_dolg']= sltask.record_ruk_str_prin_dolg
        data['$record_ruk_str_prin_fio']= sltask.record_ruk_str_prin_fio
        data['$record_ruk_org_dolg']= sltask.record_ruk_org_dolg
        data['$record_ruk_org_fio']= sltask.record_ruk_org_fio
        oor = ooutils.OORunner()
        desktop = oor.connect()
        document = desktop.loadComponentFromURL(SLTASK_TEMPLATE ,"_blank", 0, ())
        cursor = document.Text.createTextCursor()
        search = document.createSearchDescriptor()
        def findandreplace(document=document,search=search,find=None,replace=None):
            """This function searches and replaces. Create search,
            call function findFirst, and finally replace what we found."""
            #What to search for
            search.SearchString = unicode(find)
            #search.SearchCaseSensitive = True
            search.SearchWords = True
            found = document.findFirst( search )
            if found:
                print 'Found %s' % find
                while found:
                    found.String = string.replace( found.String, 
                            unicode(find),unicode(replace))
                    found = document.findNext( found.End, search)
        #Do a loop of the data and replace the content.
        for find,replace in data.items():
            findandreplace(document,search,unicode(find),unicode(replace))
            print find,replace
        document.storeAsURL('file:///home/mrnkv/MCMaker/sltask.odt',())
        document.dispose()
        print 'Done'

    def addAccount(self):
        pass

    def delAccount(self):
        pass

    def printAccount(self):
        pass

    def addKommand(self):
        dialog = KomandDialog()
        if dialog.exec_():
            komand_zadan = unicode(dialog.lineEdit.text())
            komand_addr = unicode(dialog.lineEdit_3.text())
            komand_org = unicode(dialog.lineEdit_2.text())
            komand_start = date(dialog.startDateEdit.date().year(), dialog.startDateEdit.date().month(), dialog.startDateEdit.date().day())
            komand_end = date(dialog.endDateEdit.date().year(), dialog.endDateEdit.date().month(), dialog.endDateEdit.date().day())
            komand_cos = unicode(dialog.lineEdit_4.text())
            komand = Komand(komand_zadan, komand_addr, komand_org, komand_start,
                    komand_end, komand_cos)
            session.add(komand)
            session.commit()
            self.model.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.model.data = session.query(Komand).all()
            self.model.emit(SIGNAL("layoutChanged()"))
            self.tableView.reset()
            self.komandTableView.selectRow(0)


    def delKomand(self):
        print 'Delete komand...'
        index = self.tableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        self.model.emit(SIGNAL("layoutAboutToBeChanged()"))
        session.delete(self.model.data[row])
        session.commit()
        self.model.data = session.query(Komand).all()
        self.model.emit(SIGNAL("layoutChanged()"))

    def groupsDialogShow(self):
        dialog = GroupDialogMVC()
        dialog.exec_()

    def employeesDialogShow(self):
        dialog = EmployeeDialog()
        dialog.exec_()

    def positionsDialogShow(self):
        dialog = PositionDialog()
        dialog.exec_()

    def deptsDialogShow(self):
        dialog = DeptDialog()
        dialog.exec_()


class EmployeePositionsModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self.data = list(session.query(Position).filter(Position.employee == 0))
        for i in self.data:
            pass

    def Data(self, position, index):
        if index == 0:
            dept = session.query(Dept).filter_by(dept_id = position.dept).one()
            return dept.dept_short_name
        elif index == 1:
            group = session.query(Group).filter_by(group_id = position.group).one()
            return group.group_short_name
        elif index == 2:
            return position.pos_name
    def rowCount(self, parent):
        return len(self.data)
    def columnCount(self, parent):
        return 3 
    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return QVariant(self.Data(self.data[index.row()], index.column()))

class EmployeeModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self.data = session.query(Employee).all()
    def EmployeeData(self, employee, index):
        if index == 0:
            return employee.family
        if index == 1:
            return employee.name
        if index == 2:
            return employee.sname
    def rowCount(self, parent):
        return len(self.data)
    def columnCount(self, parent):
        return 3 
    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return QVariant(self.EmployeeData(self.data[index.row()], index.column()))

class SlTaskModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self.data = session.query(ServRecord).all()
    def SlTaskData(self, sltask, index):
        if index == 0:
            return sltask.record_num
        if index == 1:
            return sltask.record_date.isoformat()
        if index == 2:
            return sltask.record_fio
    def rowCount(self, parent):
        return len(self.data)
    def columnCount(self, parent):
        return 3
    def data(self,index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return QVariant(self.SlTaskData(self.data[index.row()], index.column()))

class SelectEmployeeDialog(QDialog, Ui_SelectEmployee):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.model = EmployeeModel(self.tableView)
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)

class EmployeeDialog(QDialog, Ui_Employee):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.emplsPosModel = EmployeePositionsModel(self.positionsTableView)
        self.positionsTableView.setModel(self.emplsPosModel)
        self.emplsModel = EmployeeModel(self.emplsTableView)
        self.emplsTableView.setModel(self.emplsModel)
        self.emplsTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.positionsTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.emplsTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.positionsTableView.setSelectionMode(QAbstractItemView.SingleSelection)

    def addEmployee(self):
        name = unicode(self.emplName.text())
        f_name = unicode(self.emplFirstName.text())
        s_name = unicode(self.emplSerName.text())
        tab_num = int(unicode(self.emplTabNum.text()))
        index = self.positionsTableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        self.emplsPosModel.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.emplsModel.emit(SIGNAL("layoutAboutToBeChanged()"))
        position = self.emplsPosModel.data[row]
        position_id = position.pos_id
        employee = Employee(name, f_name, s_name, position_id, tab_num)
        session.add(employee)
        session.commit()
        position.employee = int(employee.empl_id)
        session.commit()
        self.emplsPosModel.data = list(session.query(Position).filter(Position.employee == 0))
        self.emplsModel.data = session.query(Employee).all()
        self.emplsModel.emit(SIGNAL("layoutChanged()"))
        self.emplsPosModel.emit(SIGNAL("layoutChanged()"))
        self.emplsTableView.reset()
        self.positionsTableView.reset()
        self.emplFirstName.setText('')
        self.emplSerName.setText('')
        self.emplTabNum.setText('')

    def delEmployee(self):
        index = self.emplsTableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        self.emplsPosModel.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.emplsModel.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.emplsTableView.reset()
        session.delete(self.emplsModel.data[row])
        session.commit()
        self.emplsModel.data = session.query(Employee).all()
        self.emplsModel.emit(SIGNAL("layoutChanged()"))
        self.emplsPosModel.emit(SIGNAL("layoutChanged()"))
        pass


class DeptModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self.data = session.query(Dept).all()
    def deptData(self, dept, index):
        if index == 0:
            return dept.dept_id
        elif index == 1:
            return dept.dept_long_name
        elif index == 2:
            return dept.dept_short_name
    def rowCount(self, parent):
        return len(self.data)
    def columnCount(self, parent):
        return 3 
    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return QVariant(self.deptData(self.data[index.row()], index.column()))


class DeptDialog(QDialog, Ui_Dept):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.model = DeptModel(self.deptsTableView)
        self.deptsTableView.setModel(self.model)

    def addDept(self):
        l_name = unicode(self.deptLongName.text())
        s_name = unicode(self.deptShortName.text())
        print l_name, s_name
        if len(l_name) > 0 and len(s_name) > 0:
            dept = Dept(s_name, l_name)
            session.add(dept)
            session.commit()
            self.model.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.model.data = session.query(Dept).all()
            self.model.emit(SIGNAL("layoutChanged()"))
            self.deptsTableView.reset()
            self.deptLongName.setText('')
            self.deptShortName.setText('')
        else:
            print u"Задайте краткое и полное наименование службы"
        pass

    def delDept(self):
        print 'Deleting department ...'
        index = self.deptsTableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        self.model.emit(SIGNAL("layoutAboutToBeChanged()"))
        session.delete(self.model.data[row])
        self.model.data = session.query(Dept).all()
        self.model.emit(SIGNAL("layoutChanged()"))

    def cancelAddDept(self):
        self.deptLongName.setText('')
        self.deptShortName.setText('')

class PositionModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self.data = session.query(Position).all()
        print type(len(self.data)), len(self.data)

    def positionData(self, position, index):
        if index == 0:
            dept = session.query(Dept).filter_by(dept_id = position.dept).one()
            return dept.dept_short_name
        elif index == 1:
            group = session.query(Group).filter_by(group_id = position.group).one()
            return group.group_short_name
        elif index == 2:
            return position.pos_name
        elif index == 3:
            return position.pos_short_name

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        return 4 #

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return QVariant(self.positionData(self.data[index.row()], index.column()))

class PositionDialog(QDialog, Ui_Position):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.positionModel = PositionModel(self.positionsTableView)
        self.positionsTableView.setModel(self.positionModel)
        self.deptModel= DeptModel(self.deptsComboBox)
        self.deptsComboBox.setModel(self.deptModel)
        self.deptsComboBox.setModelColumn(1)
        self.groupModel = GroupModel(self.groupsComboBox)
        self.groupsComboBox.setModel(self.groupModel)
        self.groupsComboBox.setModelColumn(1)

    def addPosition(self):
        print 'Adding position ...'
        group_pos = self.groupModel.data[self.groupsComboBox.currentIndex()]
        dept_pos = self.deptModel.data[self.deptsComboBox.currentIndex()]
        l_name = unicode(self.posLongName.text())
        s_name = unicode(self.posShortName.text())
        if len(l_name) > 0 and len(s_name) > 0:
            position = Position(l_name, s_name, group_pos, dept_pos)
            session.add(position)
            session.commit()
            self.positionModel.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.positionModel.data = session.query(Position).all()
            self.positionModel.emit(SIGNAL("layoutChanged()"))
            self.positionsTableView.reset()
        else:
            print u"Задайте краткое и полное наименование должности"

    def delPosition(self):
        print 'Deleting position ...'
        index = self.positionsTableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        self.positionModel.emit(SIGNAL("layoutAboutToBeChanged()"))
        session.delete(self.positionModel.data[row])
        self.positionModel.data = session.query(Position).all()
        self.positionModel.emit(SIGNAL("layoutChanged()"))

    def cancelAddPosition(self):
        self.posLongName.setText('')
        self.posShortName.setText('')

class KomandModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self.data = session.query(Komand).all()
    def komandData(self, komand, index):
        if index == 0:
            return komand.komand_id
        elif index == 1:
            return komand.komand_start.isoformat()
        elif index == 2:
            return komand.komand_end.isoformat()
        elif index == 3:
            return komand.komand_org
        elif index == 4:
            return komand.komand_addr
        elif index == 5:
            return komand.komand_zadan
        elif index == 6:
            return komand.komand_cos
    def rowCount(self, parent):
        return len(self.data)
    def columnCount(self, parent):
        return 7 
    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return QVariant(self.komandData(self.data[index.row()], index.column()))

class KomandDialog(QDialog, Ui_Komand):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.startDateEdit.setDate(QDate.currentDate())
        self.endDateEdit.setDate(QDate.currentDate())

class SlTaskDialog(QDialog, Ui_SlTask):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.lineEdit_10.setText(u'Начальник лаборатории связи')
        self.lineEdit_12.setText(u'Начальник лаборатории связи')
        self.lineEdit_14.setText(u'Начльник Елецкого ЛПУМГ')
        self.lineEdit_11.setText(u'В.В.Меренков')
        self.lineEdit_13.setText(u'В.В.Меренков')
        self.lineEdit_15.setText(u'В.Н.Сидорцов')




class GroupDialogMVC(QDialog, Ui_GroupDialogMVC):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.model = GroupModel(self.groupsTableView)
        self.groupsTableView.setModel(self.model)

    def delGroup(self):
        print 'Deleting group...'
        index = self.groupsTableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        self.model.emit(SIGNAL("layoutAboutToBeChanged()"))
        session.delete(self.model.data[row])
        self.model.data = session.query(Group).all()
        self.model.emit(SIGNAL("layoutChanged()"))

    def addGroup(self):
        print 'Adding group ...'
        l_name = unicode(self.groupLongName.text())
        s_name = unicode(self.groupShortName.text())
        print l_name, s_name
        if len(l_name) > 0 and len(s_name) > 0:
            group = Group(group_long_name = l_name, group_short_name = s_name)
            session.add(group)
            session.commit()
            self.model.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.model.data = session.query(Group).all()
            self.model.emit(SIGNAL("layoutChanged()"))
            self.groupsTableView.reset()
            self.groupLongName.setText('')
            self.groupShortName.setText('')
        else:
            print u"Задайте краткое и полное наименоание группы"

    def addGroupCancel(self):
        self.groupLongName.setText('')
        self.groupShortName.setText('')

class GroupModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self.data = session.query(Group).all()
        print type(len(self.data)), len(self.data)
    def groupData(self, group, index):
        if index == 0:
            return group.group_id
        elif index == 1:
            return group.group_short_name
        elif index == 2:
            return group.group_long_name
    def rowCount(self, parent):
        return len(self.data)
    def columnCount(self, parent):
        return 3 #id, long_name, short_name
    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return QVariant(self.groupData(self.data[index.row()], index.column()))

app = QApplication(sys.argv)
session = createSession('')
window = MainWindow()

window.show()
sys.exit(app.exec_())

