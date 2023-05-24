import threading

def f1():
    import END_TG_TEST
def f2():
    import Vk
t1 = threading.Thread(target=f1)
t2 = threading.Thread(target=f2)

t1.start()
t2.start()