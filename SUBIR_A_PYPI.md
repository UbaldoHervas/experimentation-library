# Publicación de ExperimentPy

El paquete se publica en PyPI como `experimentpy`. El código fuente está en
https://github.com/UbaldoHervas/experimentation-library.

Antes de publicar una versión, sube al repositorio el README, la documentación
y las imágenes de `docs/assets/`. PyPI carga esas imágenes mediante sus URLs
públicas de GitHub.

Desde la raíz del repositorio:

```bash
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
python -m build
python -m twine check --strict dist/*
```

Publica únicamente el wheel y el archivo fuente de la versión nueva. Para
esta actualización:

```bash
python -m twine upload dist/experimentpy-0.1.1-py3-none-any.whl dist/experimentpy-0.1.1.tar.gz
```

Al solicitar usuario, introduce `__token__`; como contraseña, utiliza un token
de PyPI válido con permiso para publicar `experimentpy`.

La distribución se publica mediante Twine usando la cuenta del propietario.
La autenticación de subida usa un token de PyPI. No añadas ese token al código,
al repositorio ni a los archivos de distribución.
