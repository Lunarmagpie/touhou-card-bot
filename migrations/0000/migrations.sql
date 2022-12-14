CREATE TABLE players ();
CREATE TABLE interactions ();
CREATE TABLE _migrations ();
ALTER TABLE players ADD COLUMN id BIGINT;
ALTER TABLE players ADD COLUMN decks JSON;
ALTER TABLE players ADD COLUMN cards INTEGER[];
ALTER TABLE interactions ADD COLUMN serial_id SERIAL;
ALTER TABLE interactions ADD COLUMN id BIGINT;
ALTER TABLE interactions ADD COLUMN token VARCHAR;
ALTER TABLE _migrations ADD COLUMN id_ INTEGER;
ALTER TABLE players ALTER COLUMN id SET NOT NULL;
ALTER TABLE players ALTER COLUMN decks SET NOT NULL;
ALTER TABLE players ALTER COLUMN cards SET NOT NULL;
ALTER TABLE interactions ALTER COLUMN serial_id SET NOT NULL;
ALTER TABLE interactions ALTER COLUMN id SET NOT NULL;
ALTER TABLE interactions ALTER COLUMN token SET NOT NULL;
ALTER TABLE _migrations ALTER COLUMN id_ SET NOT NULL;
ALTER TABLE players ADD CONSTRAINT _players_id_primary_key PRIMARY KEY ( id );
ALTER TABLE interactions ADD CONSTRAINT _interactions_serial_id_primary_key PRIMARY KEY ( serial_id );
ALTER TABLE _migrations ADD CONSTRAINT __migrations_id__primary_key PRIMARY KEY ( id_ );