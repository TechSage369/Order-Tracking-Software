from django.urls import path

from . import views

app_name = "billing"
urlpatterns = [
    path("", views.index, name='index'),
    path('modal/<int:order_id>', views.modal_view, name='modal-view'),
    path('update-order/<int:order_id>', views.update_order, name='update_order'),
    path('modal-save', views.modal_save, name='modal_save'),
    path('delete-order/<int:order_id>', views.delete_order, name='delete_order'),
]

htmx_patterns = [
    path('search-items',
         views.search_items,
         name="search_items"
         ),

    path('add-item/<int:item_id>/',
         views.add_item,
         name="add_item"
         ),

    path('update-item-quantity/<int:item_id>/<int:order_id>',
         views.update_item_quantity,
         name="update_item_quantity"
         ),

    path('delete-item/<int:item_id>/<int:order_id>',
         views.delete_item,
         name="delete_item"
         ),

    path('create-order/',
         views.create_order,
         name='create_order'),

    path('update-table-number/<int:order_id>',
         views.update_table_number,
         name='update_table_number'),

    path('print-receipt/<int:order_id>',
         views.print_receipt_view,
         name="print_receipt"),

    path('search-orders',
         views.search_orders,
         name="search_orders"),

    path('update-order-status/<int:order_id>',
         views.update_order_status,
         name="update_order_status"),

    path('update-payment-method/<int:order_id>',
         views.update_payment_method,
         name="update_payment_method"),
]

urlpatterns += htmx_patterns
