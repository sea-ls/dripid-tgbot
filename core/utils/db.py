import aiosqlite


class AsyncSQLiteDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_name)

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def execute(self, query, parameters=None):
        async with self.connection.execute(query, parameters) as cursor:
            return await cursor.fetchall()

    async def commit(self):
        await self.connection.commit()

    async def insert_data(self, table_name, column, values):
        query = f"INSERT INTO {table_name} ({column}) VALUES ({values}) ON CONFLICT DO NOTHING"
        await self.execute(query)
        await self.commit()

    async def select_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        return await self.execute(query)

    async def select_data(self, table_name, condition):
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        return await self.execute(query)

    async def select_all_columns(self, table_name, columns):
        query = f"SELECT {columns} FROM {table_name}"
        return await self.execute(query)

    async def select_columns(self, table_name, columns, condition):
        query = f"SELECT {columns} FROM {table_name} WHERE {condition}"
        return await self.execute(query)

    async def select_exists(self, table_name, condition):
        query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {condition} LIMIT 1)"
        result = await self.execute(query)
        return result[0][0] == 1

    async def delete_data(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        await self.execute(query)
        await self.commit()

    async def update_data(self, table_name, set_values, condition):
        query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
        await self.execute(query)
        await self.commit()