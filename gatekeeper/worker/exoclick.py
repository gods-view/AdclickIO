import datetime
import logging
from ..model import PCampaign, PStatistics, PProvider, PApiToken, db
from ..rest import ExoClick


def exoclick(retrive_new=False):
    """
        exoclick api with python
        :return:
    """
    provider = PProvider.get(name="exoclick")

    if retrive_new:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id, PApiToken.initialized == False).order_by())
    else:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id).order_by())

    for api_token in api_tokens:

        exo_api = ExoClick(api_token.token)

        try:
            reports = exo_api.campaign_list()
            result = reports['result']
            print(type(result))
            if not len(result) > 0:
                logging.warning(str(api_token) + ' no campaign list , continue next user ')
                continue
        except Exception as e:
            logging.error(str(e))
            continue

        for campaign_id in result:
            campaign_name = result[str(campaign_id)]['name']

            if retrive_new:
                response = exo_api.statistics(campaign_id, quick=datetime.date.today() + datetime.timedelta(days=-90))
            else:
                response = exo_api.statistics(campaign_id, quick=datetime.date.today() + datetime.timedelta(days=-1))

            res = response['result']
            if str(res) == '[]':
                print(campaign_id + ' has no data, continue next')
                continue

            for re in res:
                try:
                    clicks = re['clicks']
                    cost = re['cost']
                    date = re['ddate']
                    impressions = re['impressions']
                except:
                    "get data error"
                    print("get data error")
                    continue

                # # save in mysql

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
                    'impression': impressions,
                    'click': clicks,
                    'date': date
                }

                try:
                    PStatistics.insert(statistics).execute()
                except Exception as e:
                    "IntegrityError when save in mysql  !"
                    logging.warning("statistics --> IntegrityError when save in mysql  !")
                    pass

        if retrive_new:
            api_token.initialized = True
            api_token.save()
