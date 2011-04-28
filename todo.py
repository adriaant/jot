#!/usr/bin/env python

import sys, glob, os
    
# Overview:
#   The program is run by typing todo in to the shell followed
#   by a single whitespace, a command that tells it what to do,
#   and possibly subcommands and/or arguments.
#
# Examples:
#   todo show
#       --lists 5 most recent todo items
#   todo add    
#       --opens the default editor to enter a todo item
#   todo add -m "item text"   
#       --the same thing without using an editor
#   todo version 
#       --displays version information
#   todo config show
#       --opens the configuration file in the default editor
#   todo remove [hash]
#       --removes the todo item with the given hash identifier
#   todo remove last
#       --removes the most recently created todo item
#   todo remove all
#       --removes all todo items
#   todo peers show
#       --lists peers from the todo.config file

def main():
    '''Get, interpret, and pass on any commands'''

    # Find and import support files
    path = matchPath('~/.todo')
    sys.path.append(path)
    from todolib import item, connection, util
    from todolib import add, version, remove, show, peer, config

    # Parse the configuration file
    config = { 'peers' : {} }
    config = util.parseConfig(config)

    # Apply changelog


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
        add.add(db,args)
    if command == 'version':
        version.version()
    if command == 'remove':
        remove.remove(db,args)
    if command == 'config':
        config.config(args)
    if command == 'peers':
        peer.peer(args)
    if command == 'show':
        show.show(db,args)
    return True

def matchPath(path):
    '''Matches file paths with bash wildcards and shortcuts to an
       absolute path'''
    import os
    if path[0] == '~':
        path = os.getenv('HOME') + path[1:]
    newPath = glob.glob(path)
    if len(newPath) == 0:
        print 'Fatal: Could not match path: "%s"' % path
        return False
    newPath = newPath[0]
    return os.path.abspath(newPath)

if __name__ == '__main__':
    usage = '''
Usage: todo [command]
For help: todo help
    '''
    result = main()
    if not result:
        print usage
