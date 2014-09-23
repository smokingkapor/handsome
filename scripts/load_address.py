# -*- coding: utf-8 -*-
import os
import sys


# set up django env
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'handsome.settings')


from orders.models import Province, City, Country


if __name__ == '__main__':
    # load provinces
    with open('province.txt') as f:
        for line in f.readlines():
            fake, pk, name = line.strip().split(',')
            province, created = Province.objects.get_or_create(id=pk)
            province.name = name.decode('utf-8')
            province.save()

    # load cities
    with open('city.txt') as f:
        for line in f.readlines():
            fake, pk, name, province_pk = line.strip().split(',')
            province = Province.objects.get(id=province_pk)
            city, created = City.objects.get_or_create(id=pk, province=province)
            city.name = name.decode('utf-8')
            city.save()

    # load country
    with open('area.txt') as f:
        for line in f.readlines():
            fake, pk, name, city_pk = line.strip().split(',')
            city = City.objects.get(id=city_pk)
            country, created = Country.objects.get_or_create(id=pk, city=city)
            country.name = name.decode('utf-8')
            country.save()
