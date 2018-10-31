# from architecture import init_adder
from architecture import Processor

# file = open("testfile.txt", "w")
# file.write("Hello World")
# file.close()
#
# file = open("testfile.txt", "r")
# x = file.read(5)
# print(x)
# file.close()

# with open("processor_config.txt", "r") as f:
#     data = f.readlines()
#     for line in data:
#         words = line.split()
#         print(words)

# Class example
# class MyClass:
#     """A simple example class"""
#     i = 12345
#
#     def func(self):
#         return 'hello world'
#
# x = MyClass()
# print(x.func())
# x.counter = 1
# while x.counter < 10:
#     x.counter = x.counter * 2
# print(x.counter)
# del x.counter

# ---------------------------------------





# f = open('processor_config.txt', 'r')
# lines = f.readlines()
# f.close()
#
# proc_config = ProcessorConfig()
# proc_config.read_config()
# proc_config.print_config()
#
# for i, line in enumerate(lines):
#     if "Integer adder" in line and i+1 < len(lines):
#         print(lines[i+1])
#         words = line.split()
#
#         print(words)
#
#         break

def main():
    # init_adder(proc_config.adder)
    reg_int_val = []
    reg_float_val = []
    for i in range(32):     # 0-31
        reg_int_val.append(i)
        reg_float_val.append(i)
    # print(init_val)

    mem_val = []
    for i in range(64):     # 0-63
        mem_val.append(0)

    processor = Processor(128, -1, reg_int_val, reg_float_val, mem_val)
    processor.do_adder()


if __name__ == '__main__':
    main()
