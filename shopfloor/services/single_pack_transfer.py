from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component

# TODO add completion info screen


class SinglePackTransfer(Component):
    """Methods for the Single Pack Transfer Process"""

    _inherit = "base.shopfloor.service"
    _name = "shopfloor.single.pack.transfer"
    _usage = "single_pack_transfer"
    _description = __doc__

    # TODO get rid of these methods now that we have a component
    # for the messages? could help for extensibility though...?
    def _response_for_empty_location(self, location):
        message = self.actions_for("message")
        return self._response(
            state="start", message=message.no_pack_in_location(location)
        )

    def _response_for_several_packages(self, location):
        message = self.actions_for("message")
        return self._response(
            state="start", message=message.several_packs_in_location(location)
        )

    def _response_for_package_not_found(self, barcode):
        message = self.actions_for("message")
        return self._response(
            state="start", message=message.package_not_found_for_barcode(barcode)
        )

    def _response_for_forbidden_package(self, barcode, picking_type):
        message = self.actions_for("message")
        return self._response(
            state="start",
            message=message.package_not_allowed_in_src_location(barcode, picking_type),
        )

    def _response_for_several_picking_types(self):
        message = self.actions_for("message")
        return self._response(state="start", message=message.several_picking_types())

    def _response_for_operation_not_found(self, pack):
        message = self.actions_for("message")
        return self._response(
            state="start", message=message.no_pending_operation_for_pack(pack)
        )

    def _data_after_package_scanned(self, move_line, pack):
        move = move_line.move_id
        return {
            "id": move_line.package_level_id.id,
            "name": pack.name,
            "location_src": {"id": pack.location_id.id, "name": pack.location_id.name},
            "location_dst": {
                "id": move_line.location_dest_id.id,
                "name": move_line.location_dest_id.name,
            },
            "product": {"id": move.product_id.id, "name": move.product_id.name},
            "picking": {"id": move.picking_id.id, "name": move.picking_id.name},
        }

    def _response_for_start_to_confirm(self, move_line, pack):
        message = self.actions_for("message")
        return self._response(
            state="confirm_start",
            message=message.already_running_ask_confirmation(),
            data=self._data_after_package_scanned(move_line, pack),
        )

    def _response_for_start_success(self, move_line, pack):
        message = self.actions_for("message")
        return self._response(
            state="scan_location",
            message=message.scan_destination(),
            data=self._data_after_package_scanned(move_line, pack),
        )

    def start(self, barcode):
        search = self.actions_for("search")

        picking_type = self.picking_types
        if len(picking_type) > 1:
            return self._response_for_several_picking_types()

        location = search.location_from_scan(barcode)

        pack = self.env["stock.quant.package"]
        if location:
            pack = self.env["stock.quant.package"].search(
                [("location_id", "=", location.id)]
            )
            if not pack:
                return self._response_for_empty_location(location)
            if len(pack) > 1:
                return self._response_for_several_packages(location)

        if not pack:
            pack = search.package_from_scan(barcode)

        if not pack:
            return self._response_for_package_not_found(barcode)

        if not pack.location_id.is_sublocation_of(picking_type.default_location_src_id):
            return self._response_for_forbidden_package(barcode, picking_type)

        existing_operations = self.env["stock.move.line"].search(
            [
                ("package_id", "=", pack.id),
                ("state", "!=", "done"),
                ("picking_id.picking_type_id", "in", self.picking_types.ids),
            ]
        )
        if not existing_operations:
            return self._response_for_operation_not_found(pack)
        # TODO can we have more than one move line?
        if existing_operations[0].package_level_id.is_done:
            return self._response_for_start_to_confirm(existing_operations, pack)

        existing_operations[0].package_level_id.is_done = True
        return self._response_for_start_success(existing_operations[0], pack)

    def _validator_start(self):
        return {"barcode": {"type": "string", "nullable": False, "required": True}}

    def _validator_return_start(self):
        return self._response_schema(
            {
                "id": {"coerce": to_int, "required": True, "type": "integer"},
                "name": {"type": "string", "nullable": False, "required": True},
                "location_src": {
                    "type": "dict",
                    "schema": {
                        "id": {"coerce": to_int, "required": True, "type": "integer"},
                        "name": {"type": "string", "nullable": False, "required": True},
                    },
                },
                "location_dst": {
                    "type": "dict",
                    "schema": {
                        "id": {"coerce": to_int, "required": True, "type": "integer"},
                        "name": {"type": "string", "nullable": False, "required": True},
                    },
                },
                "product": {
                    "type": "dict",
                    "schema": {
                        "id": {"coerce": to_int, "required": True, "type": "integer"},
                        "name": {"type": "string", "nullable": False, "required": True},
                    },
                },
                "picking": {
                    "type": "dict",
                    "schema": {
                        "id": {"coerce": to_int, "required": True, "type": "integer"},
                        "name": {"type": "string", "nullable": False, "required": True},
                    },
                },
            }
        )

    def _response_for_package_level_not_found(self):
        message = self.actions_for("message")
        return self._response(state="start", message=message.operation_not_found())

    def _response_for_move_canceled_elsewhere(self):
        message = self.actions_for("message")
        return self._response(
            state="start", message=message.operation_has_been_canceled_elsewhere()
        )

    def _response_for_location_not_found(self):
        message = self.actions_for("message")
        return self._response(
            state="scan_location", message=message.no_location_found()
        )

    def _response_for_forbidden_location(self):
        message = self.actions_for("message")
        return self._response(
            state="scan_location", message=message.dest_location_not_allowed()
        )

    def _response_for_location_need_confirm(self):
        message = self.actions_for("message")
        return self._response(
            state="confirm_location", message=message.need_confirmation()
        )

    def _response_for_validate_success(self):
        message = self.actions_for("message")
        return self._response(state="start", message=message.confirm_pack_moved())

    def validate(self, package_level_id, location_barcode, confirmation=False):
        """Validate the transfer"""
        # TODO this method is duplicated in putaway
        pack_transfer = self.actions_for("pack.transfer.validate")
        search = self.actions_for("search")

        package = self.env["stock.package_level"].browse(package_level_id)
        if not package.exists():
            return self._response_for_package_level_not_found()

        move = package.move_line_ids[0].move_id
        if not pack_transfer.is_move_state_valid(move):
            return self._response_for_move_canceled_elsewhere()

        scanned_location = search.location_from_scan(location_barcode)
        if not scanned_location:
            return self._response_for_location_not_found()
        if not pack_transfer.is_dest_location_valid(move, scanned_location):
            return self._response_for_forbidden_location()

        if pack_transfer.is_dest_location_to_confirm(move, scanned_location):
            if confirmation:
                # If the destination of the move would be incoherent
                # (move line outside of it), we change the moves' destination
                if not scanned_location.is_sublocation_of(move.location_dest_id):
                    move.location_dest_id = scanned_location.id
            else:
                return self._response_for_location_need_confirm()

        pack_transfer.set_destination_and_done(move, scanned_location)
        return self._response_for_validate_success()

    def _validator_validate(self):
        return {
            "package_level_id": {"coerce": to_int, "required": True, "type": "integer"},
            "location_barcode": {"type": "string", "nullable": False, "required": True},
            "confirmation": {"type": "boolean", "required": False},
        }

    def _validator_return_validate(self):
        return self._response_schema()

    def cancel(self, package_level_id):
        package = self.env["stock.package_level"].browse(package_level_id)
        if not package.exists():
            return self._response_for_package_level_not_found()
        # package.move_ids may be empty, it seems
        move = package.move_line_ids.move_id
        if move.state == "done":
            return self._response_for_move_already_processed()

        package.is_done = False
        return self._response_for_confirm_cancel()

    def _response_for_move_already_processed(self):
        message = self.actions_for("message")
        return self._response(state="start", message=message.already_done())

    def _response_for_confirm_cancel(self):
        message = self.actions_for("message")
        return self._response(
            state="start", message=message.confirm_canceled_scan_next_pack()
        )

    def _validator_cancel(self):
        return {
            "package_level_id": {"coerce": to_int, "required": True, "type": "integer"}
        }

    def _validator_return_cancel(self):
        return self._response_schema()
