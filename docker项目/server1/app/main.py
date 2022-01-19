from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import logging
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
logger = logging.getLogger(__name__)
# 载入模型
from optiz.pre import pre
app = FastAPI()


class R_item(BaseModel):
    a: str
    n1: str
    n2: str
    n3: str
    n4: str


@app.post("v1/r/")
def r_pre(item: R_item):
    return_dict = {'code': '200', 'msg': '返回成功', 'data': False}
#  判断传入的数据是否为空
    if item is None:
        return_dict['code'] = '5004'
        return_dict['msg'] = '空'
        return return_dict
    date = item.a + item.n1 + item.n2 + item.n3 + item.n4
    return_dict['data'] = str({'r': pre(date)})
    return return_dict


if __name__ == '__main__':
    logger.info("Try to start the service......")
    uvicorn.run(app='main:app', host='0.0.0.0', port=7001, reload=True, debug=True)
    logger.info("Successfully started service!")

