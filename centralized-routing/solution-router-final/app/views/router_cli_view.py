"""Router CLI view."""


def show_router_info(router):
    print(f"\n=== Router: {router.router_id} | {router.ip}:{router.port} ===")
