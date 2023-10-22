import logging

#logging untuk mengecek activity 
logging.basicConfig(filename=r'D:\Python\TUGAS3\app\logs\log_flask.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(asctime)s - %(levelname)s - %(message)s')
flasklogger = logging.getLogger('test_logger')