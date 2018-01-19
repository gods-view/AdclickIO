import datetime

import logging
from ..model import PCampaign, PStatistics, PProvider, PApiToken
from ..rest import ZeroPark


def zeropark(retrive_new=False):
    """
    zeropark api with python
    :return:
    """
    provider = PProvider.get(name="zeropark")

    if retrive_new:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id, PApiToken.initialized == False).order_by())
    else:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id).order_by())

    for api_token in api_tokens:

        zeropark_api = ZeroPark(api_token.token)
        for i in range(0, 90):
            startdate = datetime.date.today() + datetime.timedelta(days=-i - 1)
            enddate = datetime.date.today() + datetime.timedelta(days=-i)

            campaigns = zeropark_api.campaign_all(startdate, enddate)
            reports = campaigns['elements']  # warning: may be not find

            print(reports)

            if str(reports) == '[]':
                if retrive_new:
                    continue
                else:
                    break

            for report in reports:
                try:
                    campaign_id = report['details']['id']
                    campaign_name = report['details']['name']
                    cost = report['stats']['spent']
                    conversions = report['stats']['conversions']
                except Exception as e:
                    logging.error(str(e))
                    continue

                # save in mysql
                doc = {
                    'provider': provider,
                    'api_token': api_token,
                    'campaign_identity': campaign_id,
                    'name': campaign_name
                }

                try:
                    PCampaign.insert(doc).execute()
                except Exception as e:
                    print(campaign_id, campaign_name)
                    "IntegrityError when save in mysql  !"
                    logging.warning("campaigns --> IntegrityError when save in mysql  !")
                    pass

                statistics = {
                    'provider': provider,
                    'api_token': api_token,
                    'campaign': PCampaign.get(provider=provider, campaign_identity=campaign_id),
                    'cost': cost,
                    'conversion': conversions,
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
