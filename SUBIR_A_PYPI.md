# Publicación con GitHub Actions

El paquete se publica en PyPI como `experimentpy`, desde el repositorio
`UbaldoHervas/experimentation-library`.

## Configuración de PyPI

En https://pypi.org/manage/project/experimentpy/settings/publishing/ añade
un Trusted Publisher de GitHub Actions con estos valores:

| Campo | Valor |
| --- | --- |
| Owner | `UbaldoHervas` |
| Repository | `experimentation-library` |
| Workflow filename | `publish.yml` |
| Environment | `pypi` |

El archivo del flujo debe existir en `.github/workflows/publish.yml`.

## Publicar

Con el código actualizado en `main`, abre la pestaña Actions del repositorio,
selecciona **Publish to PyPI** y pulsa **Run workflow**, eligiendo `main`.
El flujo ejecuta los tests, construye y comprueba las distribuciones, y las
publica mediante OIDC. No necesita guardar un token de PyPI en GitHub.

La versión preparada es **0.1.2**. Cada publicación posterior requiere una
versión nueva en `pyproject.toml`, `src/experimentpy/__init__.py` y el test
de versión. Una versión ya publicada no se puede reemplazar.

PyPI verifica las URLs del mismo repositorio al subir mediante Trusted
Publishing. Un enlace de repositorio GitHub verificado permite mostrar el
panel de estadísticas en la ficha de esa versión.

Referencias:

- https://docs.pypi.org/project_metadata/#repository-statistics
- https://docs.pypi.org/trusted-publishers/adding-a-publisher/
- https://docs.pypi.org/trusted-publishers/using-a-publisher/
