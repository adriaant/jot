import os,glob

def decorate(colorCode,text):
    '''Returns a string enveloped by an ANSI color code'''
    colors = {'HEADER' : '\033[95m',
              'OKBLUE' : '\033[94m',
              'OKGREEN' : '\033[92m',
              'WARNING' : '\033[93m',
              'FAIL' : '\033[91m',
              'ENDC' : '\033[0m'}
    return colors[colorCode] + text + colors['ENDC']

def parseArgs(args):
    '''Parse arguments that follow the command'''
    prevArg = None 
    parsedArgs = []
    for arg in args:
        # pairs arguments in to tuples
        if arg[0] == '-': 
            # the first char of the first element of the tuple must be a '-'
            if prevArg is not None:
                tup = prevArg,None
                parsedArgs.append(tup)
            prevArg = arg[1:]
        elif prevArg is not None:
            tup = prevArg,arg
            parsedArgs.append(tup)
            prevArg = None
        else:
            parsedArgs.append(arg)
    if prevArg is not None:
        tup = prevArg,None
        parsedArgs.append(tup)
    return parsedArgs

def parseConfig(config,path='~/.todo/todo.config'):
    '''Update configuration with settings from todo.config.'''
    path = matchPath(path)
    configfile = open(path,'r')
    for line in configfile:
        if line[0].isalpha():
            line = line.strip().split()
            if line[1] != '#':
                config[line[0]] = line[1]
    return config

def matchPath(path,mustExist=True):
    '''Matches file paths with bash wildcards and shortcuts to an
       absolute path'''
    if path[0] == '~':
        path = os.getenv('HOME') + path[1:]
    newPath = glob.glob(path)
    if len(newPath) == 0:
        if not mustExist:
            return path
        print 'Fatal: Could not match path: "%s"' % path
        return False
    newPath = newPath[0]
    return os.path.abspath(newPath)
