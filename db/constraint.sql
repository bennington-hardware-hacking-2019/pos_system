/* database constraint */ 

ALTER TABLE "transaction" ADD CONSTRAINT fk_link_nfc_tag FOREIGN KEY (nfc_tag) REFERENCES inventory (nfc_tag) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "transaction" ADD CONSTRAINT fk_link_bennington_id FOREIGN KEY (bennington_id) REFERENCES account (bennington_id) ON DELETE CASCADE ON UPDATE CASCADE;
