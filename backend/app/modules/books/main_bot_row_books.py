import random
from flask import jsonify, request
from flask import current_app as app
import numpy as np

from app.logger import request_log_wrapper

def _main_bot_row_books():
    """
    Gets a randomized list of books of length 18.
    """

    print("ping - _main_bot_row_books")
    start = request.args.get("start_list")
    seed = request.args.get("seed")
    print("start: {0}; seed: {1}".format(start, seed))

    # declare pymysql client
    connection = app.config["PYMYSQL_CONNECTION"]

    # declare pymongo client
    mongo = app.config["MONGODB_CLIENT"]
    metadata = mongo.metadata.metadata

    start = int(start)
    random.seed(int(seed))
    count = int(metadata.count())
    total_lst = random.sample(range(count), count)
    end = start+18
    lst = total_lst[start:end]
    lst = list(np.array(lst,dtype=str))
    print("lst: {0}".format(lst))

    finaldict = {}
    outerlist = []

    met_data = metadata.find( { 'index': { '$in' : lst } }, { '_id':0,'title':1,'asin':1,'imUrl':1,'categories':1,'related':1 } )

    for j in met_data:
        temp = {}

        if 'title' in j:
            temp['title'] = j['title']

        temp['asin'] = j['asin']

        # averageRating = db.session.query(func.avg(amazonreviews.overall)).group_by(amazonreviews.asin).filter_by(asin=j['asin']).scalar()

        # pymysql query
        # query = "SELECT AVG(overall) FROM {0} WHERE asin=\'{1}\'".format(app.config["MYSQL_TABLE_REVIEWS"], temp['asin'])
        # with connection as cursor:
        # with connection.cursor() as cursor:
            # print("query: {0}".format(query))
            # cursor.execute(query)
            # query_result = cursor.fetchone()
            # averageRating = query_result["AVG(overall)"]
            # if averageRating:
                # averageRating = float(averageRating)
                # temp['averageRating'] = averageRating
            # else:
                # temp['averageRating'] = 0
        # cursor.close()

        if 'imUrl' in j:
            temp['imUrl'] = j['imUrl']
        else:
            temp['imUrl'] = None

        temp['categories'] = j['categories']

        outerlist.append(temp)


    finaldict['collection'] = outerlist


    # for logging received requests
    log_msg = request_log_wrapper(request)
    app.logger.info(log_msg)

    return(jsonify(finaldict))
