# -*- coding: utf-8 -*-
import logging
import logging.config

# 采用配置文件配置
logging.config.fileConfig('logging.conf')
# 创建logger
logger = logging.getLogger('infoLogger')


