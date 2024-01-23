class SystemConfig:
    DEBUG = True

    # SQLALCHEMY_DATABASE_URI = '{engine}://{username}:{password}@{host}:{port}/{database}?charset={charset}'.format(**{
    #     'engine': 'mysql+pymysql'
    #     ,'host': 'sc-m-db'
    #     ,'port': 3306
    #     ,'username': 'root'
    #     ,'password': 'scmysql080'
    #     ,'database': 'scapp'
    #     ,'charset': 'utf8'
    # })

    SQLALCHEMY_DATABASE_URI = '{engine}://{username}:{password}@{host}:{port}/{database}?client_encoding={charset}'.format(**{
        'engine': 'postgresql+psycopg2'
        ,'host': 'p-db'
        ,'port': 5432
        ,'username': 'postgres'
        ,'password': 'postgres080'
        ,'database': 'smartcrm'
        ,'charset': 'utf8'
    })

Config = SystemConfig
