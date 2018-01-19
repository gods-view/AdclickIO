from datetime import datetime, date

import logging
import peewee
from ..model import PCampaign, PStatistics, PProvider, PApiToken, db
from ..rest import Popads


def popads(retrive_new=False):
    """
    popads api with python
    :return:
    """
    provider = PProvider.get(name="popads")

    if retrive_new:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id, PApiToken.initialized == False).order_by())
    else:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id).order_by())

    for api_token in api_tokens:
        popads_api = Popads(api_token.token)
        try:
            if retrive_new:
                report = popads_api.report_advertiser(quick='last_90_days')
            else:
                report = popads_api.report_advertiser(quick='yesterday')
            if not len(report['rows']) > 0:
                logging.warning(str(api_token) + ' no data , continue next user ')
                continue
        except Exception as e:
            logging.error(e)
            continue

        # save in mysql
        campaigns = list(map(lambda data: {
            'provider': provider,
            'api_token': api_token,
            'name': data['campaign'],
            'campaign_identity': data['campaign_id']
        }, report['rows']))

        try:
            if len(campaigns) > 0:
                q = PCampaign.insert_many(campaigns).sql()
                db.execute_sql(
                    q[0] + ' on duplicate key update name=name ', q[1])
        except peewee.IntegrityError:
            "IntegrityError when save in mysql  !"
            logging.warning("campaigns --> IntegrityError when save in mysql  !")
            pass

        statistics = list(map(lambda data: {
            'provider': provider,
            'api_token': api_token,
            'campaign': PCampaign.get(provider=provider, campaign_identity=data['campaign_id']),
            'cost': data['cost'],
            'impression': data['impressions'],
            'conversion': data['conversion_count'],
            'date': data['datetime'],
        }, report['rows']))

        try:
            if len(statistics) > 0:
                q = PStatistics.insert_many(statistics).sql()
                db.execute_sql(
                    q[0] + ' on duplicate key update provider_id=provider_id ', q[1])
        except peewee.IntegrityError:
            "IntegrityError when save in mysql  !"
            logging.warning("statistics --> IntegrityError when save in mysql  !")
            pass

        if retrive_new:
            api_token.initialized = True
            api_token.save()
