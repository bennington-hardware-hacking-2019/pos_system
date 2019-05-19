/* database constraint - these link our fks */

ALTER TABLE "admin" ADD CONSTRAINT buyers_are_admins FOREIGN KEY (bennington_id) REFERENCES buyer (bennington_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "stock" ADD CONSTRAINT items_in_stock FOREIGN KEY (item_index) REFERENCES item (index) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "item" ADD CONSTRAINT purchases_have_items FOREIGN KEY (purchase_index) REFERENCES purchase (index) ON DELETE SET NULL ON UPDATE CASCADE;
