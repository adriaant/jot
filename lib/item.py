import hashlib, os, tempfile, time, sys
from bin import util 
from datetime import datetime 

class Item:
    '''Creates a jot item with an identifier and various methods.'''
    def __init__(self, db, identifier=None, priority=None, content=None, tags=None, timestamp=None):
        '''Creates a new jot item, with new or preset attributes'''

        # By setting parameters, we can create a clone of any previous Item instance that's
        # attributes are saved in the database. This is handled by giving an identifier to
        # the getItem method of the Connection class, which then creates the clone with the
        # appropriate parameters.

        if timestamp is None:
            self.timestamp = time.time()
        else:
            self.timestamp = float(timestamp)
        if identifier is None:
            self.identifier = hashlib.md5(str(time.time())).hexdigest()
        else:
            self.identifier = identifier
        if priority is None:
            self.priority = priority
        else:
            self.priority = priority
        if tags is None or type(tags) is not list:
            self.tags = []
        if type(tags) is list:
            if tags[0] == '': 
                # the Connection object will initialize items with tag parameters as a list 
                # containing a single empty string (when the tags field is empty). This seems 
                # to be the cleanest way to take care of this.
                self.tags = []
            else:
                self.tags = tags
        self.content = content
        self.db = db

    def edit(self,editor=None):
        '''Launch an editor with a tempfile containing the item's content for editing.'''
        if editor is None:
            editor = util.choose_editor()
        # Launch the editor with a tempfile 
        path = tempfile.mkstemp()[1]
        if self.content is not None:
            fp = open(path,'a')
            fp.write(self.content) # write the current content to the temp file
            fp.close()
        syscall = editor + ' ' + path
        os.system(syscall)
        if os.path.exists(path):
            fp = open(path,'r')
            self.content = ''.join([line for line in fp])
            fp.close()
            return True
        else:
            print 'Aborting'
            return False
        
    def save(self,commit=True):
        '''Puts the item in the local database.'''
        if self.content is not None:
            if self.db.grabItem(self.identifier,quiet=True) is not None: # update the row if it already exists.
                self.db.updateItem(self,commit)
            else:
                self.db.insertItem(self,commit)

    def remove(self,commit=True):
        '''Removes the item from the local database.'''
        self.db.deleteItem(self,commit)

    def display(self):
        '''Prints the item's attributes.'''
        content = ''
        prettyTime = datetime.fromtimestamp(self.timestamp).strftime('%a %b %d %H:%M')
        for ch in self.content:
            if ch == '\n':
                content += '\n          '
            else:
                content += ch
        if sys.stdout.isatty():
            print 'Hash:    ', util.decorate('WARNING',self.identifier)
            print 'Time:    ', util.decorate('WARNING',prettyTime)
            print 'Priority:', util.decorate('WARNING',self.priority)
            print 'Tags:    ', util.decorate('OKGREEN',','.join(self.tags))
            print 'Content: ', content
            print
        else:
            print 'Hash:    ', self.identifier
            print 'Time:    ', prettyTime
            print 'Priority:', self.priority
            print 'Tags:    ', ','.join(self.tags)
            print 'Content: ', content
            print

