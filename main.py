from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware

import uvicorn

app_name = "op-wchat"
app = FastAPI(
    title="op-wxchat-api",
    description="基于微信接口服务",
    version="0.1.0",
)

origins = [
    "http://wx.123go.club"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"


@app.get("/v1/wx", summary="微信回调接口", tags=["WX"])
def wx_callback(signature: str, timestamp: str, nonce: str, echostr: str):
    import hashlib
    import json

    wx_token="weixinchat"
    
    l = [wx_token, timestamp, nonce]
    l = sorted(l)
    
    sha1 = hashlib.sha1()
    sha1.update("".join(l).encode())

    hashcode = sha1.hexdigest()
    print("hashcode, signature: ", hashcode, signature)
    
    if hashcode == signature:
        return json.loads(echostr)
    else:
        return ""


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='FastApi Run Server Args')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    port = args.port
    uvicorn.run(app, log_config=log_config, port=port, host="0.0.0.0")
