"""Manages router registration (FR-01)."""
import threading

from app.models.router import Router
from app.dao import router_dao, log_dao
from app.utils.logger import logger


class RouterRegistryController:
    def __init__(self):
        self.routers: dict = router_dao.load_routers()
        # Guards check-then-write below so two near-simultaneous
        # REGISTER_ROUTER messages for the same router_id can't both
        # pass the duplicate check before either is stored.
        self._lock = threading.Lock()

    def register(self, router_id: str, ip: str, port: int) -> bool:
        """Register a new router under `router_id` (FR-01).

        Returns True if the router was registered. Returns False without
        modifying the registry if `router_id` is already registered
        (either by another instance or by this same router registering
        more than once) — the existing entry is preserved.
        """
        with self._lock:
            if router_id in self.routers:
                logger.warning(
                    f"Registration rejected: router_id '{router_id}' is already "
                    f"registered to {self.routers[router_id]}"
                )
                log_dao.append_log(
                    "REGISTER_REJECTED",
                    {"router_id": router_id, "ip": ip, "port": port, "reason": "duplicate router_id"},
                )
                return False

            router = Router(router_id, ip, port)
            self.routers[router_id] = router
            router_dao.save_routers(self.routers)
            log_dao.append_log("REGISTER", {"router_id": router_id, "ip": ip, "port": port})
            logger.info(f"Router registered: {router}")
            return True

    def remove_router(self, router_id: str) -> bool:
        """Deregister router_id from the registry (FR-09).

        Returns True if it existed and was removed, False if not found.
        """
        with self._lock:
            if router_id not in self.routers:
                logger.warning(
                    f"Removal rejected: router_id '{router_id}' not found in registry"
                )
                return False
            del self.routers[router_id]
            router_dao.save_routers(self.routers)
            log_dao.append_log("ROUTER_REMOVED", {"router_id": router_id})
            logger.info(f"Router removed from registry: {router_id}")
            return True

    def is_registered(self, router_id: str) -> bool:
        """Return True if `router_id` is already present in the registry (FR-01)."""
        return router_id in self.routers

    def get_router(self, router_id: str):
        return self.routers.get(router_id)

    def all_routers(self):
        return list(self.routers.values())
