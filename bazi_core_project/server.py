import os
from datetime import date
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
from Bazi_agent import run_analysis, build_archetype_title
from Bazi_calculate import calculate_bazi

app = FastAPI()

# 内存缓存
_cache = {}

class BirthRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)

    @field_validator('year', 'month', 'day', 'hour')
    @classmethod
    def validate_date(cls, v, info):
        return v

    def model_post_init(self, __context):
        # 验证日期真实存在
        try:
            date(self.year, self.month, self.day)
        except ValueError:
            raise ValueError(f"{self.year}年{self.month}月{self.day}日不是有效日期")

@app.post("/api/analyze")
def analyze(request: BirthRequest):
    try:
        # 验证日期
        try:
            date(request.year, request.month, request.day)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"{request.year}年{request.month}月{request.day}日不是有效日期"
            )

        # 检查缓存
        cache_key = (request.year, request.month, request.day, request.hour)
        if cache_key in _cache:
            return _cache[cache_key]

        # 最多重试2次
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                # 调用Agent
                result = run_analysis(request.year, request.month, request.day, request.hour)

                # 校验四柱
                expected_bazi = calculate_bazi(request.year, request.month, request.day, request.hour)
                if (result["year_pillar"] != expected_bazi["年柱"] or
                    result["month_pillar"] != expected_bazi["月柱"] or
                    result["day_pillar"] != expected_bazi["日柱"] or
                    result["hour_pillar"] != expected_bazi["时柱"]):

                    if attempt < max_retries:
                        continue  # 重试
                    else:
                        raise HTTPException(
                            status_code=502,
                            detail="生成结果校验未通过,请稍后重试"
                        )

                # 校验称号
                day_stem = result["day_pillar"][0]
                month_stem = result["month_pillar"][0]
                expected_title = build_archetype_title(day_stem, month_stem)
                if result["archetype_title"] != expected_title:
                    if attempt < max_retries:
                        continue  # 重试
                    else:
                        raise HTTPException(
                            status_code=502,
                            detail="生成结果校验未通过,请稍后重试"
                        )

                # 校验通过，缓存并返回
                _cache[cache_key] = result
                return result

            except HTTPException:
                raise
            except Exception as e:
                if attempt < max_retries:
                    continue
                else:
                    raise HTTPException(
                        status_code=502,
                        detail="生成失败,请稍后重试"
                    )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail="生成失败,请稍后重试"
        )

# 挂载静态文件
BASE_DIR = Path(__file__).parent
frontend_dir = BASE_DIR / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

@app.get("/")
def read_root():
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Frontend not found"}
