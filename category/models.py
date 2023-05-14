from django.db import models


class Category(models.Model):
    ALCOHOL = (
        ("SOJU", "소주"),
        ("BEER", "맥주"),
        ("WINE", "와인"),
        ("LIQUOR", "양주"),
        ("TAKJU", "탁주"),
        ("ETC", "기타"),
    )

    category_name = models.CharField("카테고리 이름", choices=ALCOHOL, max_length=10)
    sul_name = models.CharField("제품이름", max_length=100, unique=True)

    def __str__(self):
        return (self.sul_name)
