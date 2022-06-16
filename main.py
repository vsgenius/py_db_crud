from crud import Crud

if __name__ == '__main__':
    db = Crud(database="netology_db", user="postgres", password="postgres")
    db.add_new_client('ivan','ivan','q@q.ru','142987174090')
    db.add_new_client('petr','ptr','p@p.ru')
    db.add_phone(4, '23454653767')
    db.add_phone(5, '742824688468')
    db.update_data_client(1, 'feodor', 'ivanov', '1@1.ru')
    db.del_phone(9)
    db.del_client(1)
    print(db.find_client(phone='142987174090'))
