import keyword


def service_dir(service: str) -> str:
    return f"{service}_" if keyword.iskeyword(service) else service


def class_name(service: str) -> str:
    parts = service.replace("_", "-").split("-")
    return "".join(p.capitalize() for p in parts) + "Client"


def enum_member(name: str) -> str:
    return name.replace("-", "_").upper()


def module_name(service: str) -> str:
    return f"{service.replace('-', '_')}_client"
