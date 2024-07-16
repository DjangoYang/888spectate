import aiosqlite


async def database_connection(db_name):
    return DBContextManager(db_name)


async def setup_database(db):
    query = """
        CREATE TABLE IF NOT EXISTS sport(
            id INTEGER PRIMARY KEY,
            name VARCHAR(45) NOT NULL,
            slug VARCHAR(45) UNIQUE NOT NULL,
            active TINYINT DEFAULT 1
        );
    """
    await execute_query(db, query)

    query = """
        CREATE TABLE IF NOT EXISTS `event` (
            `id` INTEGER PRIMARY KEY,
            `name` VARCHAR(45) NOT NULL,
            `active` TINYINT DEFAULT 1,
            `slug` VARCHAR(45) UNIQUE NOT NULL,
            `type` VARCHAR(45) NOT NULL,
            `status` VARCHAR(45) NOT NULL,
            `start_time` DATETIME NULL,
            `actual_start_time` DATETIME NULL,
            `sport_id` INTEGER NOT NULL,
            `logos` VARCHAR(255) NULL,
            CONSTRAINT `sport_id`
                FOREIGN KEY (`sport_id`)
                REFERENCES `sport` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION
        )
    """
    await execute_query(db, query)

    query = """
        CREATE TABLE IF NOT EXISTS `selection` (
            `id` INTEGER PRIMARY KEY,
            `name` VARCHAR(45) NOT NULL,
            `price` INTEGER NOT NULL,
            `active` TINYINT DEFAULT 1,
            `outcome` VARCHAR(45) NOT NULL,
            `event_id` INTEGER NOT NULL,
            CONSTRAINT `event_id`
                FOREIGN KEY (`event_id`)
                REFERENCES `event` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION
        )
    """
    await execute_query(db, query)


class DBContextManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_name)
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


async def execute_query(db, query, params=None):
    async with db as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, params)
        await conn.commit()


async def fetch_all(db, query, params=None):
    async with db as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, params)
        result = await cursor.fetchall()
        result_dicts = [
            dict(zip([column[0] for column in cursor.description], row))
            for row in result
        ]
        if result is None:
            return []
        return result_dicts


async def fetch_one(db, query, params=None):
    async with db as conn:
        cursor = await conn.cursor()
        await cursor.execute(query, params)
        result = await cursor.fetchone()
        if result is None:
            return {}
        result_dict = dict(zip([column[0] for column in cursor.description], result))
        return result_dict
