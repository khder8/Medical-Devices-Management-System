import pyodbc as odbc

class data_base_connection:
    def __init__(self):
        self.DRIVER = "ODBC Driver 17 for SQL Server"
        self.SERVER="LAPTOP-E6L17HVP"
        self.DATABASE="Med_Devices"
        self.Trusted_connection="yes" 
        

    def connect_db(self):
        # Establish a database connection
        self.con =odbc.connect(f'DRIVER={self.DRIVER};SERVER={self.SERVER};DATABASE={self.DATABASE};Trusted_Connection={self.Trusted_connection};') 

        # Create a cursor for executing SQL queries
        self.cursor = self.con.cursor()


    def add_info(self, device_id , device_name, device_type, Classification, department, Room_Number,Status, Serial_Number):
        #print(Classification)
        # Connect to the database
        
        self.connect_db()
        

        # Construct SQL query for adding information
        sql = f"""
            INSERT INTO Devices (id, D_name, D_type, D_classification, dep_id, room_number,D_status,Serial_number) 
	            VALUES ({device_id}, '{device_name}', '{device_type}', '{Classification}', '{department}', '{Room_Number}', '{Status}','{Serial_Number}');
        """

        try:
            # Execute the SQL query for adding information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()

    def update_info(self, device_id , device_name, device_type, classification, department, Room_number,Status, Serial_Number,M_date):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for updating information
        sql = f"""
            UPDATE Devices
                SET id='{device_id}', D_name='{device_name}', D_type='{device_type}', D_classification='{classification}' 
                    , room_number='{Room_number}',D_status='{Status}',Serial_number='{Serial_Number}',next_maintenance_date='{M_date}',
                    dep_id= (select dep_id from departments where dep_name='{department}')

                where id ='{device_id}';

            


                
        """

        try:
            # Execute the SQL query for updating information
            self.cursor.execute(sql)
            self.con.commit()


        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()

    def delete_info(self, device_id):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for deleting information
        sql = f"""  
            DELETE FROM Devices WHERE id={device_id};
        """

        try:
            # Execute the SQL query for deleting information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()                   

    def search_info(self, device_id=None, device_name=None, device_type=None, classification=None, department=None, room_number=None,Status=None,Serial_Number=None):
        # Connect to the database
        self.connect_db()

        condition = ""
        if device_id:
            condition += f" id LIKE '%{device_id}%'"
        else:
            if device_name:
                if condition:
                    condition += f" and D_name LIKE '%{device_name}%'"
                else:
                    condition += f" D_name LIKE '%{device_name}%'"

            if device_type:
                if condition:
                    condition += f" and D_type LIKE '%{device_type}%'"
                else:
                    condition += f" D_type LIKE '%{device_type}%'"

            if classification:
                if condition:
                    condition += f" and D_classification LIKE'%{classification}%'"
                else:
                    condition += f"D_classification LIKE'%{classification}%'"

            if department:
                if condition:
                    condition += f" and  dep_name LIKE '%{department}%' "
                else:
                    condition += f"dep_name LIKE'%{department}%'"

            if room_number:
                if condition:
                    condition += f" and room_number LIKE '%{room_number}%'"
                else:
                    condition += f"room_number LIKE '%{room_number}%'"
            if  Serial_Number:
                if condition:
                    condition += f" and Serial_number LIKE '%{Serial_Number}%'"
                else:
                    condition += f"Serial_number LIKE '%{Serial_Number}%'" 
            if  Status:
                if condition:
                    condition += f" and D_status LIKE '%{Status}%'"
                else:
                    condition += f"D_Status LIKE '%{Status}%'"       

        if condition:
            # Construct SQL query for searching information with conditions
           
            sql = f"""
                SELECT id , D_name , D_type ,D_classification, dep_name , room_number , D_status,Serial_number  
                from Devices 
                inner join departments
                on (Devices.dep_id=departments.dep_id) and {condition}
            """
            
        else:
            # Construct SQL query for searching all information
            sql = f"""
                SELECT id , D_name , D_type , D_classification,dep_name, room_number ,D_status,Serial_number  FROM  Devices
                inner join departments
                on (Devices.dep_id=departments.dep_id);
             """

        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result1 = self.cursor.fetchall()
            print(result1)
            
            
            return result1
        
        
        

        except Exception as E:
            return E

        finally:
            # Close the database connection
            self.con.close()    
    
    def maint_info(self,device_id):
        
        self.connect_db()
        sql = f"""

        select   'Maintenance_id:' + CONVERT (varchar,Maintenance_id)
                  +'device_id:' +Convert(varchar,device_id)

                  + 'Maintenance_date:' + Convert(varchar,Maintenance_date) 
                  +  'M_description'+ Convert(varchar,M_description)
                  from  
                  Maintenance_Records 
                 where device_id= {device_id}  
                  
                  """ 
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result1 = self.cursor.fetchall()
            print(result1)
            
            
            return result1
        

        except Exception as E:
            return E

        finally:
            # Close the database connection
            self.con.close()    
        

    def maint_prov(self,device_id):
        
        self.connect_db()
        sql = f"""

        select  
         'provider_id:' + CONVERT (varchar,provider_id)
          +'provider_name:' +Convert(varchar,provider_name)
           + 'contact information:' + Convert(varchar,contact_infromation)
            + 'service_type:'+ Convert(varchar,service_type)
                  from Service_provider  
                  where device_id={device_id}
                  """ 
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result1 = self.cursor.fetchall()
            print(result1)
            
            
            return result1
        

        except Exception as E:
            return E

        finally:
            # Close the database connection
            self.con.close()    
                

    def quantity(self,device_type):
        
        self.connect_db()
        sql = f"""

        select  D_type , count(id)
        from Devices 
        where D_type='{device_type}'
        group by 
        D_type
        
         
                  """ 
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result1 = self.cursor.fetchall()
            return result1
        

        except Exception as E:
            return E

        finally:
            # Close the database connection
            self.con.close()    
    def op_info(self, device_id):
        # Connect to the database
        self.connect_db()
        #print(device_id)

        # Construct SQL query for deleting information
        sql = f"""  
            select  'emp_id is:'+convert( varchar,emp_id) + ' , emp_name is: '+ f_name +' ' l_name 
            from Employees
            
            inner join Devices
            on Devices.per_charge = Employees.emp_id and Devices.id='{device_id}';
        """

        try:
            # Execute the SQL query for deleting information
            self.cursor.execute(sql)
            result1 = self.cursor.fetchall()
            return result1

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close() 

    def next_M_date(self,device_id):
        
        self.connect_db()
        sql = f"""

        select next_maintenance_date
        from Devices 
        where id='{device_id}'
        
         
                  """ 
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result1 = self.cursor.fetchall()
            return result1
        

        except Exception as E:
            return E

        finally:
            # Close the database connection
            self.con.close()  
