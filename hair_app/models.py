from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class HairProfile(models.Model):
    """
    Profil włosów użytkownika – dane osobowe + ankieta o włosach.
    Podpięte 1:1 pod konto użytkownika.
    """

    class Gender(models.TextChoices):
        female = "K", "Kobieta"
        male = "M", "Mężczyzna"
        other = "I", "Inna"

    class Porosity(models.TextChoices):
        low = "Low", "Niskoporowate"
        medium = "Med", "Średnioporowate"
        high = "High", "Wysokoporowate"

    class HairLength(models.TextChoices):
        SHORT = "S", "Krótkie"
        MEDIUM = "M", "Średnie"
        LONG = "L", "Długie"

    class CurlType(models.TextChoices):
        straight = "1", "Proste"
        wavy = "2", "Falowane"
        curly = "3", "Kręcone"
        coily = "4", "Afro"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="hair_profile",
        help_text="Konto użytkownika powiązane z tym profilem włosów.",
    )

    # Dane profilowe
    imie = models.CharField("Imię", max_length=50)
    nazwisko = models.CharField("Nazwisko", max_length=100)
    plec = models.CharField(
        "Płeć",
        max_length=1,
        choices=Gender.choices,
        default=Gender.other,
    )

    # Ankieta włosowa
    porowatosc = models.CharField(
        "Porowatość",
        max_length=4,
        choices=Porosity.choices,
        default=Porosity.medium,
    )
    dlugosc = models.CharField(
        "Długość włosów",
        max_length=1,
        choices=HairLength.choices,
        default=HairLength.MEDIUM,
    )
    skret = models.CharField(
        "Typ skrętu",
        max_length=1,
        choices=CurlType.choices,
        default=CurlType.straight,
    )
    tluszczenie = models.BooleanField(
        "Przetłuszczająca się skóra głowy",
        default=False,
    )
    farba = models.BooleanField(
        "Czy włosy są farbowane",
        default=False,
    )


    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Profil włosów"
        verbose_name_plural = "Profile włosów"

    def __str__(self):
        return f"Profil włosów: {self.user.username}"


class HairProduct(models.Model):
    """
    Produkt do włosów – używany w podpowiedzi pielęgnacyjnej.
    """

    class Category(models.TextChoices):
        szampon = "SH", "Szampon"
        odzywka = "CO", "Odżywka"
        maskaa = "MA", "Maska"
        olejki = "OI", "Olejek"
        odbezspl = "LI", "Odżywka bez spłukiwania"
        serum = "SE", "Serum / kuracja"

    name = models.CharField("Nazwa produktu", max_length=150)
    brand = models.CharField("Marka", max_length=100, blank=True)
    category = models.CharField(
        "Kategoria",
        max_length=2,
        choices=Category.choices,
    )
    description = models.TextField("Opis", blank=True)

    # Dopasowanie do typu włosów – do rekomendacji
    suitable_porosity = models.CharField(
        "Dla jakiej porowatości",
        max_length=4,
        choices=HairProfile.Porosity.choices,
        blank=True,
        help_text="Opcjonalnie – jeśli produkt jest szczególnie polecany dla danego typu porowatości.",
    )
    suitable_curl_type = models.CharField(
        "Dla jakiego typu skrętu",
        max_length=1,
        choices=HairProfile.CurlType.choices,
        blank=True,
    )

    is_featured = models.BooleanField(
        "Polecany produkt",
        default=False,
        help_text="Jeśli zaznaczone – może się pojawiać w sekcji podpowiedzi pielęgnacyjnej.",
    )

    shop_url = models.URLField(
        "Link do sklepu",
        blank=True,
        help_text="Jeśli macie docelowo sklep – tu można dodać link do zakupu.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produkt do włosów"
        verbose_name_plural = "Produkty do włosów"

    def __str__(self):
        if self.brand:
            return f"{self.brand} – {self.name}"
        return self.name


class HairRoutineEntry(models.Model):
    """
    Pojedynczy wpis w kalendarzu pielęgnacji (dzień + co było robione).
    """

    class CareType(models.TextChoices):
        WASH = "WASH", "Mycie"
        CONDITIONER = "COND", "Odżywka"
        MASK = "MASK", "Maska"
        OIL = "OIL", "Olejowanie"
        SCALP = "SCALP", "Pielęgnacja skóry głowy"
        STYLING = "STYLE", "Stylizacja"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hair_routines",
    )
    date = models.DateField("Data pielęgnacji")
    care_type = models.CharField(
        "Rodzaj pielęgnacji",
        max_length=6,
        choices=CareType.choices,
    )
    products_used = models.ManyToManyField(
        HairProduct,
        blank=True,
        related_name="used_in_routines",
        verbose_name="Użyte produkty",
    )
    notes = models.TextField(
        "Notatki",
        blank=True,
        help_text="Np. jak zareagowały włosy, co się sprawdziło, co nie.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wpis pielęgnacji"
        verbose_name_plural = "Wpisy pielęgnacji"
        ordering = ["-date", "-created_at"]
        unique_together = ("user", "date", "care_type")

    def __str__(self):
        return f"{self.user.username} – {self.care_type} – {self.date}"


class HairTip(models.Model):
    """
    Porady pielęgnacyjne dopasowane do typu włosów.
    Np. 'Jak dbać o włosy wysokoporowate, kręcone, długie'.
    """

    title = models.CharField("Tytuł porady", max_length=150)
    content = models.TextField("Treść porady")

    porowatosc = models.CharField(
        "Porowatość docelowa",
        max_length=4,
        choices=HairProfile.Porosity.choices,
        blank=True,
        help_text="Zostaw puste, jeśli porada jest ogólna.",
    )
    skret = models.CharField(
        "Typ skrętu docelowy",
        max_length=1,
        choices=HairProfile.CurlType.choices,
        blank=True,
    )
    dlugosc = models.CharField(
        "Długość włosów docelowa",
        max_length=1,
        choices=HairProfile.HairLength.choices,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Porada pielęgnacyjna"
        verbose_name_plural = "Porady pielęgnacyjne"

    def __str__(self):
        return self.title













