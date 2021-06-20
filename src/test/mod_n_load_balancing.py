from test_helper.load_balancing_test import lb_test
from app.load_balancing import ModN
from app import Server
from random import sample

if __name__ == '__main__':

    lb_test(lambda x: ModN(x))
