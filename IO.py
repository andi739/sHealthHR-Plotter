import os

AUTOLOAD_FILE_NAME = "autoload"
PROGRAM_FOLDER_NAME = "sHealthHrPlotter\\"

def __make_base_folder():
    """Check whether program folder in user/documents exists, if not create one.

    Returns:
        string: path of program folder
    """    
    path = os.environ['USERPROFILE'] + "\\documents\\" + PROGRAM_FOLDER_NAME
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def get_autoload_filepath():
    #check whether program folder in user/documents exists, if not create one.
    base_path = __make_base_folder()
    #check whether autoload file exists and get it's contents
    file_content = ""
    if os.path.isfile(base_path+AUTOLOAD_FILE_NAME):
        #file exists, so we get it's contents #maybe TODO add flags like last opened?
        f = open(base_path+AUTOLOAD_FILE_NAME, 'r')
        file_content = f.read()
        f.close()
    #TODO getAutoload-Filepath JSON [.json format]
    return file_content
    #TODO in summary: ..... If file is EMPTY also no autoload-filepath, returns empty string

def set_autoload_filepath(file_path):
    #check whether program folder in user/documents exists, if not create one.
    base_path = __make_base_folder()
    #create file or overwrite it
    f = open(base_path+AUTOLOAD_FILE_NAME, 'w+')
    #write path of saved project file
    f.write(file_path)
    f.close()
    return


def load_config():
    #check whether program folder in user/documents exists, if not create one.
    base_path = __make_base_folder()
    #TODO |loadCOnfig(Kommt später, Settings mit ConfigParser [.ini format]) 
        #point descr onHover or onClick 


def save_file():#mithilfe von file-explorer
    #TODO save - load df.to_pickle df.read_pickle !? Oder Sqlite?? ->mit extra infos, wie default display, etc. settings. matplot chart realtime generation (solangs nicht 10jahre dauert, da entweder ändern oder während des ladens nen Fenster ...loading...)
    pass
    set_autoload_filepath(path)

def load_file():#mithilfe von file-explorer
    pass


def new_file(): #TODO diese beiden fct's hier oder data_import? oder beide dateien zusammenführen?
    pass#New File From Raw Data
def add_data():
    pass#Add Raw Data To This File


#TODO implement file stuff for linux and test everything!