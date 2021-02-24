# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'win_modal_setup.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(465, 573)
        Form.setMinimumSize(QtCore.QSize(465, 573))
        Form.setMaximumSize(QtCore.QSize(465, 573))
        Form.setBaseSize(QtCore.QSize(465, 573))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pics/gui_res/ico_ser.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabSetting = QtWidgets.QTabWidget(Form)
        self.tabSetting.setBaseSize(QtCore.QSize(0, 0))
        self.tabSetting.setObjectName("tabSetting")
        self.tab_setup_common = QtWidgets.QWidget()
        self.tab_setup_common.setObjectName("tab_setup_common")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_setup_common)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.tab_setup_common)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(45, 41))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/pics/gui_res/ico_albert.ico"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.tab_setup_common)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.groupBox = QtWidgets.QGroupBox(self.tab_setup_common)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btn_config_swipe = QtWidgets.QPushButton(self.groupBox)
        self.btn_config_swipe.setObjectName("btn_config_swipe")
        self.horizontalLayout_3.addWidget(self.btn_config_swipe)
        self.btn_config_load = QtWidgets.QPushButton(self.groupBox)
        self.btn_config_load.setObjectName("btn_config_load")
        self.horizontalLayout_3.addWidget(self.btn_config_load)
        self.btn_config_save = QtWidgets.QPushButton(self.groupBox)
        self.btn_config_save.setObjectName("btn_config_save")
        self.horizontalLayout_3.addWidget(self.btn_config_save)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_setup_common)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.label_import_dir_default = QtWidgets.QLabel(self.groupBox_2)
        self.label_import_dir_default.setMinimumSize(QtCore.QSize(0, 20))
        self.label_import_dir_default.setFrameShape(QtWidgets.QFrame.Box)
        self.label_import_dir_default.setObjectName("label_import_dir_default")
        self.verticalLayout_4.addWidget(self.label_import_dir_default)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.btn_set_dir_import_default = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_set_dir_import_default.setObjectName("btn_set_dir_import_default")
        self.horizontalLayout_4.addWidget(self.btn_set_dir_import_default)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.tabSetting.addTab(self.tab_setup_common, "")
        self.tab_setup_types = QtWidgets.QWidget()
        self.tab_setup_types.setObjectName("tab_setup_types")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.tab_setup_types)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.toolBox = QtWidgets.QToolBox(self.tab_setup_types)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 423, 307))
        self.page.setObjectName("page")
        self.horizontalLayout_45 = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout_45.setObjectName("horizontalLayout_45")
        self.groupBox_24 = QtWidgets.QGroupBox(self.page)
        self.groupBox_24.setObjectName("groupBox_24")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.groupBox_24)
        self.verticalLayout_24.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_24.setSpacing(3)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.horizontalLayout_43 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_43.setObjectName("horizontalLayout_43")
        self.label_25 = QtWidgets.QLabel(self.groupBox_24)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_43.addWidget(self.label_25)
        self.lineEdit_exportname_voice_in = QtWidgets.QLineEdit(self.groupBox_24)
        self.lineEdit_exportname_voice_in.setObjectName("lineEdit_exportname_voice_in")
        self.horizontalLayout_43.addWidget(self.lineEdit_exportname_voice_in)
        self.verticalLayout_24.addLayout(self.horizontalLayout_43)
        self.listView_voice_in = QtWidgets.QListView(self.groupBox_24)
        self.listView_voice_in.setObjectName("listView_voice_in")
        self.verticalLayout_24.addWidget(self.listView_voice_in)
        self.lineEdit_add_voice_in = QtWidgets.QLineEdit(self.groupBox_24)
        self.lineEdit_add_voice_in.setObjectName("lineEdit_add_voice_in")
        self.verticalLayout_24.addWidget(self.lineEdit_add_voice_in)
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_44.addItem(spacerItem4)
        self.btn_add_voice_in = QtWidgets.QPushButton(self.groupBox_24)
        self.btn_add_voice_in.setObjectName("btn_add_voice_in")
        self.horizontalLayout_44.addWidget(self.btn_add_voice_in)
        self.btn_remove_voice_in = QtWidgets.QPushButton(self.groupBox_24)
        self.btn_remove_voice_in.setObjectName("btn_remove_voice_in")
        self.horizontalLayout_44.addWidget(self.btn_remove_voice_in)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_44.addItem(spacerItem5)
        self.verticalLayout_24.addLayout(self.horizontalLayout_44)
        self.horizontalLayout_45.addWidget(self.groupBox_24)
        self.groupBox_23 = QtWidgets.QGroupBox(self.page)
        self.groupBox_23.setObjectName("groupBox_23")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.groupBox_23)
        self.verticalLayout_23.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_23.setSpacing(3)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.horizontalLayout_41 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_41.setObjectName("horizontalLayout_41")
        self.label_24 = QtWidgets.QLabel(self.groupBox_23)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_41.addWidget(self.label_24)
        self.lineEdit_exportname_voice_out = QtWidgets.QLineEdit(self.groupBox_23)
        self.lineEdit_exportname_voice_out.setObjectName("lineEdit_exportname_voice_out")
        self.horizontalLayout_41.addWidget(self.lineEdit_exportname_voice_out)
        self.verticalLayout_23.addLayout(self.horizontalLayout_41)
        self.listView_voice_out = QtWidgets.QListView(self.groupBox_23)
        self.listView_voice_out.setObjectName("listView_voice_out")
        self.verticalLayout_23.addWidget(self.listView_voice_out)
        self.lineEdit_add_voice_out = QtWidgets.QLineEdit(self.groupBox_23)
        self.lineEdit_add_voice_out.setObjectName("lineEdit_add_voice_out")
        self.verticalLayout_23.addWidget(self.lineEdit_add_voice_out)
        self.horizontalLayout_42 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_42.setObjectName("horizontalLayout_42")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_42.addItem(spacerItem6)
        self.btn_add_voice_out = QtWidgets.QPushButton(self.groupBox_23)
        self.btn_add_voice_out.setObjectName("btn_add_voice_out")
        self.horizontalLayout_42.addWidget(self.btn_add_voice_out)
        self.btn_remove_voice_out = QtWidgets.QPushButton(self.groupBox_23)
        self.btn_remove_voice_out.setObjectName("btn_remove_voice_out")
        self.horizontalLayout_42.addWidget(self.btn_remove_voice_out)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_42.addItem(spacerItem7)
        self.verticalLayout_23.addLayout(self.horizontalLayout_42)
        self.horizontalLayout_45.addWidget(self.groupBox_23)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 385, 271))
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_50 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_50.setObjectName("horizontalLayout_50")
        self.groupBox_26 = QtWidgets.QGroupBox(self.page_2)
        self.groupBox_26.setObjectName("groupBox_26")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.groupBox_26)
        self.verticalLayout_26.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_26.setSpacing(3)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.horizontalLayout_48 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_48.setObjectName("horizontalLayout_48")
        self.label_27 = QtWidgets.QLabel(self.groupBox_26)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_48.addWidget(self.label_27)
        self.lineEdit_exportname_message_in = QtWidgets.QLineEdit(self.groupBox_26)
        self.lineEdit_exportname_message_in.setObjectName("lineEdit_exportname_message_in")
        self.horizontalLayout_48.addWidget(self.lineEdit_exportname_message_in)
        self.verticalLayout_26.addLayout(self.horizontalLayout_48)
        self.listView_message_in = QtWidgets.QListView(self.groupBox_26)
        self.listView_message_in.setObjectName("listView_message_in")
        self.verticalLayout_26.addWidget(self.listView_message_in)
        self.lineEdit_add_message_in = QtWidgets.QLineEdit(self.groupBox_26)
        self.lineEdit_add_message_in.setObjectName("lineEdit_add_message_in")
        self.verticalLayout_26.addWidget(self.lineEdit_add_message_in)
        self.horizontalLayout_49 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_49.setObjectName("horizontalLayout_49")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_49.addItem(spacerItem8)
        self.btn_add_message_in = QtWidgets.QPushButton(self.groupBox_26)
        self.btn_add_message_in.setObjectName("btn_add_message_in")
        self.horizontalLayout_49.addWidget(self.btn_add_message_in)
        self.btn_remove_message_in = QtWidgets.QPushButton(self.groupBox_26)
        self.btn_remove_message_in.setObjectName("btn_remove_message_in")
        self.horizontalLayout_49.addWidget(self.btn_remove_message_in)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_49.addItem(spacerItem9)
        self.verticalLayout_26.addLayout(self.horizontalLayout_49)
        self.horizontalLayout_50.addWidget(self.groupBox_26)
        self.groupBox_25 = QtWidgets.QGroupBox(self.page_2)
        self.groupBox_25.setObjectName("groupBox_25")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.groupBox_25)
        self.verticalLayout_25.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_25.setSpacing(3)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.horizontalLayout_46 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_46.setObjectName("horizontalLayout_46")
        self.label_26 = QtWidgets.QLabel(self.groupBox_25)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_46.addWidget(self.label_26)
        self.lineEdit_exportname_message_out = QtWidgets.QLineEdit(self.groupBox_25)
        self.lineEdit_exportname_message_out.setObjectName("lineEdit_exportname_message_out")
        self.horizontalLayout_46.addWidget(self.lineEdit_exportname_message_out)
        self.verticalLayout_25.addLayout(self.horizontalLayout_46)
        self.listView_message_out = QtWidgets.QListView(self.groupBox_25)
        self.listView_message_out.setObjectName("listView_message_out")
        self.verticalLayout_25.addWidget(self.listView_message_out)
        self.lineEdit_add_message_out = QtWidgets.QLineEdit(self.groupBox_25)
        self.lineEdit_add_message_out.setObjectName("lineEdit_add_message_out")
        self.verticalLayout_25.addWidget(self.lineEdit_add_message_out)
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_47.addItem(spacerItem10)
        self.btn_add_message_out = QtWidgets.QPushButton(self.groupBox_25)
        self.btn_add_message_out.setObjectName("btn_add_message_out")
        self.horizontalLayout_47.addWidget(self.btn_add_message_out)
        self.btn_remove_message_out = QtWidgets.QPushButton(self.groupBox_25)
        self.btn_remove_message_out.setObjectName("btn_remove_message_out")
        self.horizontalLayout_47.addWidget(self.btn_remove_message_out)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_47.addItem(spacerItem11)
        self.verticalLayout_25.addLayout(self.horizontalLayout_47)
        self.horizontalLayout_50.addWidget(self.groupBox_25)
        self.toolBox.addItem(self.page_2, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 407, 293))
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_55 = QtWidgets.QHBoxLayout(self.page_3)
        self.horizontalLayout_55.setObjectName("horizontalLayout_55")
        self.groupBox_27 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_27.setObjectName("groupBox_27")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout(self.groupBox_27)
        self.verticalLayout_27.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_27.setSpacing(3)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.horizontalLayout_51 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_51.setObjectName("horizontalLayout_51")
        self.label_28 = QtWidgets.QLabel(self.groupBox_27)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_51.addWidget(self.label_28)
        self.lineEdit_exportname_network = QtWidgets.QLineEdit(self.groupBox_27)
        self.lineEdit_exportname_network.setObjectName("lineEdit_exportname_network")
        self.horizontalLayout_51.addWidget(self.lineEdit_exportname_network)
        self.verticalLayout_27.addLayout(self.horizontalLayout_51)
        self.listView_network = QtWidgets.QListView(self.groupBox_27)
        self.listView_network.setObjectName("listView_network")
        self.verticalLayout_27.addWidget(self.listView_network)
        self.lineEdit_add_network = QtWidgets.QLineEdit(self.groupBox_27)
        self.lineEdit_add_network.setObjectName("lineEdit_add_network")
        self.verticalLayout_27.addWidget(self.lineEdit_add_network)
        self.horizontalLayout_52 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_52.setObjectName("horizontalLayout_52")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_52.addItem(spacerItem12)
        self.btn_add_network = QtWidgets.QPushButton(self.groupBox_27)
        self.btn_add_network.setObjectName("btn_add_network")
        self.horizontalLayout_52.addWidget(self.btn_add_network)
        self.btn_remove_network = QtWidgets.QPushButton(self.groupBox_27)
        self.btn_remove_network.setObjectName("btn_remove_network")
        self.horizontalLayout_52.addWidget(self.btn_remove_network)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_52.addItem(spacerItem13)
        self.verticalLayout_27.addLayout(self.horizontalLayout_52)
        self.horizontalLayout_55.addWidget(self.groupBox_27)
        self.groupBox_28 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_28.setObjectName("groupBox_28")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.groupBox_28)
        self.verticalLayout_28.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_28.setSpacing(3)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.horizontalLayout_53 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_53.setObjectName("horizontalLayout_53")
        self.label_29 = QtWidgets.QLabel(self.groupBox_28)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_53.addWidget(self.label_29)
        self.lineEdit_exportname_forwarding = QtWidgets.QLineEdit(self.groupBox_28)
        self.lineEdit_exportname_forwarding.setObjectName("lineEdit_exportname_forwarding")
        self.horizontalLayout_53.addWidget(self.lineEdit_exportname_forwarding)
        self.verticalLayout_28.addLayout(self.horizontalLayout_53)
        self.listView_forwarding = QtWidgets.QListView(self.groupBox_28)
        self.listView_forwarding.setObjectName("listView_forwarding")
        self.verticalLayout_28.addWidget(self.listView_forwarding)
        self.lineEdit_add_forwarding = QtWidgets.QLineEdit(self.groupBox_28)
        self.lineEdit_add_forwarding.setObjectName("lineEdit_add_forwarding")
        self.verticalLayout_28.addWidget(self.lineEdit_add_forwarding)
        self.horizontalLayout_54 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_54.setObjectName("horizontalLayout_54")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_54.addItem(spacerItem14)
        self.btn_add_forwarding = QtWidgets.QPushButton(self.groupBox_28)
        self.btn_add_forwarding.setObjectName("btn_add_forwarding")
        self.horizontalLayout_54.addWidget(self.btn_add_forwarding)
        self.btn_remove_forwarding = QtWidgets.QPushButton(self.groupBox_28)
        self.btn_remove_forwarding.setObjectName("btn_remove_forwarding")
        self.horizontalLayout_54.addWidget(self.btn_remove_forwarding)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_54.addItem(spacerItem15)
        self.verticalLayout_28.addLayout(self.horizontalLayout_54)
        self.horizontalLayout_55.addWidget(self.groupBox_28)
        self.toolBox.addItem(self.page_3, "")
        self.verticalLayout_22.addWidget(self.toolBox)
        self.horizontalLayout_40 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_40.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_40.setSpacing(3)
        self.horizontalLayout_40.setObjectName("horizontalLayout_40")
        self.label_23 = QtWidgets.QLabel(self.tab_setup_types)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_40.addWidget(self.label_23)
        self.lineEdit_exportname_unknowntypes = QtWidgets.QLineEdit(self.tab_setup_types)
        self.lineEdit_exportname_unknowntypes.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_exportname_unknowntypes.setObjectName("lineEdit_exportname_unknowntypes")
        self.horizontalLayout_40.addWidget(self.lineEdit_exportname_unknowntypes)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_40.addItem(spacerItem16)
        self.verticalLayout_22.addLayout(self.horizontalLayout_40)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_22.addItem(spacerItem17)
        self.tabSetting.addTab(self.tab_setup_types, "")
        self.tab_setup_columns = QtWidgets.QWidget()
        self.tab_setup_columns.setObjectName("tab_setup_columns")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_setup_columns)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.toolBox_2 = QtWidgets.QToolBox(self.tab_setup_columns)
        self.toolBox_2.setObjectName("toolBox_2")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 385, 293))
        self.page_4.setObjectName("page_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.page_4)
        self.label_5.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.comboBox_choose_import_column = QtWidgets.QComboBox(self.page_4)
        self.comboBox_choose_import_column.setObjectName("comboBox_choose_import_column")
        self.horizontalLayout_5.addWidget(self.comboBox_choose_import_column)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.listView_keywords_col_replace = QtWidgets.QListView(self.page_4)
        self.listView_keywords_col_replace.setObjectName("listView_keywords_col_replace")
        self.verticalLayout_6.addWidget(self.listView_keywords_col_replace)
        self.label_6 = QtWidgets.QLabel(self.page_4)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.lineEdit_add_keyword_column = QtWidgets.QLineEdit(self.page_4)
        self.lineEdit_add_keyword_column.setObjectName("lineEdit_add_keyword_column")
        self.verticalLayout_6.addWidget(self.lineEdit_add_keyword_column)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem18)
        self.btn_add_keyword_column = QtWidgets.QPushButton(self.page_4)
        self.btn_add_keyword_column.setObjectName("btn_add_keyword_column")
        self.horizontalLayout_6.addWidget(self.btn_add_keyword_column)
        self.btn_remove_keyword_column = QtWidgets.QPushButton(self.page_4)
        self.btn_remove_keyword_column.setObjectName("btn_remove_keyword_column")
        self.horizontalLayout_6.addWidget(self.btn_remove_keyword_column)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem19)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.toolBox_2.addItem(self.page_4, "")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0, 0, 423, 426))
        self.page_5.setObjectName("page_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.table_columns_exportnames = QtWidgets.QTableWidget(self.page_5)
        self.table_columns_exportnames.setObjectName("table_columns_exportnames")
        self.table_columns_exportnames.setColumnCount(2)
        self.table_columns_exportnames.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_columns_exportnames.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_columns_exportnames.setHorizontalHeaderItem(1, item)
        self.table_columns_exportnames.horizontalHeader().setDefaultSectionSize(100)
        self.table_columns_exportnames.horizontalHeader().setMinimumSectionSize(25)
        self.table_columns_exportnames.horizontalHeader().setSortIndicatorShown(False)
        self.table_columns_exportnames.horizontalHeader().setStretchLastSection(True)
        self.table_columns_exportnames.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_7.addWidget(self.table_columns_exportnames)
        self.toolBox_2.addItem(self.page_5, "")
        self.verticalLayout_5.addWidget(self.toolBox_2)
        self.tabSetting.addTab(self.tab_setup_columns, "")
        self.verticalLayout.addWidget(self.tabSetting)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem20)
        self.btn_setup_ok = QtWidgets.QPushButton(Form)
        self.btn_setup_ok.setObjectName("btn_setup_ok")
        self.horizontalLayout.addWidget(self.btn_setup_ok)
        self.btn_setup_cancel = QtWidgets.QPushButton(Form)
        self.btn_setup_cancel.setObjectName("btn_setup_cancel")
        self.horizontalLayout.addWidget(self.btn_setup_cancel)
        self.btn_setup_accept = QtWidgets.QPushButton(Form)
        self.btn_setup_accept.setEnabled(False)
        self.btn_setup_accept.setObjectName("btn_setup_accept")
        self.horizontalLayout.addWidget(self.btn_setup_accept)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        self.tabSetting.setCurrentIndex(2)
        self.toolBox.setCurrentIndex(0)
        self.toolBox_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Налаштування"))
        self.label_2.setText(_translate("Form", "Математик 1.1 - build220221(develop)"))
        self.groupBox.setTitle(_translate("Form", "Відновлення конфігурації програми"))
        self.label_3.setText(_translate("Form", "Скидання конфігурації призводить до відновлення налаштувань розпізнання типів файлів, їх підписів, розпізнання підписів колонок - до типових правил передбачених розробником. При цьому втрачаються зміни внесені користувачем. Наявна можливість зберегти поточні налаштування в окремий файл для їх подальшого відновлення. "))
        self.btn_config_swipe.setText(_translate("Form", "Скинути до початкових"))
        self.btn_config_load.setText(_translate("Form", "Завантажити з файлу"))
        self.btn_config_save.setText(_translate("Form", "Зберегти поточні"))
        self.groupBox_2.setTitle(_translate("Form", "Типова папка імпорту"))
        self.label_4.setText(_translate("Form", "Типова папка використовується для швидкого додавання файлів таблиць для імпорту (не включає вкладені папки)"))
        self.label_import_dir_default.setText(_translate("Form", "C:\\"))
        self.btn_set_dir_import_default.setText(_translate("Form", "Обрати"))
        self.tabSetting.setTabText(self.tabSetting.indexOf(self.tab_setup_common), _translate("Form", "Загальні"))
        self.groupBox_24.setTitle(_translate("Form", "Вхідні голосові з\'єднання"))
        self.label_25.setText(_translate("Form", "Конвертувати в:"))
        self.lineEdit_exportname_voice_in.setText(_translate("Form", "вх"))
        self.btn_add_voice_in.setText(_translate("Form", "Додати"))
        self.btn_remove_voice_in.setText(_translate("Form", "Видалити"))
        self.groupBox_23.setTitle(_translate("Form", "Вихідні голосові з\'єднання"))
        self.label_24.setText(_translate("Form", "Конвертувати в:"))
        self.lineEdit_exportname_voice_out.setText(_translate("Form", "вих"))
        self.btn_add_voice_out.setText(_translate("Form", "Додати"))
        self.btn_remove_voice_out.setText(_translate("Form", "Видалити"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("Form", "Голосові з\'єднання"))
        self.groupBox_26.setTitle(_translate("Form", "Вхідні SMS-повідомлення"))
        self.label_27.setText(_translate("Form", "Конвертувати в:"))
        self.lineEdit_exportname_message_in.setText(_translate("Form", "вх СМС"))
        self.btn_add_message_in.setText(_translate("Form", "Додати"))
        self.btn_remove_message_in.setText(_translate("Form", "Видалити"))
        self.groupBox_25.setTitle(_translate("Form", "Вихідні SMS-повідомлення"))
        self.label_26.setText(_translate("Form", "Конвертувати в:"))
        self.lineEdit_exportname_message_out.setText(_translate("Form", "вих СМС"))
        self.btn_add_message_out.setText(_translate("Form", "Додати"))
        self.btn_remove_message_out.setText(_translate("Form", "Видалити"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("Form", "SMS-повідомлення"))
        self.groupBox_27.setTitle(_translate("Form", "Використання мережі"))
        self.label_28.setText(_translate("Form", "Конвертувати в:"))
        self.lineEdit_exportname_network.setText(_translate("Form", "інтернет"))
        self.btn_add_network.setText(_translate("Form", "Додати"))
        self.btn_remove_network.setText(_translate("Form", "Видалити"))
        self.groupBox_28.setTitle(_translate("Form", "Переадресація"))
        self.label_29.setText(_translate("Form", "Конвертувати в:"))
        self.lineEdit_exportname_forwarding.setText(_translate("Form", "переад"))
        self.btn_add_forwarding.setText(_translate("Form", "Додати"))
        self.btn_remove_forwarding.setText(_translate("Form", "Видалити"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("Form", "Переадресація та інтернет"))
        self.label_23.setText(_translate("Form", "Нерозпізнані типи замінити на:"))
        self.lineEdit_exportname_unknowntypes.setText(_translate("Form", "переад"))
        self.tabSetting.setTabText(self.tabSetting.indexOf(self.tab_setup_types), _translate("Form", "Типи"))
        self.label_5.setText(_translate("Form", "Тип колонки:"))
        self.label_6.setText(_translate("Form", "Додати підпис для розпізнавання: "))
        self.btn_add_keyword_column.setText(_translate("Form", "Додати"))
        self.btn_remove_keyword_column.setText(_translate("Form", "Видалити"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_4), _translate("Form", "Розпізнання колонок у імпортованих файлах"))
        item = self.table_columns_exportnames.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Тип колонки"))
        item = self.table_columns_exportnames.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Підпис у вихідному файлі"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_5), _translate("Form", "Підписи колонок у експортованих файлах"))
        self.tabSetting.setTabText(self.tabSetting.indexOf(self.tab_setup_columns), _translate("Form", "Колонки"))
        self.btn_setup_ok.setText(_translate("Form", "OK"))
        self.btn_setup_cancel.setText(_translate("Form", "Скасувати"))
        self.btn_setup_accept.setText(_translate("Form", "Підтвердити"))
import gui.res_file_rc