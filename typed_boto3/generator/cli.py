import argparse
from pathlib import Path

from typed_boto3.generator.emitter import emit_service
from typed_boto3.generator.overloads_emitter import (
    write_package_init,
    write_service_name_enum,
    write_services_init,
)
from typed_boto3.generator.regions_emitter import write_region_enum


PACKAGE_ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m typed_boto3.generator")
    parser.add_argument(
        "--regions",
        action="store_true",
        help="Regenerate typed_boto3/_region.py from botocore partition metadata.",
    )
    parser.add_argument(
        "--service",
        nargs="+",
        default=[],
        help="boto3 service name(s) to generate (e.g. lambda s3).",
    )
    args = parser.parse_args(argv)

    if args.regions:
        write_region_enum(PACKAGE_ROOT)
        print(f"Wrote {PACKAGE_ROOT / '_region.py'}")

    if args.service:
        services_dir = PACKAGE_ROOT / "services"
        for svc in args.service:
            stats = emit_service(svc, services_dir)
            print(
                f"{svc}: {stats.total} ops (untyped_in={stats.untyped_input}, "
                f"untyped_out={stats.untyped_output})"
            )
        write_service_name_enum(args.service, PACKAGE_ROOT)
        write_services_init(args.service, services_dir)
        write_package_init(args.service, PACKAGE_ROOT)
        print(f"Updated {PACKAGE_ROOT / '__init__.py'}, {PACKAGE_ROOT / '_service_name.py'}, "
              f"{services_dir / '__init__.py'}")

    if not args.regions and not args.service:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
