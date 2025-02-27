import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from locations.models import Location
from weather.models import Weather


class Command(BaseCommand):
    help = "Fetch weather data from the Korean Meteorological Administration API"

    def handle(self, *args, **kwargs):
        location_codes = {
            1: {"nx": 60, "ny": 127},  # 서울
            2: {"nx": 60, "ny": 120},  # 경기도
            3: {"nx": 55, "ny": 124},  # 인천
            4: {"nx": 73, "ny": 134},  # 강원도
            5: {"nx": 87, "ny": 106},  # 경상북도
            6: {"nx": 91, "ny": 77},  # 경상남도
            7: {"nx": 89, "ny": 90},  # 대구
            8: {"nx": 102, "ny": 84},  # 울산
            9: {"nx": 98, "ny": 76},  # 부산
            10: {"nx": 69, "ny": 107},  # 충청북도
            11: {"nx": 68, "ny": 100},  # 충청남도
            12: {"nx": 66, "ny": 103},  # 세종
            13: {"nx": 67, "ny": 100},  # 대전
            14: {"nx": 63, "ny": 89},  # 전라북도
            15: {"nx": 51, "ny": 67},  # 전라남도
            16: {"nx": 58, "ny": 74},  # 광주
            17: {"nx": 52, "ny": 38},  # 제주도
        }

        # 현재 날짜와 내일 날짜 계산
        base_date = datetime.now().strftime("%Y%m%d")
        base_time = "0220"  # 새벽 02:00 발표 시각

        service_key = settings.KMA_API_KEY  # 기상청 공공 API 키

        for location_id, coords in location_codes.items():
            location = Location.objects.get(pk=location_id)
            nx, ny = coords["nx"], coords["ny"]

            url = (
                f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
                f"?serviceKey={service_key}&numOfRows=1000&pageNo=1&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}&dataType=JSON"
            )

            print(f"Request URL: {url}")

            response = requests.get(url)
            if response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR(f"Failed to fetch data: {response.status_code}")
                )
                self.stdout.write(
                    self.style.ERROR(f"Response content: {response.content}")
                )
                continue

            try:
                data = response.json()
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"JSON decode error: {e}"))
                self.stdout.write(
                    self.style.ERROR(f"Response content: {response.content}")
                )

                # XML 응답 처리
                try:
                    root = ET.fromstring(response.content)
                    err_msg = root.find(".//errMsg").text
                    return_auth_msg = root.find(".//returnAuthMsg").text
                    return_reason_code = root.find(".//returnReasonCode").text

                    self.stdout.write(
                        self.style.ERROR(
                            f"API Error: {err_msg}, {return_auth_msg}, {return_reason_code}"
                        )
                    )
                except ET.ParseError as parse_error:
                    self.stdout.write(
                        self.style.ERROR(f"XML parse error: {parse_error}")
                    )

                continue

            if data["response"]["header"]["resultCode"] == "00":
                items = data["response"]["body"]["items"]["item"]

                weather_data = {
                    base_date: {},
                }  # 날씨 데이터를 저장할 딕셔너리

                for item in items:
                    fcst_date = item["fcstDate"]
                    category = item["category"]
                    fcst_value = item["fcstValue"]

                    # KeyError를 방지하기 위해 날짜의 엔트리가 존재하지 않으면 생성
                    if fcst_date not in weather_data:
                        weather_data[fcst_date] = {
                            "POP": None,
                            "TMN": None,
                            "TMX": None,
                            "SKY": None,
                        }

                    # 요청한 카테고리 데이터만 저장
                    if category in ["POP", "TMN", "TMX", "SKY"]:
                        if category in ["TMN", "TMX"]:  # 실수로 변환할 값
                            fcst_value = float(fcst_value)
                        else:  # 정수로 변환할 값
                            fcst_value = int(fcst_value)

                        weather_data[fcst_date][category] = fcst_value

                # Debug용 출력
                for date, data in weather_data.items():
                    print(f"Location: {location.city}, Date: {date}, Data: {data}")

                # Save to the database
                for date, data in weather_data.items():
                    if any(
                        value is not None for value in data.values()
                    ):  # 적어도 하나의 값이 있는 경우에만 저장
                        weather, created = Weather.objects.update_or_create(
                            location=location,
                            base_date=base_date,
                            fcst_date=date,
                            defaults={
                                "POP": data.get("POP"),
                                "TMN": data.get("TMN"),
                                "TMX": data.get("TMX"),
                                "SKY": data.get("SKY"),
                            },
                        )

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Created new weather record for {location.city}, date {date}"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Updated weather record for {location.city}, date {date}"
                                )
                            )
            else:
                self.stdout.write(self.style.ERROR("Failed to fetch data from API"))
