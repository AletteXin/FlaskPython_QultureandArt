import os
from urllib.parse import urlparse

def parse_db_url(database_url):
    parsed = urlparse(database_url)
    return {
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port,
        'database': parsed.path[1:]
    }

def return_db():
    db_config = parse_db_url(os.environ['DATABASE_URL'])

    if os.getenv('MIGRATION', '0') == '1':
        from playhouse.postgres_ext import PostgresqlExtDatabase
    
        return PostgresqlExtDatabase(   
#             os.environ['DATABASE_URL'],
            os.environ['RDS_READS_DB_NAME'],
#             database = os.environ('RDS_READS_DB_NAME'),
#             'qulturenart',
#             user = 'qultureandart26',
#             password = 'thisisthepassword',
#             host = 'qulturenart.cbmasmhporwp.us-east-1.rds.amazonaws.com',
#             port = '5433'       
            user = os.environ('RDS_USER'),
            password = os.getenv('RDS_DB_PASS'),
            host = os.environ('RDS_HOST'),
            port = os.environ('RDS_DB_PORT'),
#             db_config['database'],
#             user=db_config.get('user', None),
#             password=db_config.get('password', None),
#             host=db_config.get('host', 'localhost'),
#             port=db_config.get('port', '5432')
        )

    else:
        from playhouse.pool import PooledPostgresqlExtDatabase

        return PooledPostgresqlExtDatabase(
# #             os.environ['DATABASE_URL'],
            os.environ['RDS_READS_DB_NAME'],
#             database = os.getenv('RDS_READS_DB_NAME'),
#             'qulturenart',
#             user = 'qultureandart26',
#             password = 'thisisthepassword',
#             host = 'qulturenart.cbmasmhporwp.us-east-1.rds.amazonaws.com',
#             port = '5433'
            user = os.environ('RDS_USER'),
            password = os.environ('RDS_DB_PASS'),
            host = os.environ('RDS_HOST'),
            port = os.environ('RDS_DB_PORT'),
            max_connections=os.environ('DB_POOL', 5),
            stale_timeout=os.environ('DB_TIMEOUT', 300),  # 5 minutes.
#             db_config['database'],
#             user=db_config.get('user', None),
#             password=db_config.get('password', None),
#             host=db_config.get('host', 'localhost'),
#             port=db_config.get('port', '5432')
        )
    

db = return_db()
