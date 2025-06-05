def generate_module_id():
    for i in range(1, 1000):
        module_id = 'M' + str(i).zfill(2) + '_'
        yield module_id


def generate_testcase_id():
    for i in range(1, 10000):
        case_id = 'C' + str(i).zfill(2) + '_'
        yield case_id


def generate_order():
    for order_id in range(1, 10000):
        yield order_id


m_id = generate_module_id()
c_id = generate_testcase_id()