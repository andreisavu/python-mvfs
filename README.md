
Python Virtual Multi-version File System
========================================

An easy solution you can use if you need to store multiple or all versions.
The library is built on top of the standard filesystem.
You can edit older versions. Each version is stored in gzip format.

How the api looks like?
-----------------------

    import mvfs
    import mvfs.openers
    
    storage = mvfs.Storage('/base/folder/')
    storage = mvfs.Storage('/base/filder', opener=mvfs.openers.PlainFileOpener())

    # open the latest revision for reading
    f = storage.open('/some/file/path', 'r') 

    # open the revision created at this specific timestamp
    f = storage.open('/path', 'r', ts=2344) 

    # get a list of all the timestamps in descending order
    ersions = storage.get_versions('/path/to/file') 

    # a new revision is created
    f = storage.open('/existing/path', 'w') 

    # create a new context and open an older revision for writing
    with storage.open('/path/in/the/virtual/fs', 'w', ts=23) as f:
    f.write('something')

    # cleanup the virtual fs and maintain no more than 5 versions for each file
    storage.cleanup(versions=5)  


