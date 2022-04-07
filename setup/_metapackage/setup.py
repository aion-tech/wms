import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-wms",
    description="Meta package for oca-wms Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-delivery_carrier_preference',
        'odoo14-addon-delivery_carrier_warehouse',
        'odoo14-addon-delivery_preference_glue_stock_picking_group',
        'odoo14-addon-sale_stock_available_to_promise_release',
        'odoo14-addon-sale_stock_available_to_promise_release_cutoff',
        'odoo14-addon-sale_stock_available_to_promise_release_dropshipping',
        'odoo14-addon-shopfloor',
        'odoo14-addon-shopfloor_base',
        'odoo14-addon-shopfloor_batch_automatic_creation',
        'odoo14-addon-shopfloor_checkout_sync',
        'odoo14-addon-shopfloor_delivery_shipment',
        'odoo14-addon-shopfloor_delivery_shipment_mobile',
        'odoo14-addon-shopfloor_example',
        'odoo14-addon-shopfloor_manual_product_transfer',
        'odoo14-addon-shopfloor_manual_product_transfer_mobile',
        'odoo14-addon-shopfloor_mobile',
        'odoo14-addon-shopfloor_mobile_base',
        'odoo14-addon-shopfloor_mobile_base_auth_api_key',
        'odoo14-addon-shopfloor_mobile_base_auth_user',
        'odoo14-addon-shopfloor_packing_info',
        'odoo14-addon-shopfloor_rest_log',
        'odoo14-addon-shopfloor_workstation',
        'odoo14-addon-shopfloor_workstation_label_printer',
        'odoo14-addon-shopfloor_workstation_mobile',
        'odoo14-addon-stock_available_to_promise_release',
        'odoo14-addon-stock_available_to_promise_release_dynamic_routing',
        'odoo14-addon-stock_checkout_sync',
        'odoo14-addon-stock_dynamic_routing',
        'odoo14-addon-stock_dynamic_routing_checkout_sync',
        'odoo14-addon-stock_dynamic_routing_reserve_rule',
        'odoo14-addon-stock_move_source_relocate',
        'odoo14-addon-stock_move_source_relocate_dynamic_routing',
        'odoo14-addon-stock_picking_completion_info',
        'odoo14-addon-stock_picking_consolidation_priority',
        'odoo14-addon-stock_picking_type_shipping_policy',
        'odoo14-addon-stock_picking_type_shipping_policy_group_by',
        'odoo14-addon-stock_reception_screen',
        'odoo14-addon-stock_reception_screen_measuring_device',
        'odoo14-addon-stock_reception_screen_qty_by_packaging',
        'odoo14-addon-stock_storage_type',
        'odoo14-addon-stock_storage_type_buffer',
        'odoo14-addon-stock_storage_type_putaway_abc',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
