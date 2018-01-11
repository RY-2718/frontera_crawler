import datetime
import sys

argv = sys.argv
first_time = argv[1]
first_time = datetime.datetime.strptime(first_time, '%Y-%m-%d_%H:%M:%S')
first_num = int(argv[2])
end_time = argv[3]
end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d_%H:%M:%S')
end_num = int(argv[4])
print("%s" % (end_time - first_time))
print("%s - %s" % (first_time.strftime("%Y/%m/%d %H:%M:%S"), end_time.strftime("%Y/%m/%d %H:%M:%S")))

delta = (end_time - first_time).total_seconds() / 60
sum = end_num - first_num
print("total %d pages, %f pages/min" % (sum, sum / delta))
