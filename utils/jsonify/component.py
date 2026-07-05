from discord import Component


def jsonify_component(component: Component) -> dict:
    return {
        "type": str(component.type),
    }
