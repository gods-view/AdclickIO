import datetime
import logging
from ..model import PCampaign, PStatistics, PProvider, PApiToken, db
from ..rest import PropellerAds


def propellerads(retrive_new=False):
    """
        exoclick api with python
        :return:
    """
    provider = PProvider.get(name="propellerads")

    if retrive_new:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id, PApiToken.initialized == False).order_by())
    else:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id).order_by())

    for api_token in api_tokens:

        propellerasd_api = PropellerAds(api_token.token)

        for i in range(0, 90):
            startdate = datetime.date.today() + datetime.timedelta(days=-i - 1)
            enddate = datetime.date.today() + datetime.timedelta(days=-i)
            report = propellerasd_api.campaign_list(startdate, enddate)

            rows = report['result']['rows']  # warning: may be not find

            if str(rows) == '[]':
                if retrive_new:
                    continue
                else:
                    break

            for row in rows:

                try:
                    campaign_id = row['campaign_id']
                    clicks = row['click']
                    impressions = row['show']
                    cost = row['profit']
                    conversion = row['convers']
                except Exception as e:
                    logging.error(str(e))
                    continue

                # save in mysql

                doc = {
                    'provider': provider,
                    'api_token': api_token,
                    'campaign_identity': campaign_id,
                    # 'name': campaign_name
                }

                try:
                    PCampaign.insert(doc).execute()
                except Exception as e:
                    "IntegrityError when save in mysql  !"
                    print(campaign_id)
                    logging.warning("campaigns --> IntegrityError when save in mysql  !")
                    pass

                statistics = {
                    'provider': provider,
                    'api_token': api_token,
                    'campaign': PCampaign.get(provider=provider, campaign_identity=campaign_id),
                    'cost': cost,
                    'impression': impressions,
                    'click': clicks,
                    'conversion': conversion,
                    'date': enddate,
                }

                try:
                    PStatistics.insert(statistics).execute()
                except Exception as e:
                    "IntegrityError when save in mysql  !"
                    logging.warning("statistics --> IntegrityError when save in mysql  !")
                    pass

            if not retrive_new:
                break

        if retrive_new:
            api_token.initialized = True
            api_token.save()
