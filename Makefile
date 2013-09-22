all: Forms/ui_empls.py \
	Forms/ui_groups.py \
	Forms/ui_mainwindow.py \
	Forms/ui_groups_mvc.py \
	Forms/ui_komand.py \
	Forms/ui_sltask.py \
	Forms/ui_position.py \
	Forms/ui_dept.py \
	Forms/ui_selectemployee.py

Forms/ui_empls.py: Forms/Empls.ui  
	pyuic4 Forms/Empls.ui -o Forms/ui_empls.py

Forms/ui_groups.py: Forms/Groups.ui
	pyuic4 Forms/Groups.ui -o Forms/ui_groups.py

Forms/ui_groups_mvc.py: Forms/GroupsMVC.ui
	pyuic4 Forms/GroupsMVC.ui -o Forms/ui_groups_mvc.py

Forms/ui_mainwindow.py: Forms/MainWindow.ui
	pyuic4 Forms/MainWindow.ui -o Forms/ui_mainwindow.py

Forms/ui_komand.py: Forms/Komand.ui  
	pyuic4 Forms/Komand.ui -o Forms/ui_komand.py

Forms/ui_position.py: Forms/Position.ui
	pyuic4 Forms/Position.ui -o Forms/ui_position.py

Forms/ui_dept.py: Forms/Dept.ui
	pyuic4 Forms/Dept.ui -o Forms/ui_dept.py

Forms/ui_sltask.py: Forms/SlTask.ui  
	pyuic4 Forms/SlTask.ui -o Forms/ui_sltask.py

Forms/ui_selectemployee.py: Forms/SelectEmployee.ui
	pyuic4 Forms/SelectEmployee.ui -o Forms/ui_selectemployee.py
