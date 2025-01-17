import os

import src.database.bd_admin.local
#import scr.BD.bd_users.local.select_bd
#import scr.BD.bd_users.local.insert_bd
#import scr.BD.bd_users.local.create_bd
#import scr.BD.bd_users.local.update_bd
import src.utils.func
import src.utils.navigations


def check_user_credentials(login, password, page):
    conn = src.utils.func.get_user_db_connection(login, password)
    if conn is None:
        src.utils.func.show_snack_bar(page, "Неправильный логин или пароль. Проверьте введенные данные.")
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.login, e.password, p.privileges, e.first_name, e.last_name FROM public.employees e
        JOIN public.post p on p.id = e.post_id 
        WHERE login = %s AND password = %s
    """, (login, password))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    #scr.BD.bd_users.local.create_bd.local_user_db()
    if result:
        for record in result:
            id_user, login_user, password_user, privileges, first_name, last_name = record
            if privileges == 2:
                #scr.BD.bd_users.local.insert_bd.insert_bd_user(id_user, login_user, password_user, privileges,
                    #                                           first_name, last_name, page)
                pass
            else:
                src.database.bd_admin.local.insert_bd_user(id_user, login_user, password_user, privileges,
                                                     first_name, last_name, page)
    else:
        src.utils.func.show_snack_bar(page, "Нет пользователя в базе данных")  # Нормально написать
        pass
