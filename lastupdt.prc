CREATE FUNCTION stamp_updated() RETURNS TRIGGER LANGUAGE 'plpgsql' AS $$
BEGIN
    NEW.last_updated := now();
    RETURN NEW;
END
$$;

ALTER TABLE beers ADD COLUMN last_updated TIMESTAMP;
CREATE TRIGGER beers_stamp_updated
    BEFORE INSERT OR UPDATE ON beers
    FOR EACH ROW EXECUTE PROCEDURE stamp_updated();