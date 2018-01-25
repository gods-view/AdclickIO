#!/usr/bin/env python
# encoding: utf-8

from peewee import *
from affiliate.model.config import mysql, mysql_report
import time

db = MySQLDatabase(mysql['name'],
                   host=mysql['host'],
                   port=int(mysql['port']),
                   user=mysql['user'],
                   passwd=mysql['passwd']
                   )


# 旧的数据库连接
class BaseModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = db


class CampaignMap(BaseModel):
    OurCampId = IntegerField(null=False, default=0)
    TheirCampId = CharField(null=False, default=0)

    class Meta:
        db_table = "CampaignMap"
        index = (('OurCampId', True), ('TheirCampId', True))


class User(BaseModel):
    idText = CharField(max_length=8, null=False)
    email = CharField(max_length=50, null=False)
    emailVerified = IntegerField(null=False, default=0)
    contact = TextField(null=False)
    password = CharField(max_length=256, null=False, default='')
    firstname = CharField(max_length=256, null=False, default='')
    lastname = CharField(max_length=256, null=False, default='')
    campanyName = CharField(max_length=256, null=False, default='')
    status = IntegerField(null=False, default=0)
    registerts = IntegerField()
    lastLogon = IntegerField()
    timezone = CharField(max_length=6, null=False, default='+00:00')
    timezoneId = IntegerField(null=False)
    rootdomainredirect = CharField(max_length=512, null=False, default='')
    json = TextField(null=False)
    setting = TextField(null=False)
    referralToken = CharField(max_length=128, null=False)
    deleted = IntegerField(null=False, default=0)

    class Meta:
        db_table = "User"
        index = (('idText', True), ('email', True))


class OfferSyncTask(BaseModel):
    """
    task
    """
    userId = IntegerField(null=False)
    thirdPartyANId = IntegerField()
    status = IntegerField(default=0)  # 0:新建;1:运行中;2:出错;3:完成
    executor = CharField(max_length=32, null=False)  # 执行者的唯一标识  mac地址
    message = TextField()
    createdAt = IntegerField(null=False)
    startedAt = IntegerField(null=False)
    endedAt = IntegerField(null=False)
    deleted = IntegerField(null=False, default=0)  # 0:未删除;1:已删除

    class Meta:
        db_table = "OfferSyncTask"


class ThirdPartyAffiliateNetwork(BaseModel):
    """
    affiliate login info
    """
    userId = IntegerField(null=False)
    trustedANId = IntegerField(null=False)  # TemplateAffiliateNetwork
    name = CharField(max_length=256, null=False, default='')
    token = TextField()
    userName = TextField()
    password = TextField()
    createdAt = IntegerField(null=False)
    deleted = IntegerField(null=False, default=0)

    class Meta:
        db_table = "ThirdPartyAffiliateNetwork"


class TemplateAffiliateNetwork(BaseModel):
    """
    provider
    """
    name = CharField(max_length=256, null=False)
    postbackParams = TextField(null=False)  # 回调url中参数的写法:{cid:%subid1%;p:%commission%}
    desc = TextField(null=False)  # 关于该AfflicateNetwork的描述，HTML
    apiOffer = IntegerField(null=False)  # 0:不支持api拉取Offer;1:支持拉取Offer
    apiName = CharField(max_length=256, null=False, help_text='api拉取时,区分用')
    apiUrl = TextField(null=False)
    apiParams = TextField(null=False)
    apiMode = IntegerField(null=False)  # 1:仅token;2:仅Username/password;3:token/up都支持
    apiInterval = IntegerField(null=False, default=0)  # 连续两次Task之间的最小间隔时间，0表示没有限制，单位：秒
    apiOfferAutoSuffix = CharField(max_length=256, null=False, default='')
    deleted = IntegerField(null=False, default=0)

    class Meta:
        db_table = "TemplateAffiliateNetwork"


class TemplateTrafficSource(BaseModel):
    """
    TemplateTrafficSource
    """
    id = IntegerField(null=False)
    order = IntegerField(null=False)
    name = CharField(max_length=256, null=False)

    class Meta:
        db_table = "TemplateTrafficSource"


class ThirdPartyCountryCode(BaseModel):
    """
    CountryCode
    """
    key_code = CharField()
    val_code = CharField()

    class Meta:
        db_table = "ThirdPartyCountryCode"


class ThirdPartyOffer(BaseModel):
    """
    offer
    """
    updatetime = TimeField()
    sourcename = CharField(max_length=20)
    userId = IntegerField(null=False)
    taskId = IntegerField(null=False)
    status = IntegerField(null=False)
    offerId = TextField()
    name = CharField(max_length=256, null=False, default='')
    previewLink = TextField()
    trackingLink = TextField()
    countryCode = TextField()
    payoutMode = IntegerField(null=False, default=1)
    payoutValue = CharField(null=False, default='0.00000')
    category = TextField()
    carrier = TextField()
    platform = TextField()
    detail = TextField()

    class Meta:
        db_table = "ThirdPartyOffer"


class Country(BaseModel):
    name = CharField(max_length=256, null=False)
    alpha2Code = CharField(max_length=2, null=False)
    alpha3Code = CharField(max_length=3, null=False)
    numCode = IntegerField(null=False)

    class Meta:
        db_table = "Country"
        index = (('alpha2Code', True), ('alpha3Code', True), ('numCode', True))


class Flow(BaseModel):
    name = CharField(max_length=256, null=False)

    class Meta:
        db_table = "Flow"
        index = ('id', True)


class Lander(BaseModel):
    name = CharField(max_length=256, null=False)

    class Meta:
        db_table = "Lander"
        index = ('id', True)


class Offer(BaseModel):
    name = CharField(max_length=256, null=False)
    payoutMode = IntegerField(null=False)
    payoutValue = FloatField(null=False)

    class Meta:
        db_table = "Offer"
        index = ('id', True)


class TrackingCampaign(BaseModel):
    id = IntegerField(null=False)
    status = IntegerField(null=False)
    name = CharField(max_length=256, null=False)
    remark = CharField(max_length=1000, null=False)
    TheirCampName = CharField(max_length=1000, null=False)

    class Meta:
        db_table = "TrackingCampaign"
        index = ('id', True)


class TrafficSource(BaseModel):
    id = IntegerField(null=False)
    userid = IntegerField(null=False)
    name = CharField(max_length=256, null=False)
    trafficTemplateId = IntegerField(default=0, null=False)
    token = CharField(max_length=128)
    account = CharField(max_length=128)
    password = CharField(max_length=128)
    integrations = IntegerField(null=False)

    class Meta:
        db_table = "TrafficSource"
        index = ('id', True)


class AffiliateNetwork(BaseModel):
    name = CharField(max_length=256, null=False)

    class Meta:
        db_table = "AffiliateNetwork"
        index = ('id', True)


class AdConversionsStatis(BaseModel):
    UserID = CharField(max_length=256, null=True, default='')
    PostbackTimestamp = CharField(max_length=256, null=True, default='')
    VisitTimestamp = CharField(max_length=256, null=True, default='')
    ExternalID = CharField(max_length=256, null=True, default='')
    ClickID = CharField(max_length=256, null=True, default='')
    TransactionID = CharField(max_length=256, null=True, default='')
    Revenue = CharField(max_length=256, null=True, default='0.0')
    Cost = CharField(max_length=256, null=True, default='0.0')
    CampaignName = CharField(max_length=256, null=True, default='')
    CampaignID = CharField(max_length=256, null=True, default='')
    LanderName = CharField(max_length=256, null=True, default='')
    LanderID = CharField(max_length=256, null=True, default='')
    OfferName = CharField(max_length=256, null=True, default='')
    OfferID = CharField(max_length=256, null=True, default='')
    Country = CharField(max_length=256, null=True, default='')
    CountryCode = CharField(max_length=256, null=True, default='')
    TrafficSourceName = CharField(max_length=256, null=True, default='')
    TrafficSourceID = CharField(max_length=256, null=True, default='')
    AffiliateNetworkName = CharField(max_length=256, null=True, default='')
    AffiliateNetworkID = CharField(max_length=256, null=True, default='')
    Device = CharField(max_length=256, null=True, default='')
    OS = CharField(max_length=256, null=True, default='')
    OSVersion = CharField(max_length=256, null=True, default='')
    Brand = CharField(max_length=256, null=True, default='')
    Model = CharField(max_length=256, null=True, default='')
    Browser = CharField(max_length=256, null=True, default='')
    BrowserVersion = CharField(max_length=256, null=True, default='')
    ISP = CharField(max_length=256, null=True, default='')
    MobileCarrier = CharField(max_length=256, null=True, default='')
    ConnectionType = CharField(max_length=256, null=True, default='')
    VisitorIP = CharField(max_length=256, null=True, default='')
    VisitorReferrer = CharField(max_length=256, null=True, default='')
    V1 = CharField(max_length=256, null=True, default='')
    V2 = CharField(max_length=256, null=True, default='')
    V3 = CharField(max_length=256, null=True, default='')
    V4 = CharField(max_length=256, null=True, default='')
    V5 = CharField(max_length=256, null=True, default='')
    V6 = CharField(max_length=256, null=True, default='')
    V7 = CharField(max_length=256, null=True, default='')
    V8 = CharField(max_length=256, null=True, default='')
    V9 = CharField(max_length=256, null=True, default='')
    V10 = CharField(max_length=256, null=True, default='')

    class Meta:
        db_table = "AdConversionsStatis"
        index = (('ClickID', True))


class AdStatisLog(BaseModel):
    UserID = CharField(null=False, default=0)
    CampaignID = CharField(null=False, default=0)
    CampaignName = CharField(max_length=256, null=True, default='')
    FlowID = CharField(null=True, default=0)
    FlowName = CharField(max_length=256, null=True, default='')
    LanderID = CharField(null=True, default=0)
    LanderName = CharField(max_length=256, null=True, default='')
    OfferID = CharField(null=True, default=0)
    OfferName = CharField(max_length=256, null=True, default='')
    OfferUrl = CharField(max_length=256, null=True, default='')
    OfferCountry = CharField(max_length=256, null=True, default='')
    AffiliateNetworkID = CharField(null=True, default=0)
    AffilliateNetworkName = CharField(max_length=256, null=True, default='')
    TrafficSourceID = CharField(null=True, default=0)
    TrafficSourceName = CharField(max_length=256, null=True, default='')
    Language = CharField(max_length=256, null=True, default='')
    Model = CharField(max_length=256, null=True, default='')
    Country = CharField(max_length=256, null=True, default='')
    City = CharField(max_length=256, null=True, default='')
    Region = CharField(max_length=256, null=True, default='')
    ISP = CharField(max_length=256, null=True, default='')
    MobileCarrier = CharField(max_length=256, null=True, default='')
    Domain = CharField(max_length=256, null=True, default='')
    DeviceType = CharField(max_length=256, null=True, default='')
    Brand = CharField(max_length=256, null=True, default='')
    OS = CharField(max_length=256, null=True, default='')
    OSVersion = CharField(max_length=256, null=True, default='')
    Browser = CharField(max_length=256, null=True, default='')
    BrowserVersion = CharField(max_length=256, null=True, default='')
    ConnectionType = CharField(max_length=256, null=True, default='')
    Timestamp = CharField(null=True, default=0)
    Visits = CharField(null=True, default=0)
    Clicks = CharField(null=True, default=0)
    Conversions = CharField(null=True, default=0)
    Cost = CharField(null=True, default=0)
    Revenue = CharField(null=True, default=0)
    Impressions = CharField(null=True, default=0)
    KeysMD5 = CharField(max_length=256, null=True, default='')
    Ip = CharField(max_length=256, null=True, default='')
    V1 = CharField(max_length=256, null=True, default='')
    V2 = CharField(max_length=256, null=True, default='')
    V3 = CharField(max_length=256, null=True, default='')
    V4 = CharField(max_length=256, null=True, default='')
    V5 = CharField(max_length=256, null=True, default='')
    V6 = CharField(max_length=256, null=True, default='')
    V7 = CharField(max_length=256, null=True, default='')
    V8 = CharField(max_length=256, null=True, default='')
    V9 = CharField(max_length=256, null=True, default='')
    V10 = CharField(max_length=256, null=True, default='')
    tsCampaignId = CharField(max_length=256, null=True, default='')
    tsWebsiteId = CharField(max_length=256, null=True, default='')

    class Meta:
        db_table = "AdStatis"
        index = (('KeysMD5', True))


class AdCost(BaseModel):
    id = CharField(null=False)
    CampaignID = CharField(max_length=50, null=True)
    userid = IntegerField(null=False)
    WebsiteId = CharField(max_length=50, null=False, default='')
    WebsiteChildId = CharField(max_length=50, null=False, default='')
    Cost = CharField(max_length=50, null=False, default='')
    Createtime = BigIntegerField()
    Status = IntegerField(null=False)
    # State = IntegerField(null=False, default=0)
    type = IntegerField(null=False)
    State = CharField(null=False)
    begintime = BigIntegerField()
    endtime = BigIntegerField()
    updatecost = IntegerField(default=0)
    TrafficsourceId = CharField(max_length=100)
    remark = CharField(max_length=255)
    updatebid = IntegerField(default=0)
    bid = FloatField(null=True)

    class Meta:
        db_table = "AdCost"


class WebsiteId(BaseModel):
    id = IntegerField(null=False)
    userId = IntegerField(null=False)
    status = IntegerField(null=False)
    web_site_id = CharField(max_length=256)
    state = IntegerField(null=False)
    remark = CharField(max_length=256)
    campaignId = IntegerField(null=False)
    TrafficSourceId = IntegerField(null=False)

    class Meta:
        db_table = "WebSiteId"


class UserBilling(BaseModel):
    totalEvents = IntegerField(null=False)
    billedEvents = IntegerField(null=False)
    userId = IntegerField(null=False)
    expired = IntegerField(null=False)

    class Meta:
        db_table = "UserBilling"


db.connect()

# a = Country.update(name='ccc').where(Country.id == 1).execute()
# pass
