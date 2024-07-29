# -*- coding: utf-8 -*-
import sys
sys.path.append("../")


from app_core import app
from views import nl2sql_blue


# 接口注册
app.register_blueprint(nl2sql_blue)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=63000, debug=False)