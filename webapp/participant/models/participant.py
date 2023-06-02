import json

from django.db import models
from rest_framework.response import Response

from survey.models import Survey
from user.models import User


class Participant(models.Model):
    class Meta:
        db_table = 'participant'
        verbose_name = 'participant'
        verbose_name_plural = 'participants'

    user = models.ForeignKey(
        User,
        verbose_name="설문 참여자",
        on_delete=models.CASCADE,
        null=False,
    )

    survey = models.ForeignKey(
        Survey,
        verbose_name="설문",
        on_delete=models.CASCADE,
        null=False,
    )

    json = models.JSONField(
        verbose_name="설문 데이터",
        null=False,
    )

    created_at = models.DateTimeField(
        verbose_name="설문 참여 일시",
        auto_now_add=True,
    )

    update_at = models.DateTimeField(
        verbose_name="설문 재참여 일시",
        auto_now=True,
    )

    def __str__(self):
        return self.user.hidden_realName

    # json필드를 파싱하여 문자열 길이 계산
    @property
    def json_len_count(self):
        total_length = 0

        # JSON 데이터를 파싱하여 문자열 길이 계산
        try:
            data = json.dumps(self.json)
            data = json.loads(data)
            for value in data.values():
                if isinstance(value, str):
                    total_length += len(value)
        except json.JSONDecodeError:
            # JSON 파싱 에러 처리
            return Response({"error": "설문 응답(JSON)를 파싱할 수 없습니다."})

        return total_length

    # json필드를 파싱하여 3,4,5자의 문자열 반복 횟수 계산
    @property
    def json_duplication_count(self):
        duplication_count = 0
        string_counts = {}

        # json필드를 파싱하여 문자열 반복 횟수 계산
        try:
            data = json.dumps(self.json)
            data = json.loads(data)
            for value in data.values():
                if isinstance(value, str) and len(value) >= 3:
                    # 문자열 길이가 3 이상인 경우만 처리
                    for i in range(len(value) - 2):
                        substring = value[i:i + 3]
                        if substring in string_counts:
                            string_counts[substring] += 1
                        else:
                            string_counts[substring] = 1

            # 3, 4, 5자 이상 반복되는 문자열의 횟수 세기
            for count in string_counts.values():
                if count > 1:
                    duplication_count += 1
        except json.JSONDecodeError:
            # JSON 파싱 에러 처리
            return Response({"error": "설문 응답(JSON)를 파싱할 수 없습니다."})

        return duplication_count

    # 설문응답의 정성도의 기준
    @property
    def json_quality_standard(self):
        try:
            return int(((self.json_duplication_count / self.json_len_count) + (
                    self.json_len_count - self.json_duplication_count) / 100) * 10)
        except ZeroDivisionError:
            return 0
