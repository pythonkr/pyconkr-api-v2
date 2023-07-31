from django.contrib.auth import get_user_model
from django.db import models
from sorl.thumbnail import ImageField as SorlImageField

User = get_user_model()


class SponsorLevelManager(models.Manager):
    def get_queryset(self):
        return super(SponsorLevelManager, self).get_queryset().all().order_by("order")


class SponsorLevel(models.Model):
    class Meta:
        verbose_name = "후원사 등급"
        verbose_name_plural = "후원사 등급"

    name = models.CharField(max_length=255, blank=True, default="", help_text="후원 등급명")
    desc = models.TextField(
        null=True, blank=True, help_text="후원 혜택을 입력하면 될 거 같아요 :) 후원사가 등급을 정할 때 볼 문구입니다."
    )
    visible = models.BooleanField(default=True)
    price = models.IntegerField(default=0)
    limit = models.IntegerField(default=0, help_text="후원사 등급별 구좌 수")
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SponsorLevelManager()

    @property
    def current_remaining_number(self):
        return (
            0
            if self.limit - self.accepted_count < 0
            else self.limit - self.accepted_count
        )

    @property
    def paid_count(self):
        return Sponsor.objects.filter(
            level=self, submitted=True, accepted=True, paid_at__isnull=False
        ).count()

    @property
    def accepted_count(self):
        return Sponsor.objects.filter(level=self, submitted=True, accepted=True).count()

    def __str__(self):
        return self.name


def registration_file_upload_to(instance, filename):
    return f"sponsor/business_registration/{instance.id}/{filename}"


def bank_book_file_upload_to(instance, filename):
    return f"sponsor/bank_book/{instance.id}/{filename}"


def logo_image_upload_to(instance, filename):
    return f"sponsor/logo/{instance.id}/{filename}"


class Sponsor(models.Model):
    class Meta:
        ordering = ["paid_at", "id"]
        verbose_name = "후원사"
        verbose_name_plural = "후원사 목록"

    creator = models.ForeignKey(
        User,
        null=True,  # TODO: 추후 로그인 적용 후 입력
        blank=True,  # TODO: 추후 로그인 적용 후 입력
        on_delete=models.CASCADE,
        help_text="후원사를 등록한 유저",
        related_name="sponsor_creator",
    )
    name = models.CharField(
        max_length=255, help_text="후원사의 이름입니다. 서비스나 회사 이름이 될 수 있습니다."
    )
    level = models.ForeignKey(
        SponsorLevel,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        help_text="후원을 원하시는 등급을 선택해주십시오. 모두 판매된 등급은 선택할 수 없습니다.",
    )
    desc = models.TextField(
        null=True, blank=True, help_text="후원사 설명입니다. 이 설명은 국문 홈페이지에 게시됩니다."
    )
    eng_desc = models.TextField(
        null=True, blank=True, help_text="후원사 영문 설명입니다. 이 설명은 영문 홈페이지에 게시됩니다."
    )
    manager_name = models.CharField(
        max_length=100, help_text="준비위원회와 후원과 관련된 논의를 진행할 담당자의 이름을 입력해주십시오."
    )
    manager_email = models.CharField(
        max_length=100,
        help_text="입력하신 메일로 후원과 관련된 안내 메일이나 문의를 보낼 예정입니다. 후원 담당자의 이메일 주소를 입력해주십시오.",
    )
    manager_tel = models.CharField(
        max_length=20,
        default="",
        help_text="메일에 회신이 없거나, 긴급한 건의 경우, 문자나 유선으로 안내드릴 수 있습니다. 후원 담당자의 유선 연락처를 입력해주십시오.",
    )
    manager_id = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="후원사를 위한 추가 아이디",
        related_name="sponsor_temp_id",
    )
    business_registration_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="후원사 사업자 등록 번호입니다. 세금 계산서 발급에 사용됩니다.",
    )
    business_registration_file = models.FileField(
        null=True,
        blank=True,
        default=None,
        upload_to=registration_file_upload_to,
        help_text="후원사 사업자 등록증 스캔본입니다. 세금 계산서 발급에 사용됩니다.",
    )
    bank_book_file = models.FileField(
        null=True,
        blank=True,
        upload_to=bank_book_file_upload_to,
        help_text="후원사 통장 사본입니다.",
    )
    url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="파이콘 한국 홈페이지에 공개되는 후원사 홈페이지 주소입니다.",
    )
    logo_image = SorlImageField(
        upload_to=logo_image_upload_to,
        null=True,
        blank=True,
        help_text="홈페이지에 공개되는 후원사 로고 이미지입니다.",
    )
    submitted = models.BooleanField(
        default=False,
        help_text="사용자가 제출했는지 여부를 저장합니다. 요청이 제출되면 준비위원회에서 검토하고 받아들일지를 결정합니다.",
    )
    accepted = models.BooleanField(
        default=False, help_text="후원사 신청이 접수되었고, 입금 대기 상태인 경우 True로 설정됩니다."
    )
    paid_at = models.DateTimeField(
        null=True, blank=True, help_text="후원금이 입금된 일시입니다. 아직 입금되지 않았을 경우 None이 들어갑니다."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}/{self.level}"



class Patron(models.Model):
    class Meta:
        ordering = ["-total_contribution", "contribution_datetime"]
        verbose_name = "개인후원자"
        verbose_name_plural = "개인후원자 목록"

    name = models.CharField(max_length=100)
    creator = models.ForeignKey(
        User,
        null=True,  # TODO: 추후 로그인 적용 후 입력
        blank=True,  # TODO: 추후 로그인 적용 후 입력
        on_delete=models.CASCADE,
        help_text="개인후원을 등록한 유저",
        related_name="patron_user",
    )
    total_contribution = models.IntegerField(default=0, help_text="개인후원한 금액입니다.")
    contribution_datetime = models.DateTimeField(
        help_text="개인후원 결제한 일시입니다."
    )
    contribution_message = models.TextField(
        help_text="후원메시지입니다. emoji 를 입력가능해야하고 html 태그가 들어갈 수 있습니다."
    )
    # need html sanitizing before saving
    # but need to include emoji

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
