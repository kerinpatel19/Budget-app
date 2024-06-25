import mysql.connector
from mysql.connector import errorcode

class GetCategory:
    @classmethod
    def get_category(cls,db_host, db_user, db_password, db_name,Control_category):
        return_list = []
        
        table_name = f"categories"
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        try:
            # Construct and execute the SQL query to select all distinct values from the Sub_Category column
            select_query = f"SELECT DISTINCT Category FROM {table_name} WHERE Control_Category = %s"
            cursor.execute(select_query, (Control_category,))

            # Fetch all the rows
            rows = cursor.fetchall()

            # Display the results
            for row in rows:
                return_list.append(row[0])  # Assuming Sub_Category is the first (0-indexed) column
            return return_list
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            if err.errno == errorcode.ER_NO_SUCH_TABLE:
                
                table_name2 = 'categories'
                category_columns = [
                    "ID int AUTO_INCREMENT PRIMARY KEY",
                    "Control_Category VARCHAR(255)",
                    "Category VARCHAR(255)"
                ]

                # Create the Categorys table
                create_table_query5 = f"CREATE TABLE IF NOT EXISTS {table_name2.lower()} ({', '.join(category_columns)})"
                cursor.execute(create_table_query5)
                db_connection.commit()
                result = []
                file_path = "/Users/kerinpatel/Desktop/dev/Projects-python/Budget-app/Data_base/Category.txt"
                with open(file_path, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line:
                            key, value = line.split('=')
                            format = (key.strip(), value.strip())
                            result.append(format)
                
                
                categories = result

                for main_category, sub_category in categories:
                    insert_data_query_cat = f"""
                    INSERT INTO {table_name2.lower()} (Control_Category, Category) 
                    VALUES (%s, %s)
                    """
                    cursor.execute(insert_data_query_cat, (main_category, sub_category))
                    db_connection.commit()
                return "Retry"
        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()

    @classmethod
    def view_all_category(cls, db_host, db_user, db_password, db_name):
        result = []
        try:
            connection = mysql.connector.connect(host=db_host,
                                                    user=db_user,
                                                    password=db_password,
                                                    database=db_name)
            cursor = connection.cursor()
            cursor.execute('SELECT Control_Category, Category FROM categories')
            rows = cursor.fetchall()
            for row in rows:
                result.append(row)
        except mysql.connector.Error as error:
            print("Failed to view categories: {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        return result
    
    @classmethod
    def add_category(cls, db_host, db_user, db_password, db_name, control, category):
        try:
            connection = mysql.connector.connect(host=db_host,
                                                    user=db_user,
                                                    password=db_password,
                                                    database=db_name)
            cursor = connection.cursor()
            sql = "INSERT INTO categories (Control_Category, Category) VALUES (%s, %s)"
            val = (control, category)
            cursor.execute(sql, val)
            connection.commit()
            return f"Category added - {control} - {category}"
        except mysql.connector.Error as error:
            print("Failed to add category: {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    @classmethod
    def delete_category(cls, db_host, db_user, db_password, db_name, control, category, reassign=None):
        message_2 = ""
        try:
            connection = mysql.connector.connect(host=db_host,
                                                    user=db_user,
                                                    password=db_password,
                                                    database=db_name)
            cursor = connection.cursor()
            sql = "DELETE FROM categories WHERE Control_Category = %s AND Category = %s"
            val = (control, category)
            cursor.execute(sql, val)
            connection.commit()
            message_1 = f"{category} - Deleted"
            if reassign:
                print(reassign)
                new_control = reassign[0]
                new_category = reassign[1]
                year =[2]
                cls.change_category(db_host, db_user, db_password, db_name, control, category, new_control, new_category, year)
                message_2 = f"Reassign to {new_category}"
        except mysql.connector.Error as error:
            print("Failed to delete category: {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        if reassign:
            return [message_1, message_2]
        else:
            return message_1
    
    @classmethod
    def change_category(cls, db_host, db_user, db_password, db_name, old_control, old_category, new_control, new_category, year, message=False):
        try:
            connection = mysql.connector.connect(host=db_host,
                                                user=db_user,
                                                password=db_password,
                                                database=db_name)
            cursor = connection.cursor()
            
            sql_update_category = "UPDATE categories SET Control_Category = %s, Category = %s WHERE Control_Category = %s AND Category = %s"
            val_update_category = (new_control, new_category, old_control, old_category)
            cursor.execute(sql_update_category, val_update_category)
            
            # Update transactions with the new category and control
            sql_update_transactions = f"UPDATE Posted_transactions_{year} SET Control_Category = %s, Category = %s WHERE Control_Category = %s AND Category = %s"
            val_update_transactions = (new_control, new_category, old_control, old_category)
            cursor.execute(sql_update_transactions, val_update_transactions)
            
            connection.commit()
            if message:
                return f"{old_control} and {old_category} changed to {new_control} and {new_category}"
        except mysql.connector.Error as error:
            print("Failed to change category: {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    @classmethod
    def edit_category(cls, db_host, db_user, db_password, db_name, old_control, old_category, new_control, new_category):
        try:
            connection = mysql.connector.connect(host=db_host,
                                                user=db_user,
                                                password=db_password,
                                                database=db_name)
            cursor = connection.cursor()
            
            sql_update_category = "UPDATE categories SET Control_Category = %s, Category = %s WHERE Control_Category = %s AND Category = %s"
            val_update_category = (new_control, new_category, old_control, old_category)
            cursor.execute(sql_update_category, val_update_category)
            connection.commit()
            return "Updated"
        except mysql.connector.Error as error:
            print("Failed to change category: {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    
    
