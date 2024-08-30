import pymysql


def transfer_data(source_config, dest_config, query, table_name):
    """
    从源数据库按筛选条件取出数据，并追加到目标数据库的表中。

    :param source_config: 源数据库配置，包含host, user, password, database等信息的字典。
    :param dest_config: 目标数据库配置，包含host, user, password, database等信息的字典。
    :param query: 从源数据库中提取数据的查询语句。
    :param table_name: 目标数据库中表的名称。
    """
    # 连接源数据库
    source_conn = pymysql.connect(
        host=source_config['host'],
        user=source_config['user'],
        password=source_config['password'],
        database=source_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    # 连接目标数据库
    dest_conn = pymysql.connect(
        host=dest_config['host'],
        user=dest_config['user'],
        password=dest_config['password'],
        database=dest_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with source_conn.cursor() as source_cursor, dest_conn.cursor() as dest_cursor:
            # 执行查询，提取数据
            source_cursor.execute(query)
            rows = source_cursor.fetchall()

            # 生成插入语句
            if rows:
                columns = ', '.join(rows[0].keys())
                placeholders = ', '.join(['%s'] * len(rows[0]))
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                # 插入数据到目标数据库
                for row in rows:
                    dest_cursor.execute(insert_query, tuple(row.values()))

                # 提交事务
                dest_conn.commit()

    except Exception as e:
        print(f"Error: {e}")
        dest_conn.rollback()

    finally:
        source_conn.close()
        dest_conn.close()


# 示例用法
source_db_config = {
    'host': '193.112.190.33',
    'user': 'bmsh0516-pro',
    'password': 'kGwTtenrPTSBA8n3',
    'database': 'bmsh0516-pro'
}


dest_db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'wjy201121',
    'database': 'sys'
}

sql_query = "SELECT * FROM u_book_info WHERE type = 2 "
target_table = "dest_table"

transfer_data(source_db_config, dest_db_config, sql_query, target_table)
