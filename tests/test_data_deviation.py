# test_data_deviation.py
# Test database dictionaries for allocation deviation tests
# 2024-01-30
# @juicemcpeso

expected = {0: [{'asset_class_id': 1,
                 'location_id': 2,
                 'current_value': 140000000,
                 'plan_percent': 2000,
                 'plan_value': 200000000,
                 'deviation': -3000,
                 'contribution': 0},
                {'asset_class_id': 2,
                 'location_id': 2,
                 'current_value': 40000000,
                 'plan_percent': 500,
                 'plan_value': 50000000,
                 'deviation': -2000,
                 'contribution': 0},
                {'asset_class_id': 1,
                 'location_id': 1,
                 'current_value': 340000000,
                 'plan_percent': 4000,
                 'plan_value': 400000000,
                 'deviation': -1500,
                 'contribution': 0}]}

#
# {'asset_class_id':,'location_id':,'current_value':,'plan_percent':,'plan_value':,'deviation':,'contribution':},
# {'asset_class_id':,'location_id':,'current_value':,'plan_percent':,'plan_value':,'deviation':,'contribution':}]}
#

# {'asset_class_id':,'location_id':,'current_value':,'plan_percent':,'plan_value':,'deviation':,'contribution':},
