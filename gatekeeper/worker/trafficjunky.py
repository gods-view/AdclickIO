import datetime
import logging
from ..model import PCampaign, PStatistics, PProvider, PApiToken, db
from ..rest import TrafficJunky


def trafficjunky(retrive_new=False):
    """
        trafficjunky api with python
        :return:
    """
    provider = PProvider.get(name="trafficjunky")

    if retrive_new:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id, PApiToken.initialized == False).order_by())
    else:
        api_tokens = (PApiToken.select(PApiToken).join(
            PProvider).where(PProvider.id == provider.id).order_by())

    for api_token in api_tokens:

        trafficjuck_api = TrafficJunky(api_token.token)

        try:
            campaign_list = trafficjuck_api.campaign_list()
        except Exception as e:
            logging.error(e)
            continue

        for campaign in campaign_list:
            try:
                campaign_id = campaign['campaign_id']

                for i in range(0, 90):
                    startdate = datetime.date.today() + datetime.timedelta(days=-i - 1)
                    enddate = datetime.date.today() + datetime.timedelta(days=-i)

                    campaignstats = trafficjuck_api.campaigns_stats(campaign_id,startdate,enddate)

                    campaign_detail = campaignstats[str(campaign_id)]
                    campaign_name = campaign_detail['campaign_name']
                    clicks = campaign_detail['clicks']
                    impressions = campaign_detail['impressions']
                    cost = campaign_detail['cost']

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
                        "IntegrityError when save in mysql  !"
                        print(campaign_id, campaign_name)
                        logging.warning("campaigns --> IntegrityError when save in mysql  !")
                        pass

                    statistics = {
                        'provider': provider,
                        'api_token': api_token,
                        'campaign': PCampaign.get(provider=provider, campaign_identity=campaign_id),
                        'cost': cost,
                        'click': clicks,
                        'impression': impressions,
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

            except Exception as e:
                "get data error"
                logging.error(str(e))
                continue

        if retrive_new:
            api_token.initialized = True
            api_token.save()