from fastapi import APIRouter
from . import log_device_data,query_device_data,register_device
from typing import Dict,List

router = APIRouter()

router.post("/log_device_data")(log_device_data.fun)
router.get("/query_device_data/{device_id}",response_model=Dict[str,List[query_device_data.ChannelData]])(query_device_data.fun)
router.post("/register_device")(register_device.fun)

