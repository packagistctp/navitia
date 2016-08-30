# coding=utf-8

# Copyright (c) 2001-2014, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io
from __future__ import absolute_import, print_function, unicode_literals, division
from importlib import import_module
import logging


class StreetNetwork(object):
    @staticmethod
    def get_street_network(instance, street_network_configuration):
        log = logging.getLogger(__name__)
        try:
            cls = street_network_configuration['class']
        except KeyError, TypeError:
            log.warn('impossible to build a routing, missing mandatory field in configuration')

        routing_name = street_network_configuration.get('name', 'Routing_name')
        args = street_network_configuration.get('args', {})

        try:
            if '.' not in cls:
                log.warn('impossible to build routing {}, wrongly formated class: {}'.format(routing_name, cls))

            module_path, name = cls.rsplit('.', 1)
            module = import_module(module_path)
            attr = getattr(module, name)
            log.info('{} service used for direct_path'.format(name))
        except ImportError:
            log.warn('impossible to build routing {}, cannot find class: {}'.format(routing_name, cls))

        try:
            service_args = args.get('service_args', None)
            if service_args:
                directions_options = service_args.get('directions_options', None)
            else:
                directions_options = None

            street_network = attr(instance=instance,
                                  service_url=args.get('service_url', None),
                                  directions_options=directions_options,
                                  costing_options=args.get('costing_options', None),
                                  api_key=args.get('api_key', None))
        except TypeError as e:
            log.warn('impossible to build routing proxy {}, wrong arguments: {}'.format(routing_name, e.message))
        return street_network
