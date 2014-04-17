# -*- coding: utf-8 -*-
import json
import urllib
import urllib2


PROVINCES = {"1": "北京", "2": "上海", "3": "天津", "4": "重庆", "5": "河北",
             "6": "山西", "7": "河南", "8": "辽宁", "9": "吉林", "10": "黑龙江",
             "11": "内蒙古", "12": "江苏", "13": "山东", "14": "安徽", "15": "浙江",
             "16": "福建", "17": "湖北", "18": "湖南", "19": "广东", "20": "广西",
             "21": "江西", "22": "四川", "23": "海南", "24": "贵州", "25": "云南",
             "26": "西藏", "27": "陕西", "28": "甘肃", "29": "青海", "30": "宁夏",
             "31": "新疆", "32": "台湾", "42": "香港", "43": "澳门", "84": "钓鱼岛"}

def get_cities(province_id):
    content = urllib2.urlopen(
        'http://easybuy.jd.com//address/getCitys.action',
        urllib.urlencode({'provinceId': province_id})).read()
    cities = {}
    for city_id, city_name in json.loads(content).iteritems():
        cities[city_id] = city_name

    return cities

def get_countries(city_id):
    content = urllib2.urlopen('http://easybuy.jd.com//address/getCountys.action',
                              urllib.urlencode({'cityId': city_id})).read()
    countries = {}
    for country_id, country_name in json.loads(content).iteritems():
        countries[country_id] = country_name

    return countries

def get_towns(country_id):
    content = urllib2.urlopen('http://easybuy.jd.com//address/getTowns.action',
                              urllib.urlencode({'countyId': country_id})).read()
    towns = {}
    for town_id, town_name in json.loads(content).iteritems():
        towns[town_id] = town_name

    return towns

if __name__ == 'main':
    results = {}
    for province_id, province_name in PROVINCES.iteritems():
        results[province_id] = {'name': province_name, 'children': {}}
        for city_id, city_name in get_cities(province_id):
            children = results[province_id]['children']
            children[city_id] = {'name': city_name, 'children': {}}
            for country_id, country_name in get_countries(city_id):
                children = results[country_id]['children']
                children[country_id] = {'name': country_name, 'children': {}}
                for town_id, town_name in get_towns(country_id):
                    children = results[town_id]['children']
                    children[town_id] = {'name': town_name}

    print json.dumps(results, indent=4)
