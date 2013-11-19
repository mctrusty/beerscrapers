-- Function: process_beer_audit()

-- DROP FUNCTION process_beer_audit();

CREATE OR REPLACE FUNCTION process_beer_audit()
  RETURNS trigger AS
$BODY$
DECLARE oldprice character varying;
BEGIN
	-- This trigger checks to see if a row already exists, updates it if it does,
	-- inserts it if it does not, and then makes a note of any price changes in an
	-- audit table.
	IF EXISTS (SELECT 1 FROM beers WHERE store = NEW.store AND link = NEW.link)
	THEN
		SELECT price into oldprice from beers where store = NEW.store and link = NEW.link;
		IF (NEW.price != oldprice) THEN 
			INSERT INTO  price_audit VALUES(now(), NEW.store, NEW.link,NEW.price);
			UPDATE beers SET price = NEW.price WHERE store = NEW.store AND link = NEW.link;
		END IF;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION process_beer_audit()
  OWNER TO michael;
