def store_media_on_disk(media_file, file_path):
    """
    @param media_file: the files that should be uploaded
    @param file_path: where the file shouldbe uploaded
    """
    
    dest = open(file_path, 'wb+')
    
    for chunk in media_file.chunks(): 
        dest.write(chunk)
    dest.close()