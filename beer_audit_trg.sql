-- Trigger: beer_audit on beers

-- DROP TRIGGER beer_audit ON beers;

CREATE TRIGGER beer_audit
  BEFORE INSERT
  ON beers
  FOR EACH ROW
  EXECUTE PROCEDURE process_beer_audit();
