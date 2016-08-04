
def register_resource(api, resource_class, prefix = "/"):
    def fix_route(route):
        if route[0] == "/":
            route = route[1:]

        if prefix.endswith("/"):
            return prefix + route
        else:
            return prefix + "/" + route

    routes = map(fix_route, resource_class.get_routes())
    api.add_resource(resource_class, *routes)

