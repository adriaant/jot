import util, sqlite3
from item import Item

class Connection:
    '''Creates a sqlite3 database connection and offers methods for selecting, deleting,
       and updating items. All actions are written to the changelog.'''

    def __init__(self,path='~/.todo/todo.db',changelog='~/.todo/todo.changelog',verbose=False):
        '''Constructs a Connection object with option to set locations and verbosity'''
        self.path = util.matchPath(path)
        self.cursor = None
        self.connected = False
        self.verbose = verbose
        self.changelog = changelog
        try:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            self.connected = True
        except sqlite3.Error:
            print 'Fatal: Could not connect to database.'

    def insertItem(self,item):
        '''Inserts an item.'''

        query = 'insert into todo(hash,descrip,priority,ts) values("%s","%s","%s","%s")' \
            % (item.identifier, item.content, item.priority, item.timestamp)
        if self.connected:
            self.cursor.execute(query)
            self.commit()
            self.log(query) # Need to log any queries that add, remove, or modify table rows

    def deleteItem(self,item):
        '''Deletes an item.'''

        query = 'delete from todo where hash="%s"' % (item.identifier)
        if self.connected:
            self.cursor.execute(query)
            self.commit()
            self.log(query)
    
    def updateItem(self,item):
        '''Updates an item.'''

        query = 'update todo where hash="%s"' % (item.identifier)
        if self.connected:
            self.cursor.execute(query)
            self.commit()
            self.log(query)

    def grabItem(self, identifier):
        '''Given an identifier hash, returns an Item object.'''

        identifier = self.matchIdentifier(identifier)
        if identifier is None:
            return None
        query = 'select * from todo where hash="%s"' % (identifier)
        if self.connected:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                item = Item(db=self,identifier=row[0],content=row[1],priority=row[2],timestamp=row[3])
                return item
            else:
                return None

    def grabMostRecent(self, n=1):
        '''Returns the n most recent items from the database as a list of Item objects.'''

        query = 'select * from todo order by ts desc'
        if self.connected:
            self.cursor.execute(query)
            rows = self.cursor.fetchmany(n)
            items = []
            if len(rows) > 0:
                for row in rows:
                    item = Item(db=self,identifier=row[0],content=row[1],priority=row[2],timestamp=row[3])
                    items.append(item)
                return items
            else:
                return None

    def grabAll(self):
        '''Returns all items from the database as a list of Item objects.'''

        query = 'select * from todo order by ts desc'
        if self.connected:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            items = []
            if len(rows) > 0:
                for row in rows:
                    item = Item(db=self,identifier=row[0],content=row[1],priority=row[2],timestamp=row[3])
                    items.append(item)
                return items
            else:
                return None

    def matchIdentifier(self,identifier):
        '''Since entering partial identifier hashes is allowed, we need a way to match them'''

        query = 'select hash from todo where hash like "%s%%"' % identifier 
        if self.connected:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            if len(rows) == 0:
                print util.decorate('FAIL','Fatal: No identifier could be matched')
                return None 
            if len(rows) > 1:
                print util.decorate('FAIL','Fatal: Supplied identifier has multiple matches, please be more specific.')
                return None 
            else:
                return str(rows[0][0])

    def commit(self):
        '''Commit the change(s) to the database.'''
        if self.connected:
            self.connection.commit()
            return True
        return False

    def log(self,query):
        '''Logs queries to the changelog which may be distributed to peers.'''
        try:
            if self.verbose:
                print query
            log = open(self.changelog,'a')
            log.write(query)
            log.close()
            return True
        except:
            return False

