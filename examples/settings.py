from sams.default_settings import env

# Common settings across both apps

#: full mongodb connection uri
MONGO_URI = env('SAMS_MONGO_URI', 'mongodb://localhost/sams')

#: elastic url
ELASTICSEARCH_URL = env('SAMS_ELASTICSEARCH_URL', 'http://localhost:9200')

#: elastic index name
ELASTICSEARCH_INDEX = env('SAMS_ELASTICSEARCH_INDEX', 'sams')

#: Public URL used in `api` HATEOAS responses for downloading from the `file_server`
SAMS_PUBLIC_URL = env('SAMS_PUBLIC_URL', 'http://localhost:5750')

# Configure the StorageDestinations
STORAGE_DESTINATION_1 = 'MongoGridFS,files,mongodb://localhost/sams_files'
STORAGE_DESTINATION_2 = 'MongoGridFS,media,mongodb://localhost/sams_media'
