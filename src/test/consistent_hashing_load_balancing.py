from test_helper.load_balancing_test import lb_test
from app.load_balancing import ConsistentHashing

if __name__ == '__main__':
    lb_test(lambda x: ConsistentHashing(x))
