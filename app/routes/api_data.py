from fastapi import APIRouter, HTTPException, status, File, UploadFile, Request, Depends
from fastapi.responses import StreamingResponse

from app.utils.utils import get_hashed_password, verify_password
from app.utils.repo import JWTRepo, JWTBearer, JWTBearerAdmin

from app.config.config import db
from app.schemas.user import userEntity, usersEntity
from app.main_data.getData import times, stateOk, inspection, data

from datetime import date, datetime

from bson import ObjectId
import base64

import pandas as pd
import io
from UliPlot.XLSX import auto_adjust_xlsx_column_width

import numpy as np


app_router = APIRouter()


stateFail = [0 for i in range(0, 7)]
for i in range(0, 7):
    stateFail[i] = times[i] - stateOk[i]


@app_router.get("/chart-data", dependencies=[Depends(JWTBearer())])
async def chart_data():
    return {"count": times, "stateOk": stateOk, "stateFail": stateFail}


@app_router.get("/status-success", dependencies=[Depends(JWTBearer())])
async def status_success():
    percent = round(100 * (sum(stateOk) / sum(times)), 2)
    return {"state_ok": (format(sum(stateOk), ",d")), "percent": percent}


@app_router.get("/total-check-times", dependencies=[Depends(JWTBearer())])
async def status_fail():
    return {"total_check": (format(sum(times), ",d"))}


@app_router.get("/get-inspection", dependencies=[Depends(JWTBearer())])
async def get_inspection():
    return {"data": inspection}


@app_router.get("/get-inspection-detail")
async def get_inspection_detail(id: str):
    try:
        detail_predict = []
        angid = [0 for i in range(0, 7)]
        listA = data[id]
        for detail in listA:
            temp = listA[detail]
            num = int(temp["angle_id"])
            angid[num - 1] += 1

            time = datetime.fromisoformat(temp["date"])
            dt = time.strftime("%Y/%m/%d %H:%M:%S").split(" ")

            detail_predict.append(
                {
                    "date": dt[0],
                    "time": dt[1],
                    "angle_id": temp["angle_id"],
                    "status": temp["status"],
                    "predict_result": temp["predict_result"],
                }
            )

        # get labels
        labels = dict()
        if data[id]:
            for item in data[id]:
                result = data[id][item]
                for i in result["predict_result"]:
                    if i in labels:
                        labels[i] += 1
                    else:
                        labels[i] = 1
        else:
            raise HTTPException(status_code=404, detail="Id invalid")

        labels_key = sorted(labels)
        result = []
        for i in range(len(labels_key)):
            result.append(labels[labels_key[i]])
        return {"angle_id": angid, "all_details": detail_predict, "label": labels_key, "value": result}
    except:
        raise HTTPException(status_code=500)


@app_router.post("/upload-avatar", dependencies=[Depends(JWTBearer())])
async def upload_avatar(file: UploadFile, id: str):
    allowedFiles = {
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/tiff",
        "image/bmp",
        "video/webm",
    }
    if file.content_type in allowedFiles:
        user = userEntity(db.find_one({"_id": ObjectId(id)}))
        try:
            contents = base64.b64encode(file.file.read())
            # with open("uploaded_" + file.filename, "wb") as f:
            #     f.write(contents)

            # print(contents)

            # user["image"] = contents
            # db.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})

        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()

        return {"message": f"Successfuly uploaded {file.filename}"}
    raise HTTPException(status_code=415, detail="Unsupported Media Type")


@app_router.get("/download_api_data", dependencies=[Depends(JWTBearer())])
async def download_api_data():
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    for id in data:
        df = pd.DataFrame(data[id])
        name = id.replace("/", "-")
        df.to_excel(writer, sheet_name=name)
        auto_adjust_xlsx_column_width(df, writer, sheet_name=name, margin=0)
    writer.close()
    xlsx_data = output.getvalue()

    return StreamingResponse(
        io.BytesIO(xlsx_data),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=api_data.xlsx"},
    )


@app_router.get("/id_statistic", dependencies=[Depends(JWTBearer())])
async def id_statistic():

    # get labels
    labels = dict()
    for i in data:
        if i[0:3] in labels:
            labels[i[0:3]] += 1
        else:
            labels[i[0:3]] = 1
    value = []
    label = sorted(labels)
    for i in range(len(label)):
        value.append(labels[label[i]])
    return {"label": label, "value": value}


# @app_router.get("/predict_result_statistic", dependencies=[Depends(JWTBearer())])
# async def predict_result_statistic(id):
