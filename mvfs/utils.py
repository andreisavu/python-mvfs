
import os
import errno

def mkdir_p(path):
    """ Create a hierarchy of directories. 

    Same functionality as the shell command mkdir -p

    Credits: http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    """
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errrno == errno.EEXIST:
            pass
        else:
            raise

