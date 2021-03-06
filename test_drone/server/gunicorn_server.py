"""使用gunicorn运行服务.

注意,使用本项目的flask的log组件不能改变其log的format,但可以在配置文件中以`SERVER_CONFIG_`+[官方页面](http://docs.gunicorn.org/en/latest/settings.html#settings)
写出的配置项的大写来设置gunicorn的配置.从而修改log的形式.

推荐的设置有:

+ `"SERVER_CONFIG_ACCESS_LOG_FORMAT":"{\"remote_address\":\"%(h)s\",\"request_time\":\"%(t)s\",\"request\":\"%(m)s %(U)s\",\"status\":\"%(s)s\"}"`
    用于将access+log信息转为json形式.
+ `"SERVER_CONFIG_LOGLEVEL":"warning"`
    用于将服务器的系统信息log信息打印的等级提高.
+ `"SERVER_CONFIG_ERRORLOG": "gunicorn.log"`
    用于将服务器的log输出转移到文件中

需要注意如果要使用websocket,那么需要先安装`flask_sockets`,然后设置`"SERVER_CONFIG_WORKER_CLASS":"flask_sockets.worker"`
"""
import logging
from flask import Flask
from flask_sockets import SocketMiddleware
from gunicorn.app.base import Application

Formatters = {
    "server_json": logging.Formatter(**{
        "fmt": '''{"time":"%(asctime)s","name":"test_drone.server", "level":"%(levelname)s","msg":"%(message)s"}''',
        "datefmt": "%Y-%m-%dT%H:%M:%S Z"
    })
}


def run(app: Flask,
        host: str="0.0.0.0",
        port: int=5000,
        worker_class: str="sync",
        **kwargs):
    """使用gunicorn执行flask的app.

    详细参数可以查看<https://docs.gunicorn.org/en/stable/settings.html#access-log-format>

    Args:
        app (Flask): [description]
        host (str, optional): Defaults to "0.0.0.0". 启动服务器的主机名
        port (int, optional): Defaults to 5000. 服务端口
        worker_class (str, optional): Defaults to "sync". 指定使用什么来启动worker,默认为多进程

    Raises:
        AttributeError: 当使用websocket时如果worker_class
    """

    if isinstance(app.wsgi_app, SocketMiddleware):
        if worker_class != "flask_sockets.worker":
            raise AttributeError("websocket必须使用flask_sockets.worker作为worker")

    class FlaskApplication(Application):

        def init(self, parser, opts, args):
            data = {
                'bind': '{0}:{1}'.format(host, port)
            }
            data.update(
                kwargs
            )
            return data

        def load(self):
            return app

    wsgi_app = FlaskApplication()
    return wsgi_app.run()


__all__ = ["run"]
