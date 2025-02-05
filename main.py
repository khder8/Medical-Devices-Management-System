import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator

# Importing the UI and database connection classes
from ge_project import Ui_Form
from data_base_connection import data_base_connection

# Create a main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI from a separate UI file (created using Qt Designer)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Create a database connection object
        self.db = data_base_connection()
        

        # Connect UI elements to class variables
        self.Device_ID = self.ui.lineEdit
        self.Device_ID.setValidator(QIntValidator())  # Restrict input to integers

        self.Device_name = self.ui.lineEdit_2
        self.Device_Type = self.ui.lineEdit_3
        self.Classification = self.ui.lineEdit_4
        self.Department = self.ui.lineEdit_5
        self.Room_Number= self.ui.lineEdit_6
        self.Status = self.ui.lineEdit_7
        self.Serial_Number=self.ui.lineEdit_8
        self.M_date=self.ui.lineEdit_9
        

        self.add_btn = self.ui.add_btn
        self.update_btn = self.ui.update_btn
        self.select_btn = self.ui.select_btn
        self.search_btn = self.ui.search_btn
        self.clear_btn = self.ui.clear_btn
        self.delete_btn = self.ui.delete_btn
        self.Maint_hist_btn = self.ui.pushButton_2
        self.Maint_prov_btn = self.ui.pushButton_3
        self.Quantity_btn = self.ui.pushButton_4
        self.operator_btn = self.ui.pushButton_5
        self.next_M_date_btn=self.ui.pushButton
        
        self.Maint_hist_btn.setToolTip("INSERT DERVICE ID TO PROVIDE ITS MAINT HISTORY")
        self.Maint_prov_btn.setToolTip("INSERT DERVICE ID TO PROVIDE ITS MAINT Provider")
        self.operator_btn.setToolTip("INSERT DERVICE ID TO PROVIDE ITS Operator")
        self.Quantity_btn.setToolTip("INSERT DERVICE Type TO PROVIDE the Quantity")








        self.result_table = self.ui.tableWidget
        self.result_table.setSortingEnabled(False)
        self.buttons_list = self.ui.function_frame.findChildren(QPushButton)

        # Initialize signal-slot connections
        self.init_signal_slot()

        # Populate the initial data in the table 
        #self.search_info()
        
    def init_signal_slot(self):
        # Connect buttons to their respective functions
        self.add_btn.clicked.connect(self.add_info)
        self.search_btn.clicked.connect(self.search_info)
        self.clear_btn.clicked.connect(self.clear_form_info)
        self.select_btn.clicked.connect(self.select_info)
        self.update_btn.clicked.connect(self.update_info)
        self.delete_btn.clicked.connect(self.delete_info)
        self.Maint_hist_btn.clicked.connect(self.Maint_hist_info)
        self.Maint_prov_btn.clicked.connect(self.Maint_prov_info)
        self.Quantity_btn.clicked.connect(self.Quantity_info)
        self.operator_btn.clicked.connect(self.operator_info)
        self.next_M_date_btn.clicked.connect(self.next_M_date)
        


    
        
    def Quantity_info (self):
         # Function to add Device information
        self.disable_buttons()

        device_info = self.get_device_info()
       
        
        if device_info['Device_Type'] :
           
           dev_type=self.check_device_type(device_info["Device_Type"])
           if  dev_type :
               quantity= self.db.quantity(device_type=device_info["Device_Type"])
               
           else:
             QMessageBox.information(self, "Warning", " The Device type you entered is not found",
                                        QMessageBox.StandardButton.Ok)
             self.enable_buttons()
             return
        else :
             QMessageBox.information(self, "Warning", " please enter a Device type ",
                                        QMessageBox.StandardButton.Ok)
             self.enable_buttons()
             return

        if quantity:
           QMessageBox.information(self, "Info", f" the quantity of this device type is : {quantity}",
                                        QMessageBox.StandardButton.Ok)
           self.enable_buttons()
          
    def disable_buttons(self):
        # Disable all buttons
        for button in self.buttons_list:
            button.setDisabled(True)

    def enable_buttons(self):
        # Enable all buttons
        for button in self.buttons_list:
            button.setDisabled(False)

    def add_info(self):
        # Function to add Device information
        self.disable_buttons()

        device_info = self.get_device_info()
        #print(device_info)

        if device_info["Device_Id"] and device_info["Device_name"]:
            check_result = self.check_device_id(int(device_info["Device_Id"]))

            if check_result:
                QMessageBox.information(self, "Warning", "Please input a new Device ID",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttons()
                return
            
            
            add_result = self.db.add_info(device_id=int(device_info["Device_Id"]),
                                          device_name=device_info["Device_name"],
                                          device_type=device_info["Device_Type"],
                                          Classification=device_info["Classification"],
                                          department=device_info["Department"],
                                          Room_Number=device_info["Room_Number"],
                                          Status=device_info["Status"],
                                          Serial_Number=device_info["Serial_Number"])
            
            

            if add_result:
                QMessageBox.information(self, "Warning", f"Add fail: {add_result}, Please try again.",
                                        QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Warning", "Please input Device ID and Device name.",
                                    QMessageBox.StandardButton.Ok)

        self.search_info()
        self.enable_buttons()

    def update_info(self):
        # Function to update student information
        new_device_info = self.get_device_info()

        if new_device_info["Device_Id"]:
            update_result = self.db.update_info(
                device_id=new_device_info["Device_Id"],
                device_name=new_device_info["Device_name"],
                device_type=new_device_info["Device_Type"],
                classification=new_device_info["Classification"],
                department=new_device_info["Department"],
                Room_number=new_device_info["Room_Number"],
                Status=new_device_info["Status"],
                Serial_Number=new_device_info["Serial_Number"],
                M_date=new_device_info['M_date']
            )

            if update_result:
                QMessageBox.information(self, "Warning",
                                        f"Fail to update the information: {update_result}. Please try again.",
                                        QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.information(self, "Warning",
                                        f"the information has been updated",
                                        QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Warning",
                                    f"Please select one Device to update.",
                                    QMessageBox.StandardButton.Ok)
        self.enable_buttons()

    def select_info(self):
        # Function to select and populate Device information in the form
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.Device_ID.setEnabled(False)
            device_id = self.result_table.item(select_row, 0).text().strip()
            device_name = self.result_table.item(select_row, 1).text().strip()
            device_type= self.result_table.item(select_row, 2).text().strip()
            Classification = self.result_table.item(select_row, 3).text().strip()
            Department = self.result_table.item(select_row, 4).text().strip()
            Room_Number = self.result_table.item(select_row, 5).text().strip()
            Status = self.result_table.item(select_row, 6).text().strip()
            Serial_Numbe= self.result_table.item(select_row, 7).text().strip()
            


            self.Device_ID.setText(device_id)
            self.Device_name.setText( device_name)
            self.Device_Type.setText(device_type)
            self.Classification.setText(Classification)
            self.Department.setText(Department)
            self.Room_Number.setText(Room_Number)
            self.Status.setText(Status)
            self.Serial_Number.setText(Serial_Numbe)
        else:
            QMessageBox.information(self, "Warning", "Please select one Device information",
                                    QMessageBox.StandardButton.Ok)

    def search_info(self):
        # Function to search for Device information and populate the table
    
        Device_info = self.get_device_info()
        print(Device_info)
        

        search_result = self.db.search_info(
            device_id=Device_info["Device_Id"],
            device_name=Device_info["Device_name"],
            device_type=Device_info["Device_Type"],
            classification=Device_info["Classification"],
            department=Device_info["Department"],
            room_number=Device_info["Room_Number"],
            Status=Device_info["Status"],
            Serial_Number=Device_info["Serial_Number"]

        )
        

        if search_result :
            print(search_result)
            
            self.show_data(search_result)
        else:
            QMessageBox.information(self, "Search Result", "the device which your searching for is not found",
                                    QMessageBox.StandardButton.Ok)
             

    def clear_form_info(self):
        # Function to clear the form

        self.Device_ID .clear()
        self.Device_ID .setEnabled(True)
        self.Device_name.clear()
        self.Device_Type.clear()
        self.Classification.clear()
        self.Department.clear()
        self.Room_Number.clear()
        self.Status.clear()
        self.Serial_Number.clear()
        self.M_date.clear()

    def delete_info(self):
        # Function to delete device information
        select_row = self.result_table.currentRow()
        if select_row != -1:
            selected_option = QMessageBox.warning(self, "Warning", "Are you Sure to delete it?",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                Device_Id = self.result_table.item(select_row, 0).text().strip()

                delete_result = self.db.delete_info(Device_Id)
                

                if  not delete_result:
                    QMessageBox.information(self, "Warning",
                                            f"the device with the id{ Device_Id } has been deleted",
                                            QMessageBox.StandardButton.Ok)
                else:
                    QMessageBox.information(self, "Warning",
                                            f"Fail to delete the information: {delete_result}. Please try again.",
                                            QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Warning", "Please select one device information to delete",
                                    QMessageBox.StandardButton.Ok)

    def show_data(self, result):
        # Function to populate the table with Device information
        if result:
            
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))
            

            for row, info in enumerate(result):
                
                info_list = [
                    info[0],
                    info[1],
                    info[2],
                    info[3],
                    info[4],
                    info[5],
                    info[6],
                    info[7]
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)

        else:
            self.result_table.setRowCount(0)
            return

    def get_device_info(self):
        # Function to retrieve Device information from the form
        Device_Id = self.Device_ID.text().strip()
        Device_name = self.Device_name.text().strip()
        Device_Type= self.Device_Type.text().strip()
        Classification = self.Classification.text().strip()
        Department = self.Department.text().strip()
        Room_Number = self.Room_Number.text().strip()
        Status= self.Status.text().strip()
        Serial_Number= self.Serial_Number.text().strip()
        M_date=self.M_date.text().strip()



        Device_info = {
            "Device_Id": Device_Id,
            "Device_name": Device_name,
            "Device_Type": Device_Type,
            "Classification": Classification,
            "Department": Department,
            "Room_Number": Room_Number,
            "Status": Status,
            "Serial_Number": Serial_Number,
            'M_date':M_date
        }

        return Device_info

    def check_device_id(self, Devcice_Id):
         #Function to check if a Device ID already exists
        result = self.db.search_info(Devcice_Id)
        return result
    
    def check_device_type(self, device_type):
         #Function to check if a Device ID already exists
        result = self.db.search_info(device_type=device_type)
        
        return result

    
    def Maint_hist_info (self):
       self.disable_buttons()
       device_info = self.get_device_info()
       
       if device_info['Device_Id'] :
           dev_id=self.check_device_id(int(device_info["Device_Id"]))
           if  dev_id :
               Maint_hist= self.db.maint_info(device_id=int(device_info["Device_Id"]))
               
           else:
             QMessageBox.information(self, "Warning", " The Device id you entered is not found",
                                        QMessageBox.StandardButton.Ok)
             self.enable_buttons()
             return
       if Maint_hist :
           QMessageBox.information(self, "Info", f" the maintanice information is : {Maint_hist}",
                                        QMessageBox.StandardButton.Ok)
           self.enable_buttons()


    def operator_info (self):
       self.disable_buttons()
       device_info = self.get_device_info()
       
       if device_info['Device_Id'] :
           dev_id=self.check_device_id(int(device_info["Device_Id"]))
           if  dev_id :
               op_info= self.db.op_info(device_id=int(device_info["Device_Id"]))
               print(op_info)
               
           else:
             QMessageBox.information(self, "Warning", " The Device id you entered is not found",
                                        QMessageBox.StandardButton.Ok)
             self.enable_buttons()
             return
       if op_info :
           QMessageBox.information(self, "Info", f" the operator of the device is is : {op_info}",
                                        QMessageBox.StandardButton.Ok)
       self.enable_buttons()


    def Maint_prov_info (self):
       self.disable_buttons()
       device_info = self.get_device_info()
       
       if device_info['Device_Id'] :
           dev_id=self.check_device_id(int(device_info["Device_Id"]))
           if  dev_id :
               Maint_prov= self.db.maint_prov(device_id=int(device_info["Device_Id"]))
               
           else:
             QMessageBox.information(self, "Warning", " The Device id you entered is not found",
                                        QMessageBox.StandardButton.Ok)
             self.enable_buttons()
             return
       if Maint_prov :
           QMessageBox.information(self, "Info", f" the maintanice provider information is : {Maint_prov}",
                                        QMessageBox.StandardButton.Ok)
           self.enable_buttons()
        
    def  next_M_date (self):
       self.disable_buttons()
       device_info = self.get_device_info()
       
       if device_info['Device_Id'] :
           dev_id=self.check_device_id(int(device_info["Device_Id"]))
           if  dev_id :
               next_M_date= self.db.next_M_date(device_id=int(device_info["Device_Id"]))
               
               
           else:
             QMessageBox.information(self, "Warning", " The Device id you entered is not found",
                                        QMessageBox.StandardButton.Ok)
             self.enable_buttons()
             return
       if next_M_date :
           QMessageBox.information(self, "Info", f" the next M_date : {next_M_date}",
                                        QMessageBox.StandardButton.Ok)
       self.enable_buttons()

           

        
# Application entry point
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

   