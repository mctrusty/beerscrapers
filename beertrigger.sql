CREATE TABLE price_audit(
	stamp timestamp,
	store character varying,
	link character varying,
	price character varying
);

CREATE OR REPLACE FUNCTION process_beer_audit() RETURNS TRIGGER AS $process_beer_audit$
BEGIN
	-- This trigger checks to see if a row already exists, updates it if it does,
	-- inserts it if it does not, and then makes a note of any price changes in an
	-- audit table.
	IF EXISTS (SELECT 1 FROM beers WHERE store = NEW.store AND link = NEW.link)
	THEN
		IF (NEW.price != price) THEN 
			INSERT INTO  price_audit VALUES(now(), NEW.store, NEW.link,NEW.price)
		END IF;
	ELSE
		RETURN NEW;
	END IF;
END;
$process_beer_audit$
LANGUAGE plpgsql;

CREATE TRIGGER beer_audit
BEFORE INSERT OR UPDATE ON beers
	FOR EACH ROW EXECUTE PROCEDURE process_beer_audit();
	