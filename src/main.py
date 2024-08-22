import random
import string
from datetime import datetime, timedelta

import psycopg2
from psycopg2 import connection, cursor


def generate_random_string(length: int = 20) -> str:
    """Создается строка длиной `length` из случайных символов и цифр."""
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(length)
    )


def generate_random_int(begin: int = 0, end: int = 10000) -> int:
    """Создает целое число в диапазоне от `begin` до `end`."""
    return random.randint(begin, end + 1)


def get_db_connect_currsor(
    dbname: str,
    user: str,
    password: str,
    host: str = 'localhost',
    port: int = 5432,
) -> tuple[connection, cursor]:
    """Создает соединение с БД и курсор для работы."""
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
    )

    # Создание курсора
    cur = conn.cursor()

    return conn, cur


def main() -> None:
    """Создает данные и добавляет их в БД."""
    # Список городов для выбора
    cities = [
        'Москва',
        'Санкт-Петербург',
        'Новосибирск',
        'Екатеринбург',
        'Нижний Новгород',
        'Казань',
        'Челябинск',
        'Омск',
        'Самара',
        'Ростов-на-Дону',
        'Уфа',
        'Красноярск',
        'Волгоград',
        'Пермь',
        'Воронеж',
        'Краснодар',
        'Саратов',
        'Тольятти',
        'Ижевск',
        'Барнаул',
        'Ульяновск',
        'Иркутск',
        'Владивосток',
        'Ярославль',
        'Хабаровск',
        'Махачкала',
        'Оренбург',
        'Новокузнецк',
        'Тюмень',
        'Астрахань',
        'Брянск',
        'Пенза',
    ]
    db_cities = [{'id': i + 1, 'name': cities[i]} for i in range(len(cities))]
    db_users = [
        {
            'id': i + 1,
            'tg_id': generate_random_int(100000, 999999),
            'fio': generate_random_string(20),
            'phone': generate_random_int(1000000000, 9999999999),
            'email': f'{generate_random_string(5)}@example.ru',
            'iin': generate_random_int(100000, 999999),
            'role': '\'master\'::public."userrole"',
            'condition': '\'dynamic\'::public."usercondition"',
            'status': '\'active\'::public."userstatus"',
            'balance': generate_random_int(0, 1000),
            'current_percentage': 15,
            'document_photo': '',
            'contract_photo': '',
            'city_id': db_cities[random.randint(0, len(db_cities) - 1)]['id'],
        }
        for i in range(100)
    ]

    db_users += [
        {
            'id': len(db_users) + 1,
            'tg_id': 1843959363,
            'fio': 'Glav operator',
            'phone': generate_random_int(1000000000, 9999999999),
            'email': f'{generate_random_string(5)}@example.ru',
            'iin': generate_random_int(100000, 999999),
            'role': '\'master\'::public."userrole"',
            'condition': '\'dynamic\'::public."usercondition"',
            'status': '\'active\'::public."userstatus"',
            'balance': generate_random_int(0, 1000),
            'current_percentage': 15,
            'document_photo': '',
            'contract_photo': '',
            'city_id': db_cities[random.randint(0, len(db_cities) - 1)]['id'],
        },
        {
            'id': len(db_users) + 2,
            'tg_id': 6665927862,
            'fio': 'Super admin',
            'phone': generate_random_int(1000000000, 9999999999),
            'email': f'{generate_random_string(5)}@example.ru',
            'iin': generate_random_int(100000, 999999),
            'role': '\'admin\'::public."userrole"',
            'condition': '\'fixed\'::public."usercondition"',
            'status': '\'active\'::public."userstatus"',
            'balance': generate_random_int(0, 1000),
            'current_percentage': 15,
            'document_photo': '',
            'contract_photo': '',
            'city_id': db_cities[random.randint(0, len(db_cities) - 1)]['id'],
        },
    ]

    order_status = [
        '\'created\'::public."orderstatus"',
        '\'assigned\'::public."orderstatus"',
        '\'executed\'::public."orderstatus"',
        '\'on_diagnostics\'::public."orderstatus"',
        '\'closed\'::public."orderstatus"',
        '\'cancelled\'::public."orderstatus"',
    ]

    db_orders = []
    for i in range(10000):
        operator = db_users[-1]
        master = random.choice(db_users)
        while master['id'] == operator['id']:
            master = random.choice(db_users)

        status = random.choice(order_status)
        closed_date = None
        if 'closed' in status:
            closed_date = (
                datetime.today()
                + timedelta(
                    days=random.randint(1, 10),
                    hours=random.randint(1, 5),
                )
            ).strftime('%Y-%m-%d %H:%M')

        order = {
            'master_id': master['id'],
            'operator_id': operator['id'],
            'city_id': master['city_id'],
            'executing_date': (
                datetime.today() + timedelta(days=random.randint(1, 10))
            ).strftime('%Y-%m-%d'),
            'executing_time': (
                datetime.today() + timedelta(hours=random.randint(1, 5))
            ).strftime('%H:%M'),
            'address': generate_random_string(20),
            'problem': generate_random_string(20),
            'cost': generate_random_int(0, 1000),
            'contact_phone': generate_random_int(1000000000, 9999999999),
            'status': status,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'note': generate_random_string(20),
            'closed': closed_date,
            'diagnostic_act_photo': '',
            'paycheck_photo': '',
            'act_photo': '',
        }
        db_orders.append(order)

    conn, cur = get_db_connect_currsor(
        dbname='master_union',
        user='your_db_username',
        password='your_db_password',
    )

    # Удаляем данные из таблиц
    cur.execute('DELETE FROM "order";')
    cur.execute('DELETE FROM "user";')
    cur.execute('DELETE FROM "city";')
    conn.commit()

    # Заполняем таблицу городов
    for city in db_cities:
        cur.execute(
            f"INSERT INTO city (id, name) VALUES "
            f"({city['id']}, '{city['name']}')",
        )

    # Заполняем таблицу пользователей
    for user in db_users:
        cur.execute(
            f"""
            INSERT INTO "user" (
                id,
                tg_id,
                fio,
                phone,
                email,
                iin,
                role,
                condition,
                status,
                balance,
                current_percentage,
                document_photo,
                contract_photo,
                city_id
            ) VALUES (
                {user['id']},
                {user['tg_id']},
                '{user['fio']}',
                {user['phone']},
                '{user['email']}',
                {user['iin']},
                {user['role']},
                {user['condition']},
                {user['status']},
                {user['balance']},
                {user['current_percentage']},
                '{user['document_photo']}',
                '{user['contract_photo']}',
                {user['city_id']}
            )
            """,
        )

    # Заполняем таблицу заказов
    for order in db_orders:
        if 'closed' in order['status']:
            sql_stmt = f"""
            INSERT INTO "order" (
                master_id,
                operator_id,
                city_id,
                executing_date,
                executing_time,
                address,
                problem,
                cost,
                contact_phone,
                status,
                created,
                note,
                closed,
                diagnostic_act_photo,
                paycheck_photo,
                act_photo
            ) VALUES (
                {order['master_id']},
                {order['operator_id']},
                {order['city_id']},
                '{order['executing_date']}',
                '{order['executing_time']}',
                '{order['address']}',
                '{order['problem']}',
                {order['cost']},
                {order['contact_phone']},
                {order['status']},
                '{order['created']}',
                '{order['note']}',
                '{order['closed']}',
                '{order['diagnostic_act_photo']}',
                '{order['paycheck_photo']}',
                '{order['act_photo']}'
            )
            """
        else:
            sql_stmt = f"""
            INSERT INTO "order" (
                master_id,
                operator_id,
                city_id,
                executing_date,
                executing_time,
                address,
                problem,
                cost,
                contact_phone,
                status,
                created,
                note,
                diagnostic_act_photo,
                paycheck_photo,
                act_photo
            ) VALUES (
                {order['master_id']},
                {order['operator_id']},
                {order['city_id']},
                '{order['executing_date']}',
                '{order['executing_time']}',
                '{order['address']}',
                '{order['problem']}',
                {order['cost']},
                {order['contact_phone']},
                {order['status']},
                '{order['created']}',
                '{order['note']}',
                '{order['diagnostic_act_photo']}',
                '{order['paycheck_photo']}',
                '{order['act_photo']}'
            )
            """
        cur.execute(sql_stmt)

    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
