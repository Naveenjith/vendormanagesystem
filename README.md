
Setup Instructions:
Clone the repository to your local machine: git clone <https://github.com/Naveenjith/vendormanagesystem.git>
Install dependencies: pip install -r requirements.txt
Apply migrations: python manage.py migrate
Run the development server: python manage.py runserver

-vendor managing-
API Endpoints:
List all vendors:
Endpoint: GET /api/vendors/
Description: Retrieves a list of all vendors.
Create a new vendor:
Endpoint: POST /api/vendors/
Description: Creates a new vendor.
Retrieve a specific vendor:
Endpoint: GET /api/vendors/{vendor_id}/
Description: Retrieves details of a specific vendor.
Update a vendor:
Endpoint: PUT /api/vendors/{vendor_id}/
Description: Updates details of a specific vendor.
Delete a vendor:
Endpoint: DELETE /api/vendors/{vendor_id}/
Description: Deletes a specific vendor.
-purchase_orders managing-
API Endpoints:purchase_orders
● POST /api/purchase/: Create a purchase order.
● GET /api/purchase/?<vendor_id>: List all purchase orders with an option to filter by
vendor.
● GET /api/purchase/{po_id}/: Retrieve details of a specific purchase order.
● PUT /api/purchase/{po_id}/: Update a purchase order.
● DELETE /api/purchase/{po_id}/: Delete a purchase order.

-vendor performance-
GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance
metrics.
