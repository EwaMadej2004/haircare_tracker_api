from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class HairProfile(models.Model):
    """
    Profil włosów użytkownika dane osobowe + ankieta o włosach.
    Podpięte 1:1 pod konto użytkownika.
    """

  

    GENDER = (
        ("K", "Kobieta"),
        ("M", "Mezczyzna"),
        ("O", "Other")
    )

    POROSITY = (
        ("Low", "Niskoporowate"),
        ("Med", "Średnioporowate"),
        ("High", "Wysokoporowate"),
    )

    HAIR_LENGTH = (
        ("S", "Krótkie"),
        ("M", "Średnie"),
        ("L", "Długie"),
    )

    CURL_TYPE = (
        ("1", "Proste"),
        ("2", "Falowane"),
        ("3", "Kręcone"),
        ("4", "Afro"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="hair_profile",
        help_text="Konto użytkownika powiązane z tym profilem włosów.",
    )

    imie = models.CharField("Imię", max_length=50)
    nazwisko = models.CharField("Nazwisko", max_length=100)
    plec = models.CharField(
        "Płeć",
        max_length=1,
        choices=GENDER,
        default="O",
    )

    
    porowatosc = models.CharField(
        "Porowatość",
        max_length=4,
        choices=POROSITY,
        default="Med",
    )
    dlugosc = models.CharField(
        "Długość włosów",
        max_length=1,
        choices=HAIR_LENGTH,
        default="M",
    )
    skret = models.CharField(
        "Typ skrętu",
        max_length=1,
        choices=CURL_TYPE,
        default="1",
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
    Produkt do włosów używany w podpowiedzi pielęgnacyjnej.
    """

    PRODUCT_CATEGORY = (
        ("SH", "Szampon"),
        ("CO", "Odżywka"),
        ("MA", "Maska"),
        ("OI", "Olejek"),
        ("LI", "Odżywka bez spłukiwania"),
        ("SE", "Serum / kuracja"),
    )


    name = models.CharField("Nazwa produktu", max_length=150)
    brand = models.CharField("Marka", max_length=100, blank=True)
    category = models.CharField(
        "Kategoria",
        max_length=2,
        choices=PRODUCT_CATEGORY,
    )
    description = models.TextField("Opis", blank=True)

    
    suitable_porosity = models.CharField(
        "Dla jakiej porowatości",
        max_length=4,
        choices=HairProfile.POROSITY,
        blank=True,
        help_text="Co robi produkt dla tego typu porowatości.",
    )
    suitable_curl_type = models.CharField(
        "Dla jakiego typu skrętu",
        max_length=1,
        choices=HairProfile.CURL_TYPE,
        blank=True,
    )

    is_featured = models.BooleanField(
        "Polecany produkt",
        default=False,
        help_text="Pojawienie sie w sekcji podpowiedzi pielęgnacji.",
    )

    shop_url = models.URLField(
        "Link do sklepu",
        blank=True,
        help_text="Link do sklepu gdzie można kupić dany produkt.",
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

    CARE_TYPE = (
        ("WASH", "Mycie"),
        ("COND", "Odżywka"),
        ("MASK", "Maska"),
        ("OIL", "Olejowanie"),
        ("SCALP", "Pielęgnacja skóry głowy"),
        ("STYLE", "Stylizacja"),
    )


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hair_routines",
    )
    date = models.DateField("Data pielęgnacji")
    care_type = models.CharField(
        "Rodzaj pielęgnacji",
        max_length=6,
        choices=CARE_TYPE,
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
        choices=HairProfile.POROSITY,
        blank=True,
        help_text="Zostaw puste, jeśli porada ogólna.",
    )
    skret = models.CharField(
        "Typ skrętu docelowy",
        max_length=1,
        choices=HairProfile.CURL_TYPE,
        blank=True,
    )
    dlugosc = models.CharField(
        "Długość włosów docelowa",
        max_length=1,
        choices=HairProfile.HAIR_LENGTH,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Porada pielęgnacyjna"
        verbose_name_plural = "Porady pielęgnacyjne"

    def __str__(self):
        return self.title