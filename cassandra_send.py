import cassandra
# print(cassandra.__version__)
from u_info import user_info

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


# configure with cassandra cloud
cloud_config= {
        'secure_connect_bundle': 'secure-connect-database1.zip'
}
auth_provider = PlainTextAuthProvider('sWSsgfrfxpukXnmXnHkxZbRI', 'YUcLBrvHMnq_piJZbhad,UQzPPX3NLKyWOg1pi9ar6KR78XIps774i6xK1DxDXmn9AJeBf-359uxfB.6w,fqmKajtG_8Ak,ZZ-nMOfxT7-cnHm,ghpOZw2GP82uGbAfc')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
    print(row[0])
else:
    print("An error occurred.")


# sending data to cassandra
def send_user_info():
    try:
        val = user_info()
        pre = session.prepare("insert  into car_price_prediction.user_info (time,ip,city,region,country_name,latitude,longitude) values(?,?,?,?,?,?,?)")
        session.execute(pre.bind(val))
    except Exception as e:
        print(e)

# car_price_pred_user_info()
