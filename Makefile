all: ui_empls.py \
	ui_groups.py \
	ui_mainwindow.py \
	ui_groups_mvc.py \
	ui_komand.py \
	ui_sltask.py \
	ui_position.py \
	ui_dept.py \
	ui_selectemployee.py

ui_empls.py: Forms/Empls.ui  
	pyuic4 Forms/Empls.ui -o ui_empls.py

ui_groups.py: Forms/Groups.ui
	pyuic4 Forms/Groups.ui -o ui_groups.py

ui_groups_mvc.py: Forms/GroupsMVC.ui
	pyuic4 Forms/GroupsMVC.ui -o ui_groups_mvc.py

ui_mainwindow.py: Forms/MainWindow.ui
	pyuic4 Forms/MainWindow.ui -o ui_mainwindow.py

ui_komand.py: Forms/Komand.ui  
	pyuic4 Forms/Komand.ui -o ui_komand.py

ui_position.py: Forms/Position.ui
	pyuic4 Forms/Position.ui -o ui_position.py

ui_dept.py: Forms/Dept.ui
	pyuic4 Forms/Dept.ui -o ui_dept.py

ui_sltask.py: Forms/SlTask.ui  
	pyuic4 Forms/SlTask.ui -o ui_sltask.py

ui_selectemployee.py: Forms/SelectEmployee.ui
	pyuic4 Forms/SelectEmployee.ui -o ui_selectemployee.py
