#!/usr/bin/env python

import sys, glob, os, time
    
usage = '''
Usage:    jot [command]
For help: jot help
'''
    
def main():
    '''Get, interpret, and pass on any commands'''
    
    # Find and import support files
    path = os.getenv('HOME') + '/.jot'
    sys.path.append(path)

    # Class modules
    from lib import item, connection, peer

    # Command modules
    from bin import add, version, remove, show, util, \
            config, search, edit, pull, push, clone, \
            log, tag

    # Parse the configuration file
    config = util.parseConfig()

    # Apply changelog
    util.processChangelog()

    # Parse the command/arguments
    args = []
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        return False
    if len(sys.argv) > 2:
        args = util.parseArgs(sys.argv[2:])
    if len(args) > 0:
        args = util.parseArgs(args)

    # Create a database connection
    db = connection.Connection()

    # Pass off the db and any arguments to a 
    # command-specific function.
    if command == 'add':
        add.add(db,args,config)
    elif command == 'version':
        version.version()
    elif command == 'remove' or command == 'rm':
        remove.remove(db,args)
    elif command == 'config':
        config.config(args)
    elif command == 'show':
        show.show(db,args)
    elif command == 'search':
        search.search(db,args)
    elif command == 'edit':
        edit.edit(db,args,config)
    elif command == 'pull':
        pull.pull(args)
    elif command == 'push':
        push.push(args)
    elif command == 'clone':
        clone.clone(db,args)
    elif command == 'log':
        log.log(args,config)
    elif command == 'tag':
        tag.tag(db,args)
    elif command == 'help':
        help()
    else:
        print util.decorate('FAIL','Fatal: Command not recognized.')
        guess = util.guessCommand(command)
        if guess is not None:
            print 'Did you mean:',' or '.join(guess)
        return False
    return True

def help():
    print """
Reference Keywords
--------------------------------------------------------------------------------------
Like commit references in Git, you can reference notes in Jot. Besides using the 
note's unique identifier, you can use a number of keywords that represent one or more
notes. The keywords are universal, excepting the fact that some commands take only 
singular references. 

    Singular (all commands)

        last      -- most recent note         
        last^     -- 2nd most recent note
        last^^    -- 3rd most recent note
        last~[n]  -- nth most recent note (up to 9)
        [hash]    -- note (partially) matching the hash

    Plural (can't be used with tag or edit)

        last[n]   -- n most recent notes (up to 9)
        all       -- all notes

--------------------------------------------------------------------------------------

add                       When called without arguments, the add command opens a
                          shell editor. The editor Jot will open is specified by the
                          system's $EDITOR variable. If not set, Jot will default
                          to vi. It will then create a temporary file in the system's
                          tmp directory. When you finish editing, you only need to 
                          save the file. Jot will capture its content. 

    -m [string]           Add the note using the given string, skipping the editor.
    --manual [string]     Strings with spaces meed to be wrapped in quotation marks.

    -t [string]           Associate the note with a tag formed from the given
    --tag [string]        string. Multiple tags can be assigned by providing-comma
                          seperated-values. As with above, if the string contains
                          spaces, it needs to be quoted.

edit [reference]          Open the specified note for editing. Requires a singular
                          note reference.

show [reference/tag]      The show command is the primary method for viewing Jot's
                          notes. When called with no arguments, it will display the 5
                          most recent notes. You can optionally give it a reference
                          or a tag as an argument. The show command will evaluate the 
                          argument you give it in the following order:
                            
                                1. Is it a keyword?
                                2. Is it a tag?
                                3. Is it a unique identifier?

                          This means that if your tag is also a keyword, it will
                          evaluate it as such. The same applies to unique identifiers,
                          although collisions are far less likely. 

remove [reference]        This command will remove a note from Jot's database. 
                          Although permanent, it may be possible to manually recover 
                          the note from the log or a peer that you have pushed to or 
                          pulled from. The remove command will accept any of the 
                          keywords shown above. Use with caution, as it is possible 
                          to wipe all notes with:

                                $ jot remove all

tag [reference] [tag]     Manually associates a single note with one or more tags. 
                          Provide a singular reference and a string with one or more
                          comma separated values, which represent tags. As above, quote
                          the string if it contains spaces.
                          
                          If you need to remove a tag, you can use the following syntax:

                                $ tag remove [reference] [tag]
                          

search [query]            Search all notes for content fields that contain the query
                          string. Like the tag command, spaces are fair game, provided 
                          the query is enclosed in quotation marks. 
                          
                          Where supported, Jot will use full-text search, which
                          may be more accurate than the fallback (LIKE syntax). Upon 
                          installation, Jot will tell you if it needs to fallback.

push [(user@)host]        Push local changes to the remote peer. The connection is through
                          SSH, so you may provide any hostname/IP that SSH would accept. 
                          Unless you have a key set up, you'll be required to enter your
                          password. 
                          
                          On each run, Jot looks for and processes pushed changes. This 
                          means that upon running any command, the remote host will add 
                          the new changes to its database. By doing things this way, 
                          Jot doesn't need to run in the background--nobody needs another 
                          zombie process anyway.

pull [(user@)host]        Same procedure as the push command. In this case, changes are
                          pulled from the remote host and processed immediately.

version                   Displays the Jot's version information. 

log                       Dumps Jot's logs. Jot uses the Pickle module to pickle these,
                          so the command is reading, unpickling, and outputing the log 
                          files.
"""

if __name__ == '__main__':
    result = main()
    if not result:
        print usage
