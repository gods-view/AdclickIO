#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: helper.py
@time: 2017/3/29 下午6:08
"""

import uuid, time
import re
import copy
from datetime import datetime, timedelta


country_map = {'ZZ': 'ZZZ', 'AE': 'ARE', 'AF': 'AFG', 'AG': 'ATG', 'AI': 'AIA', 'AL': 'ALB', 'AM': 'ARM', 'AO': 'AGO',
               'AQ': 'ATA', 'AR': 'ARG', 'AS': 'ASM', 'AT': 'AUT', 'AU': 'AUS', 'AW': 'ABW', 'AX': 'ALA', 'AZ': 'AZE',
               'BA': 'BIH', 'BB': 'BRB', 'BD': 'BGD', 'BE': 'BEL', 'BF': 'BFA', 'BG': 'BGR', 'BH': 'BHR', 'BI': 'BDI',
               'BJ': 'BEN', 'BL': 'BLM', 'BM': 'BMU', 'BN': 'BRN', 'BO': 'BOL', 'BQ': 'BES', 'BR': 'BRA', 'BS': 'BHS',
               'BT': 'BTN', 'BV': 'BVT', 'BW': 'BWA', 'BY': 'BLR', 'BZ': 'BLZ', 'CA': 'CAN', 'CC': 'CCK', 'CD': 'COD',
               'CF': 'CAF', 'CG': 'COG', 'CH': 'CHE', 'CI': 'CIV', 'CK': 'COK', 'CL': 'CHL', 'CM': 'CMR', 'CN': 'CHN',
               'CO': 'COL', 'CR': 'CRI', 'CU': 'CUB', 'CV': 'CPV', 'CW': 'CUW', 'CX': 'CXR', 'CY': 'CYP', 'CZ': 'CZE',
               'DE': 'DEU', 'DJ': 'DJI', 'DK': 'DNK', 'DM': 'DMA', 'DO': 'DOM', 'DZ': 'DZA', 'EC': 'ECU', 'EE': 'EST',
               'EG': 'EGY', 'EH': 'ESH', 'ER': 'ERI', 'ES': 'ESP', 'ET': 'ETH', 'FI': 'FIN', 'FJ': 'FJI', 'FK': 'FLK',
               'FM': 'FSM', 'FO': 'FRO', 'FR': 'FRA', 'GA': 'GAB', 'GB': 'GBR', 'GD': 'GRD', 'GE': 'GEO', 'GF': 'GUF',
               'GG': 'GGY', 'GH': 'GHA', 'GI': 'GIB', 'GL': 'GRL', 'GM': 'GMB', 'GN': 'GIN', 'GP': 'GLP', 'GQ': 'GNQ',
               'GR': 'GRC', 'GS': 'SGS', 'GT': 'GTM', 'GU': 'GUM', 'GW': 'GNB', 'GY': 'GUY', 'HK': 'HKG', 'HM': 'HMD',
               'HN': 'HND', 'HR': 'HRV', 'HT': 'HTI', 'HU': 'HUN', 'ID': 'IDN', 'IE': 'IRL', 'IL': 'ISR', 'IM': 'IMN',
               'IN': 'IND', 'IO': 'IOT', 'IQ': 'IRQ', 'IR': 'IRN', 'IS': 'ISL', 'IT': 'ITA', 'JE': 'JEY', 'JM': 'JAM',
               'JO': 'JOR', 'JP': 'JPN', 'KE': 'KEN', 'KG': 'KGZ', 'KH': 'KHM', 'KI': 'KIR', 'KM': 'COM', 'KN': 'KNA',
               'KP': 'PRK', 'KR': 'KOR', 'KW': 'KWT', 'KY': 'CYM', 'KZ': 'KAZ', 'LA': 'LAO', 'LB': 'LBN', 'LC': 'LCA',
               'LI': 'LIE', 'LK': 'LKA', 'LR': 'LBR', 'LS': 'LSO', 'LT': 'LTU', 'LU': 'LUX', 'LV': 'LVA', 'LY': 'LBY',
               'MA': 'MAR', 'MC': 'MCO', 'MD': 'MDA', 'ME': 'MNE', 'MF': 'MAF', 'MG': 'MDG', 'MH': 'MHL', 'MK': 'MKD',
               'ML': 'MLI', 'MM': 'MMR', 'MN': 'MNG', 'MO': 'MAC', 'MP': 'MNP', 'MQ': 'MTQ', 'MR': 'MRT', 'MS': 'MSR',
               'MT': 'MLT', 'MU': 'MUS', 'MV': 'MDV', 'MW': 'MWI', 'MX': 'MEX', 'MY': 'MYS', 'MZ': 'MOZ', 'NA': 'NAM',
               'NC': 'NCL', 'NE': 'NER', 'NF': 'NFK', 'NG': 'NGA', 'NI': 'NIC', 'NL': 'NLD', 'NO': 'NOR', 'NP': 'NPL',
               'NR': 'NRU', 'NU': 'NIU', 'NZ': 'NZL', 'OM': 'OMN', 'PA': 'PAN', 'PE': 'PER', 'PF': 'PYF', 'PG': 'PNG',
               'PH': 'PHL', 'PK': 'PAK', 'PL': 'POL', 'PM': 'SPM', 'PN': 'PCN', 'PR': 'PRI', 'PS': 'PSE', 'PT': 'PRT',
               'PW': 'PLW', 'PY': 'PRY', 'QA': 'QAT', 'RE': 'REU', 'RO': 'ROU', 'RS': 'SRB', 'RU': 'RUS', 'RW': 'RWA',
               'SA': 'SAU', 'SB': 'SLB', 'SC': 'SYC', 'SD': 'SDN', 'SE': 'SWE', 'SG': 'SGP', 'SH': 'SHN', 'SI': 'SVN',
               'SJ': 'SJM', 'SK': 'SVK', 'SL': 'SLE', 'SM': 'SMR', 'SN': 'SEN', 'SO': 'SOM', 'SR': 'SUR', 'SS': 'SSD',
               'ST': 'STP', 'SV': 'SLV', 'SX': 'SXM', 'SY': 'SYR', 'SZ': 'SWZ', 'TC': 'TCA', 'TD': 'TCD', 'TF': 'ATF',
               'TG': 'TGO', 'TH': 'THA', 'TJ': 'TJK', 'TK': 'TKL', 'TL': 'TLS', 'TM': 'TKM', 'TN': 'TUN', 'TO': 'TON',
               'TR': 'TUR', 'TT': 'TTO', 'TV': 'TUV', 'TW': 'TWN', 'TZ': 'TZA', 'UA': 'UKR', 'UG': 'UGA', 'UM': 'UMI',
               'US': 'USA', 'UY': 'URY', 'UZ': 'UZB', 'VA': 'VAT', 'VC': 'VCT', 'VE': 'VEN', 'VG': 'VGB', 'VI': 'VIR',
               'VN': 'VNM', 'VU': 'VUT', 'WF': 'WLF', 'WS': 'WSM', 'YE': 'YEM', 'YT': 'MYT', 'ZA': 'ZAF', 'ZM': 'ZMB',
               'ZW': 'ZWE', 'AD': 'ADR', 'IN_Karnataka': 'KNT', 'IN_Kerala': 'KLL', 'IN_West Bengal': 'XMJ',
               'IN_Gujarat': 'GJT', 'IN_Punjab': 'PZP', 'IN_Maharashtra': 'MHL', 'IN_Andhra Pradesh': 'ADL',
               'IN_Tamil Nadu': 'MDL', 'PT_Portalegre': 'BTL', 'OTH': 'OTH',
               'global': 'ADR,WLF,JPN,JAM,JOR,WSM,JEY,GNB,GUM,GTM,SGS,GRC,GNQ,GLP,GUY,GGY,GUF,GEO,GRD,GBR,GAB,GIN,GMB,GRL,GIB,GHA,PRI,PSE,PLW,PRT,PRY,PAN,PYF,PNG,PER,PAK,PHL,PCN,POL,SPM,ZMB,ZAF,ZZZ,ZWE,MNE,MDA,MDG,MAF,MAR,MCO,MMR,MLI,MAC,MNG,MHL,MKD,MUS,MLT,MWI,MDV,MTQ,MNP,MSR,MRT,MYS,MEX,MOZ,FRA,FIN,FJI,FLK,FSM,FRO,COK,CIV,CHE,COL,CHN,CMR,CHL,CCK,CAN,COG,CAF,COD,CZE,CYP,CXR,CRI,CUW,CPV,CUB,SWZ,SYR,SXM,SSD,SUR,SLV,STP,SVK,SJM,SVN,SHN,SOM,SEN,SMR,SLE,SYC,SLB,SAU,SGP,SWE,SDN,YEM,MYT,LBN,LCA,LAO,LKA,LIE,LVA,LTU,LUX,LBR,LSO,LBY,VAT,VCT,VEN,VGB,IRQ,VIR,ISL,IRN,ITA,VNM,IMN,ISR,IOT,IND,IRL,IDN,BGD,BEL,BFA,BGR,BIH,BRB,BLM,BMU,BRN,BOL,BHR,BDI,BEN,BTN,BVT,BWA,BES,BRA,BHS,BLR,BLZ,RUS,RWA,SRB,REU,ROU,OMN,HRV,HTI,HUN,HKG,HND,HMD,ESH,EST,EGY,ECU,ETH,ESP,ERI,URY,UZB,USA,UMI,UGA,UKR,VUT,NIC,NLD,NOR,NAM,NCL,NER,NFK,NGA,NZL,NPL,NRU,NIU,KGZ,KEN,KIR,KHM,KNA,COM,KOR,PRK,KWT,KAZ,CYM,DOM,DMA,DJI,DNK,DEU,DZA,TZA,TUV,TWN,TTO,TUR,TUN,TON,TLS,TKM,TJK,TKL,THA,ATF,TGO,TCD,TCA,ARE,ATG,AFG,AIA,ARM,ALB,AGO,ATA,ASM,ARG,AUS,AUT,ABW,ALA,AZE,QAT',
               "Andorra": "AND", "United Arab Emirates": "ARE", "Afghanistan": "AFG",
               "Antigua and Barbuda": "ATG",
               "Anguilla": "AIA", "Albania": "ALB", "Armenia": "ARM", "Netherlands Antilles": "ANT", "Angola": "AGO",
               "Antarctica": "ATA", "Argentina": "ARG", "American Samoa": "ASM", "Austria": "AUT", "Australia": "AUS",
               "Aruba": "ABW",
               "Aland Islands": "ALA", "Azerbaijan": "AZE", "Bosnia and Herzegovina": "BIH", "Barbados": "BRB",
               "Bangladesh": "BGD",
               "Belgium": "BEL", "Burkina Faso": "BFA", "Bulgaria": "BGR", "Bahrain": "BHR", "Burundi": "BDI",
               "Benin": "BEN",
               "Saint-Barth\u00e9lemy": "BLM", "Bermuda": "BMU", "Brunei Darussalam": "BRN", "Bolivia": "BOL",
               "Bonaire, Sint Eustatius and Saba": "BES", "Brazil": "BRA", "Bahamas": "BHS", "Bhutan": "BTN",
               "Bouvet Island": "BVT",
               "Botswana": "BWA", "Belarus": "BLR", "Belize": "BLZ", "Canada": "CAN", "Cocos (Keeling) Islands": "CCK",
               "Congo, (Kinshasa)": "COD", "Central African Republic": "CAF", "Congo (Brazzaville)": "COG",
               "Switzerland": "CHE",
               "C\u00f4te d'Ivoire": "CIV", "Cook Islands": "COK", "Chile": "CHL", "Cameroon": "CMR", "China": "CHN",
               "Colombia": "COL", "Costa Rica": "CRI", "Cuba": "CUB", "Cape Verde": "CPV", "Curacao": "CUW",
               "Christmas Island": "CXR", "Cyprus": "CYP", "Czech Republic": "CZE", "Germany": "DEU", "Djibouti": "DJI",
               "Denmark": "DNK", "Dominica": "DMA", "Dominican Republic": "DOM", "Algeria": "DZA", "Ecuador": "ECU",
               "Estonia": "EST",
               "Egypt": "EGY", "Western Sahara": "ESH", "Eritrea": "ERI", "Spain": "ESP", "Ethiopia": "ETH",
               "Finland": "FIN",
               "Fiji": "FJI", "Falkland Islands (Malvinas)": "FLK", "Micronesia, Federated States of": "FSM",
               "Faroe Islands": "FRO",
               "France": "FRA", "Gabon": "GAB", "United Kingdom": "GBR", "Grenada": "GRD", "Georgia": "GEO",
               "French Guiana": "GUF",
               "Guernsey": "GGY", "Ghana": "GHA", "Gibraltar": "GIB", "Greenland": "GRL", "Gambia": "GMB",
               "Guinea": "GIN",
               "Guadeloupe": "GLP", "Equatorial Guinea": "GNQ", "Greece": "GRC",
               "South Georgia and the South Sandwich Islands": "SGS", "Guatemala": "GTM", "Guam": "GUM",
               "Guinea-Bissau": "GNB",
               "Guyana": "GUY", "Hong Kong, SAR China": "HKG", "Heard and Mcdonald Islands": "HMD", "Honduras": "HND",
               "Croatia": "HRV", "Haiti": "HTI", "Hungary": "HUN", "Indonesia": "IDN", "Ireland": "IRL",
               "Israel": "ISR",
               "Isle of Man": "IMN", "India": "IND", "British Indian Ocean Territory": "IOT", "Iraq": "IRQ",
               "Iran, Islamic Republic of": "IRN", "Iceland": "ISL", "Italy": "ITA", "Jersey": "JEY", "Jamaica": "JAM",
               "Jordan": "JOR", "Japan": "JPN", "Kenya": "KEN", "Kyrgyzstan": "KGZ", "Cambodia": "KHM",
               "Kiribati": "KIR",
               "Comoros": "COM", "Saint Kitts and Nevis": "KNA", "Korea (North)": "PRK", "Korea (South)": "KOR",
               "Kuwait": "KWT",
               "Cayman Islands": "CYM", "Kazakhstan": "KAZ", "Lao PDR": "LAO", "Lebanon": "LBN", "Saint Lucia": "LCA",
               "Liechtenstein": "LIE", "Sri Lanka": "LKA", "Liberia": "LBR", "Lesotho": "LSO", "Lithuania": "LTU",
               "Luxembourg": "LUX", "Latvia": "LVA", "Libya": "LBY", "Morocco": "MAR", "Monaco": "MCO",
               "Moldova": "MDA",
               "Montenegro": "MNE", "Saint-Martin (French part)": "MAF", "Madagascar": "MDG", "Marshall Islands": "MHL",
               "Macedonia, Republic of": "MKD", "Mali": "MLI", "Myanmar": "MMR", "Mongolia": "MNG",
               "Macao, SAR China": "MAC",
               "Northern Mariana Islands": "MNP", "Martinique": "MTQ", "Mauritania": "MRT", "Montserrat": "MSR",
               "Malta": "MLT",
               "Mauritius": "MUS", "Maldives": "MDV", "Malawi": "MWI", "Mexico": "MEX", "Malaysia": "MYS",
               "Mozambique": "MOZ",
               "Namibia": "NAM", "New Caledonia": "NCL", "Niger": "NER", "Norfolk Island": "NFK", "Nigeria": "NGA",
               "Nicaragua": "NIC", "Netherlands": "NLD", "Norway": "NOR", "Nepal": "NPL", "Nauru": "NRU", "Niue": "NIU",
               "New Zealand": "NZL", "Oman": "OMN", "Panama": "PAN", "Peru": "PER", "French Polynesia": "PYF",
               "Papua New Guinea": "PNG", "Philippines": "PHL", "Pakistan": "PAK", "Poland": "POL",
               "Saint Pierre and Miquelon": "SPM", "Pitcairn": "PCN", "Puerto Rico": "PRI",
               "Palestinian Territory": "PSE",
               "Portugal": "PRT", "Palau": "PLW", "Paraguay": "PRY", "Qatar": "QAT", "R\u00e9union": "REU",
               "Romania": "ROU",
               "Serbia": "SRB", "Russian Federation": "RUS", "Rwanda": "RWA", "Saudi Arabia": "SAU",
               "Solomon Islands": "SLB",
               "Seychelles": "SYC", "Sudan": "SDN", "Sweden": "SWE", "Singapore": "SGP", "Saint Helena": "SHN",
               "Slovenia": "SVN",
               "Svalbard and Jan Mayen Islands": "SJM", "Slovakia": "SVK", "Sierra Leone": "SLE", "San Marino": "SMR",
               "Senegal": "SEN", "Somalia": "SOM", "Suriname": "SUR", "South Sudan": "SSD",
               "Sao Tome and Principe": "STP",
               "El Salvador": "SLV", "Sint Maarten (Dutch Part)": "SXM", "Syrian Arab Republic (Syria)": "SYR",
               "Swaziland": "SWZ",
               "Turks and Caicos Islands": "TCA", "Chad": "TCD", "French Southern Territories": "ATF", "Togo": "TGO",
               "Thailand": "THA", "Tajikistan": "TJK", "Tokelau": "TKL", "Timor-Leste": "TLS", "Turkmenistan": "TKM",
               "Tunisia": "TUN", "Tonga": "TON", "Turkey": "TUR", "Trinidad and Tobago": "TTO", "Tuvalu": "TUV",
               "Taiwan, Republic of China": "TWN", "Tanzania, United Republic of": "TZA", "Ukraine": "UKR",
               "Uganda": "UGA",
               "US Minor Outlying Islands": "UMI", "United States of America": "USA", "Uruguay": "URY",
               "Uzbekistan": "UZB",
               "Holy See (Vatican City State)": "VAT", "Saint Vincent and Grenadines": "VCT",
               "Venezuela (Bolivarian Republic)": "VEN", "British Virgin Islands": "VGB", "Virgin Islands, US": "VIR",
               "Viet Nam": "VNM", "Vanuatu": "VUT", "Wallis and Futuna Islands": "WLF", "Samoa": "WSM", "Yemen": "YEM",
               "Mayotte": "MYT", "South Africa": "ZAF", "Zambia": "ZMB", "Zimbabwe": "ZWE",
               "Serbia and Montenegro": "SCG",
               "United States": "USA",
               "Taiwan": "TWN",
               'Congo, The Democratic Republic of the': "COD",
               "Congo": "COD",
               "Cote D'Ivoire": "CIV",
               "France, Metropolitan": "FRA",
               "Hong Kong": "HKG",
               "Heard Island and McDonald Islands": "HMD",
               "Korea, Democratic People's Republic of": "PRK",
               "Korea, Republic of": "KOR",
               "Lao People's Democratic Republic": "LAO",
               "Libyan Arab Jamahiriya": "LBY",
               "Moldova, Republic of": "MDA",
               "Macedonia": "MKD",
               "Macau": "MAC",
               "Pitcairn Islands": "PCN",
               "Reunion": "REU",
               "Svalbard and Jan Mayen": "SJM",
               "Syrian Arab Republic": "SYR",
               "Saint Vincent and the Grenadines": "VCT",
               "Venezuela": "VEN",
               "Virgin Islands, British": "VGB",
               "Virgin Islands, U.S.": "VIR",
               "Wallis and Futuna": "WLF",
               "Bonaire, Saint Eustatius and Saba": "BES",
               "Vietnam": "VNM",
               "UK": "GBR"
               }
region_map = {
    'EU': ['AUT', 'BEL', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'IRL', 'ITA',
           'LVA',
           'LTU', 'LUX', 'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK', 'SVN', 'ESP', 'SWE', 'GBR'],
    'AP': ['CHN', 'HKG', 'MAC', 'PRK', 'JPN', 'MNG', 'KOR', 'BRN', 'KHM', 'IDN', 'LAO', 'MYS', 'MMR', 'PHL', 'SGP',
           'THA',
           'TLS', 'VNM', 'AFG', 'BGD', 'BTN', 'IND', 'IRN', 'MDV', 'NPL', 'PAK', 'LKA', 'AUS', 'CXR', 'CCK', 'HMD',
           'NZL',
           'NFK', 'FJI', 'NCL', 'PNG', 'SLB', 'VUT', 'GUM', 'KIR', 'MHL', 'FSM', 'NRU', 'MNP', 'PLW', 'UMI', 'ASM',
           'COK',
           'PYF', 'NIU', 'PCN', 'WSM', 'TKL', 'TON', 'TUV', 'WLF']}


class Helper:
    def __init__(self):
        pass

    # @classmethod
    # def fix_country(cls, country):
    #     country_tmp_map = copy.deepcopy(country_map)
    #     # print "country_map",country_map['IN']
    #     if isinstance(country, list):
    #         print ('success')
    #         print (country)
    #         # country_list = map(lambda x: country_tmp_map[x], country)
    #         # print (country_list)
    #         for i, country_item in enumerate(country):
    #             if country_item not in country_tmp_map:
    #                 print (country_item)
    #                 country[i] = 'OTH'
    #         return ','.join(map(lambda x: country_tmp_map[x], country))
    #     elif isinstance(country, str):
    #         if country not in country_tmp_map:
    #             print (country)
    #             country = 'OTH'
    #         print ("success")
    #         # print (type(country), country)
    #         print (country_tmp_map[country])
    #         return country_tmp_map[country]
    #     else:
    #         print ('this type not support==============' + country)
    #         raise Exception('this type not support' + str(country))
    @classmethod
    def fix_country(cls, country):
        if isinstance(country, list):
            _country = []
            [_country.extend(region_map[x]) if x in region_map else _country.append(country_map[x]) for x in country]
            return ','.join(list(set(_country)))
        elif isinstance(country, str):
            if country.find('|') != -1:
                country = country.split('|')
                return Helper.fix_country(country)
            elif country.find(',') != -1:
                country = country.split(',')
                return Helper.fix_country(country)
            return country_map.get(country)
        else:
            raise Exception('this type not support')

    @classmethod
    def fix_country_str(cls, country):
        if country not in country_map:
            return "OTH"
        return country_map[country]

    @classmethod
    def get_mac_address(cls):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    @classmethod
    def make_timestamp_from_str(cls, str_t):
        """
        字符串转时间戳
        :param str_t: 字符串时间
        :return: timestamp
        """
        pattern = re.compile(r'^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$')
        p = pattern.search(str_t)
        if p:
            return time.mktime(time.strptime(str_t, '%Y-%m-%d %H:%M:%S'))
        pattern = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
        p = pattern.search(str_t)
        if p:
            return time.mktime(time.strptime(str_t, '%Y-%m-%d'))
        raise Exception('make_timestamp_from_str error')

    @classmethod
    def fix_tracklink_url(cls, url, more_param):
        import urllib.parse
        a = urllib.parse.urlparse(url)
        params = more_param if not a.query else a.query + '&%s' % more_param
        netloc = a.netloc if a.path else a.netloc + '/'
        return urllib.parse.urlunparse((a.scheme, netloc, a.path, '', params, ''))

    @classmethod
    def get_between_days(cls, start, end, style):
        date_list = []
        while start <= end:
            date_str = start.strftime(style)
            date_list.append(date_str)
            start += timedelta(days=1)
        return date_list

