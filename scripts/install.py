#!/usr/bin/env python3
"""Instala el conjunto SDD localmente. Solo utiliza la biblioteca estándar."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
from uuid import uuid4


SKILLS = (
    "sdd-constitution", "sdd-context", "sdd-specify", "sdd-clarify",
    "sdd-plan", "sdd-tasks", "sdd-implement", "sdd-validate",
)
MARKER = ".sdd-install.json"
REPOSITORY = Path(__file__).resolve().parents[1]


class InstallError(Exception):
    """Conflicto que debe resolverse antes de instalar."""


@dataclass(frozen=True)
class InstallResult:
    installed: tuple[str, ...]
    unchanged: tuple[str, ...]
    backup: Path | None = None


def manifest(folder: Path) -> dict[str, str]:
    """Compara contenido real, incluidas adiciones locales, sin seguir enlaces."""
    result = {}
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise InstallError(f"Enlace dentro de la skill: {path}")
        if path.is_file() and path != folder / MARKER:
            result[path.relative_to(folder).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return result


def read_owner(folder: Path) -> dict:
    marker = folder / MARKER
    if marker.is_symlink():
        return {}
    try:
        owner = json.loads(marker.read_text(encoding="utf-8"))
        return owner if isinstance(owner, dict) else {}
    except (OSError, ValueError):
        return {}


def install(source: Path, destination: Path, *, update: bool = False) -> InstallResult:
    source = source.expanduser().resolve()
    destination = destination.expanduser().resolve()
    payload = source / "skills"
    if payload == destination or payload in destination.parents or destination in payload.parents:
        raise InstallError("El destino no puede solaparse con las skills de origen.")
    version = (source / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise InstallError("VERSION está vacía.")
    if destination.exists() and not destination.is_dir():
        raise InstallError(f"El destino no es una carpeta: {destination}")

    # Validar el conjunto entero antes de tocar ninguna instalación existente.
    expected = {}
    owners = {}
    for name in SKILLS:
        folder = payload / name
        if folder.is_symlink() or not (folder / "SKILL.md").is_file():
            raise InstallError(f"Skill de origen incompleta: {folder}")
        expected[name] = manifest(folder)
        owners[name] = {"managed_by": "sdd-skills", "skill": name, "version": version}

    changed, unchanged, previous, conflicts = [], [], [], []
    for name in SKILLS:
        target = destination / name
        if not target.exists() and not target.is_symlink():
            changed.append(name)
            continue
        if target.is_symlink() or not target.is_dir():
            conflicts.append(f"{name}: el destino es un archivo o enlace")
            continue
        owner = read_owner(target)
        if owner.get("managed_by") != "sdd-skills" or owner.get("skill") != name:
            conflicts.append(f"{name}: carpeta ajena o sin marca de este instalador")
            continue
        try:
            same = manifest(target) == expected[name] and owner == owners[name]
        except InstallError:
            same = False  # Una modificación local con enlaces también se respalda.
        if same:
            unchanged.append(name)
        elif update:
            changed.append(name)
            previous.append(name)
        else:
            conflicts.append(f"{name}: contenido o versión diferente; revisa y usa --update")
    if conflicts:
        raise InstallError("No se ha instalado ninguna skill:\n- " + "\n- ".join(conflicts))
    if not changed:
        return InstallResult((), tuple(unchanged))

    # Mantener copias y staging fuera del directorio que descubre skills evita
    # que un host cargue versiones antiguas o incompletas al recorrer subcarpetas.
    backup_root = destination.parent / f".{destination.name}-sdd-backups"
    if previous and (backup_root.is_symlink() or (backup_root.exists() and not backup_root.is_dir())):
        raise InstallError(f"La carpeta de copias no es un directorio seguro: {backup_root}")
    destination.mkdir(parents=True, exist_ok=True)
    backup = backup_root / uuid4().hex if previous else None
    with tempfile.TemporaryDirectory(prefix=".sdd-install-", dir=destination.parent) as temporary:
        staging = Path(temporary)
        for name in changed:
            staged = staging / name
            shutil.copytree(payload / name, staged)
            (staged / MARKER).write_text(
                json.dumps(owners[name], indent=2) + "\n", encoding="utf-8"
            )
        deployed, moved = [], []
        try:
            if backup is not None:
                backup.mkdir(parents=True)
            for name in changed:
                target = destination / name
                if name in previous:
                    target.rename(backup / name)
                    moved.append(name)
                elif target.exists() or target.is_symlink():
                    raise InstallError(f"El destino ha cambiado durante la instalación: {target}")
                (staging / name).rename(target)
                deployed.append(name)
        except BaseException as error:
            recovery_errors = []
            for name in reversed(deployed):
                try:
                    shutil.rmtree(destination / name)
                except OSError as recovery_error:
                    recovery_errors.append(str(recovery_error))
            for name in reversed(moved):
                try:
                    (backup / name).rename(destination / name)
                except OSError as recovery_error:
                    recovery_errors.append(str(recovery_error))
            if recovery_errors:
                raise InstallError(
                    f"Falló la instalación y parte de la recuperación. Revisa {backup}: "
                    + "; ".join(recovery_errors)
                ) from error
            if backup is not None and backup.exists():
                backup.rmdir()
            raise
    return InstallResult(tuple(changed), tuple(unchanged), backup)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dest", type=Path, default=Path.cwd() / "skills",
        help="Directorio de skills (por defecto: ./skills en el repositorio actual)",
    )
    parser.add_argument(
        "--update", action="store_true",
        help="Actualizar instalaciones propias diferentes, conservando copia previa",
    )
    args = parser.parse_args(argv)
    try:
        result = install(REPOSITORY, args.dest, update=args.update)
    except (InstallError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Destino: {args.dest.expanduser().resolve()}")
    print(f"Instaladas/actualizadas: {len(result.installed)}; sin cambios: {len(result.unchanged)}")
    if result.backup:
        print(f"Copia anterior: {result.backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
