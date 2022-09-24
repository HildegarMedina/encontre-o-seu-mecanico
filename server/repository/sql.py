class Repository:
    
    def __init__(self, db):
        self.db = db
    
    async def execute_many(self, query, values=None):
        return await self.db.execute_many(query=query, values=values)

    async def execute(self, query, values=None):
        return await self.db.execute(query=query, values=values)

    async def fetch_one(self, query, values=None):
        return await self.db.fetch_one(query=query, values=values)
    
    async def fetch_all(self, query, values=None):
        return await self.db.fetch_all(query=query, values=values)