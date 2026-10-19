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
PROJECT_START = "<!-- sdd-skills:project:start -->"
PROJECT_END = "<!-- sdd-skills:project:end -->"


class InstallError(Exception):
    """Conflicto que debe resolverse antes de instalar."""


@dataclass(frozen=True)
class InstallResult:
    installed: tuple[str, ...]
    unchanged: tuple[str, ...]
    backup: Path | None = None


@dataclass(frozen=True)
class ProjectResult:
    constitution: str
    agent_context: str


def prepare_project(project: Path, version: str) -> ProjectResult:
    """Añade el punto de entrada SDD y un borrador de constitución, preservando el proyecto."""
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise InstallError(f"El proyecto no existe o no es un directorio: {project}")

    agents_path = project / "AGENTS.md"
    docs_path = project / "docs"
    constitution_path = docs_path / "constitution.md"
    if agents_path.is_symlink() or (agents_path.exists() and not agents_path.is_file()):
        raise InstallError("AGENTS.md es un enlace o no es un archivo regular.")
    if docs_path.is_symlink() or (docs_path.exists() and not docs_path.is_dir()):
        raise InstallError("docs/ es un enlace o no es un directorio seguro.")
    if constitution_path.is_symlink() or (
        constitution_path.exists() and not constitution_path.is_file()
    ):
        raise InstallError("docs/constitution.md es un enlace o no es un archivo regular.")

    old_agents = read_utf8(agents_path) if agents_path.exists() else ""
    start_count = old_agents.count(PROJECT_START)
    end_count = old_agents.count(PROJECT_END)
    if start_count != end_count or start_count > 1:
        raise InstallError("AGENTS.md contiene marcadores SDD incompletos o duplicados.")

    block = "\n".join((
        PROJECT_START,
        "## SDD Skills",
        "",
        f"Metodología Spec Driven Development, skills de usuario versión {version}.",
        "En la primera tarea de desarrollo, usa `$sdd-constitution` para acordar",
        "seis principios y `$sdd-context` para registrar contexto y comandos verificados.",
        "Los principios deben acordarse; la constitución en borrador no autoriza código.",
        "",
        "Para cada cambio, sigue `$sdd-specify` → `$sdd-clarify` → `$sdd-plan` →",
        "`$sdd-tasks` → aprobación explícita → `$sdd-implement` → `$sdd-validate`.",
        "Consulta `docs/constitution.md`, `specs/current/` y el expediente bajo `specs/`.",
        "Conserva instrucciones de agente existentes y consulta sus contradicciones.",
        PROJECT_END,
    ))
    if start_count:
        start = old_agents.index(PROJECT_START)
        end = old_agents.index(PROJECT_END) + len(PROJECT_END)
        if end < start:
            raise InstallError("Los marcadores SDD de AGENTS.md están desordenados.")
        updated_agents = old_agents[:start] + block + old_agents[end:]
        agent_status = "actualizado" if updated_agents != old_agents else "sin cambios"
    else:
        separator = "\n\n" if old_agents else ""
        updated_agents = old_agents + separator + block + "\n"
        agent_status = "creado" if not agents_path.exists() else "actualizado"

    if constitution_path.exists():
        constitution_status = "conservada"
        initial_constitution = None
    else:
        constitution_status = "borrador creado"
        initial_constitution = (
            REPOSITORY / "skills" / "sdd-constitution" / "assets" / "constitution.md"
        ).read_text(encoding="utf-8")

    # Preparar todo en la raíz del proyecto para que las sustituciones sean locales;
    # si una escritura falla, restaurar AGENTS.md y retirar el borrador parcial.
    old_agent_bytes = agents_path.read_bytes() if agents_path.exists() else None
    created_constitution = False
    created_docs = not docs_path.exists()
    try:
        if initial_constitution is not None:
            docs_path.mkdir(exist_ok=True)
            with constitution_path.open("x", encoding="utf-8", newline="") as stream:
                created_constitution = True
                stream.write(initial_constitution)
        if not agents_path.exists() or updated_agents != old_agents:
            agents_path.write_text(updated_agents, encoding="utf-8", newline="")
    except OSError as error:
        if created_constitution and constitution_path.exists():
            constitution_path.unlink()
        if old_agent_bytes is None:
            if agents_path.exists():
                agents_path.unlink()
        else:
            agents_path.write_bytes(old_agent_bytes)
        if created_docs and docs_path.exists():
            docs_path.rmdir()
        raise InstallError(f"No se pudo preparar el proyecto; se restauró su contexto: {error}") from error

    return ProjectResult(constitution_status, agent_status)


def prepare_project_preview(project: Path) -> None:
    """Detecta conflictos del proyecto antes de instalar las skills de usuario."""
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise InstallError(f"El proyecto no existe o no es un directorio: {project}")
    agents_path = project / "AGENTS.md"
    docs_path = project / "docs"
    constitution_path = docs_path / "constitution.md"
    if agents_path.is_symlink() or (agents_path.exists() and not agents_path.is_file()):
        raise InstallError("AGENTS.md es un enlace o no es un archivo regular.")
    if docs_path.is_symlink() or (docs_path.exists() and not docs_path.is_dir()):
        raise InstallError("docs/ es un enlace o no es un directorio seguro.")
    if constitution_path.is_symlink() or (
        constitution_path.exists() and not constitution_path.is_file()
    ):
        raise InstallError("docs/constitution.md es un enlace o no es un archivo regular.")
    if agents_path.exists():
        try:
            existing = read_utf8(agents_path)
        except UnicodeError as error:
            raise InstallError("AGENTS.md no es texto UTF-8; resuelve su formato antes de preparar SDD.") from error
        starts, ends = existing.count(PROJECT_START), existing.count(PROJECT_END)
        if starts != ends or starts > 1:
            raise InstallError("AGENTS.md contiene marcadores SDD incompletos o duplicados.")
        if starts and existing.index(PROJECT_END) < existing.index(PROJECT_START):
            raise InstallError("Los marcadores SDD de AGENTS.md están desordenados.")


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


def read_utf8(path: Path) -> str:
    """Read text without normalizing line endings outside the managed section."""
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


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
        "--dest", type=Path, default=Path.home() / ".agents" / "skills",
        help="Directorio de skills (por defecto: ~/.agents/skills)",
    )
    parser.add_argument(
        "--update", action="store_true",
        help="Actualizar instalaciones propias diferentes, conservando copia previa",
    )
    parser.add_argument(
        "--project", type=Path,
        help="Instalar skills y preparar también este proyecto con AGENTS.md y una constitución en borrador",
    )
    args = parser.parse_args(argv)
    try:
        if args.project is not None:
            # Resolver conflictos del proyecto antes de instalar cualquier skill.
            prepare_project_preview(args.project)
        result = install(REPOSITORY, args.dest, update=args.update)
        project_result = (
            prepare_project(args.project, (REPOSITORY / "VERSION").read_text(encoding="utf-8").strip())
            if args.project is not None else None
        )
    except (InstallError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Destino: {args.dest.expanduser().resolve()}")
    print(f"Instaladas/actualizadas: {len(result.installed)}; sin cambios: {len(result.unchanged)}")
    if result.backup:
        print(f"Copia anterior: {result.backup}")
    if project_result:
        print(f"Proyecto: {args.project.expanduser().resolve()}")
        print(f"Constitución: {project_result.constitution}; AGENTS.md: {project_result.agent_context}")
        print("En Codex, usa $sdd-constitution para acordar los seis principios del proyecto.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
