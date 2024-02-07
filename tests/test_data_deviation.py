# test_data_deviation.py
# Test database dictionaries for allocation deviation tests
# 2024-01-30
# @juicemcpeso

allocation_expected = {0: [{'asset_class_id': 1,
                            'location_id': 2,
                            'current_value': 140000000,
                            'plan_percent': 2000,
                            'plan_value': 200000000,
                            'deviation': -3000},
                           {'asset_class_id': 2,
                            'location_id': 2,
                            'current_value': 40000000,
                            'plan_percent': 500,
                            'plan_value': 50000000,
                            'deviation': -2000},
                           {'asset_class_id': 1,
                            'location_id': 1,
                            'current_value': 340000000,
                            'plan_percent': 4000,
                            'plan_value': 400000000,
                            'deviation': -1500},
                           {'asset_class_id': 2,
                            'location_id': 1,
                            'current_value': 340000000,
                            'plan_percent': 2500,
                            'plan_value': 250000000,
                            'deviation': 3600},
                           {'asset_class_id': 3,
                            'location_id': 1,
                            'current_value': 140000000,
                            'plan_percent': 1000,
                            'plan_value': 100000000,
                            'deviation': 4000}]}

allocation_deviation_with_next_level_expected = [{'asset_class_id': 1,
                                                  'location_id': 2,
                                                  'current_value': 140000000,
                                                  'plan_percent': 2000,
                                                  'plan_value': 200000000,
                                                  'deviation': -3000,
                                                  'next_deviation': -2000},
                                                 {'asset_class_id': 1,
                                                  'location_id': 2,
                                                  'current_value': 140000000,
                                                  'plan_percent': 2000,
                                                  'plan_value': 200000000,
                                                  'deviation': -3000,
                                                  'next_deviation': -1500},
                                                 {'asset_class_id': 1,
                                                  'location_id': 2,
                                                  'current_value': 140000000,
                                                  'plan_percent': 2000,
                                                  'plan_value': 200000000,
                                                  'deviation': -3000,
                                                  'next_deviation': 3600},
                                                 {'asset_class_id': 1,
                                                  'location_id': 2,
                                                  'current_value': 140000000,
                                                  'plan_percent': 2000,
                                                  'plan_value': 200000000,
                                                  'deviation': -3000,
                                                  'next_deviation': 4000},
                                                 {'asset_class_id': 2,
                                                  'location_id': 2,
                                                  'current_value': 40000000,
                                                  'plan_percent': 500,
                                                  'plan_value': 50000000,
                                                  'deviation': -2000,
                                                  'next_deviation': -1500},
                                                 {'asset_class_id': 2,
                                                  'location_id': 2,
                                                  'current_value': 40000000,
                                                  'plan_percent': 500,
                                                  'plan_value': 50000000,
                                                  'deviation': -2000,
                                                  'next_deviation': 3600},
                                                 {'asset_class_id': 2,
                                                  'location_id': 2,
                                                  'current_value': 40000000,
                                                  'plan_percent': 500,
                                                  'plan_value': 50000000,
                                                  'deviation': -2000,
                                                  'next_deviation': 4000},
                                                 {'asset_class_id': 1,
                                                  'location_id': 1,
                                                  'current_value': 340000000,
                                                  'plan_percent': 4000,
                                                  'plan_value': 400000000,
                                                  'deviation': -1500,
                                                  'next_deviation': 3600},
                                                 {'asset_class_id': 1,
                                                  'location_id': 1,
                                                  'current_value': 340000000,
                                                  'plan_percent': 4000,
                                                  'plan_value': 400000000,
                                                  'deviation': -1500,
                                                  'next_deviation': 4000},
                                                 {'asset_class_id': 2,
                                                  'location_id': 1,
                                                  'current_value': 340000000,
                                                  'plan_percent': 2500,
                                                  'plan_value': 250000000,
                                                  'deviation': 3600,
                                                  'next_deviation': 4000}]

sum_value_difference_at_each_level = [{'deviation': -2000, 'total_difference': 20000000},
                                      {'deviation': -1500, 'total_difference': 32500000},
                                      {'deviation': 3600, 'total_difference': 364000000},
                                      {'deviation': 4000, 'total_difference': 400000000}]

value_at_each_deviation_level_expected = [{'asset_class_id': 1,
                                           'location_id': 2,
                                           'current_value': 140000000,
                                           'plan_percent': 2000,
                                           'plan_value': 200000000,
                                           'deviation': -3000,
                                           'level_value': 160000000,
                                           'next_deviation': -2000},
                                          {'asset_class_id': 1,
                                           'location_id': 2,
                                           'current_value': 140000000,
                                           'plan_percent': 2000,
                                           'plan_value': 200000000,
                                           'deviation': -3000,
                                           'level_value': 170000000,
                                           'next_deviation': -1500},
                                          {'asset_class_id': 1,
                                           'location_id': 2,
                                           'current_value': 140000000,
                                           'plan_percent': 2000,
                                           'plan_value': 200000000,
                                           'deviation': -3000,
                                           'level_value': 272000000,
                                           'next_deviation': 3600},
                                          {'asset_class_id': 1,
                                           'location_id': 2,
                                           'current_value': 140000000,
                                           'plan_percent': 2000,
                                           'plan_value': 200000000,
                                           'deviation': -3000,
                                           'level_value': 280000000,
                                           'next_deviation': 4000},
                                          {'asset_class_id': 2,
                                           'location_id': 2,
                                           'current_value': 40000000,
                                           'plan_percent': 500,
                                           'plan_value': 50000000,
                                           'deviation': -2000,
                                           'level_value': 42500000,
                                           'next_deviation': -1500},
                                          {'asset_class_id': 2,
                                           'location_id': 2,
                                           'current_value': 40000000,
                                           'plan_percent': 500,
                                           'plan_value': 50000000,
                                           'deviation': -2000,
                                           'level_value': 68000000,
                                           'next_deviation': 3600},
                                          {'asset_class_id': 2,
                                           'location_id': 2,
                                           'current_value': 40000000,
                                           'plan_percent': 500,
                                           'plan_value': 50000000,
                                           'deviation': -2000,
                                           'level_value': 70000000,
                                           'next_deviation': 4000},
                                          {'asset_class_id': 1,
                                           'location_id': 1,
                                           'current_value': 340000000,
                                           'plan_percent': 4000,
                                           'plan_value': 400000000,
                                           'deviation': -1500,
                                           'level_value': 544000000,
                                           'next_deviation': 3600},
                                          {'asset_class_id': 1,
                                           'location_id': 1,
                                           'current_value': 340000000,
                                           'plan_percent': 4000,
                                           'plan_value': 400000000,
                                           'deviation': -1500,
                                           'level_value': 560000000,
                                           'next_deviation': 4000},
                                          {'asset_class_id': 2,
                                           'location_id': 1,
                                           'current_value': 340000000,
                                           'plan_percent': 2500,
                                           'plan_value': 250000000,
                                           'deviation': 3600,
                                           'level_value': 350000000,
                                           'next_deviation': 4000}]

value_difference_deviation_level_expected = [{'asset_class_id': 1,
                                              'location_id': 2,
                                              'current_value': 140000000,
                                              'plan_percent': 2000,
                                              'plan_value': 200000000,
                                              'deviation': -3000,
                                              'level_value': 160000000,
                                              'value_difference': 20000000,
                                              'next_deviation': -2000},
                                             {'asset_class_id': 1,
                                              'location_id': 2,
                                              'current_value': 140000000,
                                              'plan_percent': 2000,
                                              'plan_value': 200000000,
                                              'deviation': -3000,
                                              'level_value': 170000000,
                                              'value_difference': 30000000,
                                              'next_deviation': -1500},
                                             {'asset_class_id': 1,
                                              'location_id': 2,
                                              'current_value': 140000000,
                                              'plan_percent': 2000,
                                              'plan_value': 200000000,
                                              'deviation': -3000,
                                              'level_value': 272000000,
                                              'value_difference': 132000000,
                                              'next_deviation': 3600},
                                             {'asset_class_id': 1,
                                              'location_id': 2,
                                              'current_value': 140000000,
                                              'plan_percent': 2000,
                                              'plan_value': 200000000,
                                              'deviation': -3000,
                                              'level_value': 280000000,
                                              'value_difference': 140000000,
                                              'next_deviation': 4000},
                                             {'asset_class_id': 2,
                                              'location_id': 2,
                                              'current_value': 40000000,
                                              'plan_percent': 500,
                                              'plan_value': 50000000,
                                              'deviation': -2000,
                                              'level_value': 42500000,
                                              'value_difference': 2500000,
                                              'next_deviation': -1500},
                                             {'asset_class_id': 2,
                                              'location_id': 2,
                                              'current_value': 40000000,
                                              'plan_percent': 500,
                                              'plan_value': 50000000,
                                              'deviation': -2000,
                                              'level_value': 68000000,
                                              'value_difference': 28000000,
                                              'next_deviation': 3600},
                                             {'asset_class_id': 2,
                                              'location_id': 2,
                                              'current_value': 40000000,
                                              'plan_percent': 500,
                                              'plan_value': 50000000,
                                              'deviation': -2000,
                                              'level_value': 70000000,
                                              'value_difference': 30000000,
                                              'next_deviation': 4000},
                                             {'asset_class_id': 1,
                                              'location_id': 1,
                                              'current_value': 340000000,
                                              'plan_percent': 4000,
                                              'plan_value': 400000000,
                                              'deviation': -1500,
                                              'level_value': 544000000,
                                              'value_difference': 204000000,
                                              'next_deviation': 3600},
                                             {'asset_class_id': 1,
                                              'location_id': 1,
                                              'current_value': 340000000,
                                              'plan_percent': 4000,
                                              'plan_value': 400000000,
                                              'deviation': -1500,
                                              'level_value': 560000000,
                                              'value_difference': 220000000,
                                              'next_deviation': 4000},
                                             {'asset_class_id': 2,
                                              'location_id': 1,
                                              'current_value': 340000000,
                                              'plan_percent': 2500,
                                              'plan_value': 250000000,
                                              'deviation': 3600,
                                              'level_value': 350000000,
                                              'value_difference': 10000000,
                                              'next_deviation': 4000}]

where_to_contribute_expected = {0: [],
                                1000: [{'asset_class_id': 1,
                                        'location_id': 2,
                                        'contribution': 10000000}],
                                10000: [{'asset_class_id': 1,
                                         'location_id': 2,
                                         'contribution': 50765539},
                                        {'asset_class_id': 2,
                                         'location_id': 2,
                                         'contribution': 7691385},
                                        {'asset_class_id': 1,
                                         'location_id': 1,
                                         'contribution': 41543076}],
                                100000: [{'asset_class_id': 1,
                                          'location_id': 2,
                                          'contribution': 260000000},
                                         {'asset_class_id': 2,
                                          'location_id': 2,
                                          'contribution': 60000000},
                                         {'asset_class_id': 1,
                                          'location_id': 1,
                                          'contribution': 460000000},
                                         {'asset_class_id': 2,
                                          'location_id': 1,
                                          'contribution': 160000000},
                                         {'asset_class_id': 3,
                                          'location_id': 1,
                                          'contribution': 60000000}]}
