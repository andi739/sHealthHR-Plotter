import pandas as pd

def import_data(csv_path, csv_filename, json_path=None):
    """reads data and returns a processed dataFrame. 

    Args:
        csv_path (_type_): location of the heart_rate csv-file. Has to end with \\ or /
        csv_filename (_type_): name of the file with type
        json_path (_type_, optional): optional. location of the json heart_rate bin folders. May lead to errors if left empty. Has to end with \\ or /
    """    ''''''
#set bin path
    if json_path==None:
        json_path = csv_path+"jsons/com.samsung.shealth.tracker.heart_rate/"
    
#get unbinned data
    df_csv = pd.read_csv(csv_path+csv_filename, dtype="string", skiprows=[0], index_col=False)
    #only take rows without bin entries 
    df_fin = df_csv.loc[df_csv["com.samsung.health.heart_rate.binning_data"].isna()][['com.samsung.health.heart_rate.heart_rate', 'com.samsung.health.heart_rate.start_time', 'com.samsung.health.heart_rate.comment']].rename(columns={'com.samsung.health.heart_rate.heart_rate' : 'heart_rate', 'com.samsung.health.heart_rate.start_time' : 'date_time', 'com.samsung.health.heart_rate.comment' : 'comment'})
    df_fin['heart_rate'] = df_fin['heart_rate'].astype(float).astype('int64')
    df_fin['date_time'] = df_fin['date_time'].astype('datetime64[ns]')
    #zero seconds
    df_fin['date_time'] = df_fin['date_time'].dt.floor(freq='min')
#get binned data    
    bins = df_csv['com.samsung.health.heart_rate.binning_data'].dropna().unique()
    for bin in bins:

        #read_json
        json = pd.read_json(path_or_buf=json_path+bin[0]+'/'+bin)
        #take relevant columns
        json = json[['heart_rate', 'start_time']].rename(columns={'start_time':'date_time'})
        #add bin comment to first json object
        json['comment'] = pd.NA
        comm = df_csv.loc[df_csv['com.samsung.health.heart_rate.binning_data'] == bin]['com.samsung.health.heart_rate.comment'].dropna()
        if not comm.empty:
            json.at[0, 'comment'] = comm.values[0]
        #append to dataframe
        df_fin = pd.concat([df_fin, json], ignore_index=True)


    #sort by date
    df_fin.sort_values(by='date_time', inplace=True)
    #drop duplicates by time. COULD REMOVE COMMENTED
    #df_fin.drop_duplicates(subset=['date_time'], keep='last', inplace=True)
    
    return df_fin    
#TODO size limit, das bei z.b. 10 jahren daten das programm nicht crashed -> muss dann intelinked werden mit user input controls