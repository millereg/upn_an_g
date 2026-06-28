import gzip
import io
import json
import urllib.request
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.ubicacion.models import Ciudad, Departamento, Pais, Provincia

GITHUB_RAW = (
    "https://raw.githubusercontent.com"
    "/dr5hn/countries-states-cities-database/master/json"
)
GITHUB_RELEASES = (
    "https://github.com/dr5hn/countries-states-cities-database/releases/latest/download"
)
UBIGEO_RAW = "https://raw.githubusercontent.com/ernestorivero/Ubigeo-Peru/master/json"


class Command(BaseCommand):
    help = "Importa países, departamentos, provincias y ciudades desde APIs públicas"

    def add_arguments(self, parser):
        parser.add_argument(
            "--paises",
            nargs="+",
            metavar="ISO2",
            help="Filtrar por código ISO-2 (ej: --paises PE US MX). Sin filtro importa todo.",
        )

    def handle(self, *args, **options):
        filtro = {c.upper() for c in (options.get("paises") or [])}

        # ── Perú con UBIGEO (4 niveles reales) ──────────────────────────
        if not filtro or "PE" in filtro:
            self._importar_peru()

        # ── Resto de países con dr5hn (3 niveles) ───────────────────────
        otros = filtro - {"PE"}
        if not filtro or otros:
            self._importar_dr5hn(otros)

        self.stdout.write(self.style.SUCCESS("Importación completada exitosamente."))

    # ------------------------------------------------------------------
    def _importar_peru(self):
        self.stdout.write("⬇  [PE] Descargando UBIGEO Perú...")
        departamentos = self._fetch(f"{UBIGEO_RAW}/ubigeo_peru_2016_departamentos.json")
        provincias = self._fetch(f"{UBIGEO_RAW}/ubigeo_peru_2016_provincias.json")
        distritos = self._fetch(f"{UBIGEO_RAW}/ubigeo_peru_2016_distritos.json")

        provs_by_dept = {}
        for p in provincias:
            provs_by_dept.setdefault(p["department_id"], []).append(p)

        dists_by_prov = {}
        for d in distritos:
            dists_by_prov.setdefault(d["province_id"], []).append(d)

        self.stdout.write(
            f"  Procesando {len(departamentos)} departamentos · "
            f"{len(provincias)} provincias · {len(distritos)} distritos..."
        )

        with transaction.atomic():
            pais, _ = Pais.objects.get_or_create(
                codigo="PE",
                defaults={"nombre": "Perú"},
            )
            for dept in departamentos:
                dpto, _ = Departamento.objects.get_or_create(
                    nombre=dept["name"].strip()[:75],
                    pais=pais,
                )
                for prov in provs_by_dept.get(dept["id"], []):
                    provincia, _ = Provincia.objects.get_or_create(
                        nombre=prov["name"].strip()[:85],
                        departamento=dpto,
                    )
                    for dist in dists_by_prov.get(prov["id"], []):
                        Ciudad.objects.get_or_create(
                            nombre=dist["name"].strip()[:75],
                            provincia=provincia,
                        )

        self.stdout.write("  ✔ Perú")

    # ------------------------------------------------------------------
    def _importar_dr5hn(self, filtro: set):
        self.stdout.write("⬇  Descargando países...")
        countries = self._fetch(f"{GITHUB_RAW}/countries.json")

        self.stdout.write("⬇  Descargando estados / departamentos...")
        states = self._fetch(f"{GITHUB_RAW}/states.json")

        self.stdout.write(
            "⬇  Descargando ciudades (archivo ~18 MB gz, puede tardar)..."
        )
        cities = self._fetch_gz(f"{GITHUB_RELEASES}/json-cities.json.gz")

        if filtro:
            countries = [c for c in countries if c.get("iso2", "").upper() in filtro]

        # Excluir PE (ya importado con UBIGEO)
        countries = [c for c in countries if c.get("iso2", "").upper() != "PE"]

        states_by_country: dict = {}
        for s in states:
            states_by_country.setdefault(s["country_id"], []).append(s)

        cities_by_state: dict = {}
        for city in cities:
            cities_by_state.setdefault(city["state_id"], []).append(city)

        self.stdout.write(f"  Procesando {len(countries)} países...")

        with transaction.atomic():
            for country in countries:
                pais, _ = Pais.objects.get_or_create(
                    codigo=country["iso2"][:5],
                    defaults={"nombre": country["name"][:45]},
                )
                for state in states_by_country.get(country["id"], []):
                    dpto, _ = Departamento.objects.get_or_create(
                        nombre=state["name"][:75],
                        pais=pais,
                    )
                    provincia, _ = Provincia.objects.get_or_create(
                        nombre=state["name"][:85],
                        departamento=dpto,
                    )
                    for city in cities_by_state.get(state["id"], []):
                        Ciudad.objects.get_or_create(
                            nombre=city["name"][:75],
                            provincia=provincia,
                        )
                self.stdout.write(f"  ✔ {country['name']}")

    # ------------------------------------------------------------------
    def _fetch(self, url: str) -> list:
        with urllib.request.urlopen(url, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))

    def _fetch_gz(self, url: str) -> list:
        req = urllib.request.Request(url, headers={"Accept-Encoding": "identity"})
        with urllib.request.urlopen(req, timeout=180) as response:
            raw = response.read()
        with gzip.open(io.BytesIO(raw)) as gz_file:
            return json.loads(gz_file.read().decode("utf-8"))
