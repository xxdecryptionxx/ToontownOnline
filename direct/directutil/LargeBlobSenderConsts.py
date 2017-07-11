# File: d (Python 2.4)

USE_DISK = 1
ChunkSize = 100
FilePattern = 'largeBlob.%s'

def getLargeBlobPath():
    return config.GetString('large-blob-path', 'i:\\toontown_in_game_editor_temp')

