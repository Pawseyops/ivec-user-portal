
CREATE LANGUAGE plpgsql;

-- Temporary procedure to migrate 5 boolean columns to a one-to-one relationship
-- This gets destroyed again before we commit the transaction.
CREATE FUNCTION migrate_priorityarea() RETURNS VOID AS $$
DECLARE
    app RECORD;
BEGIN
    FOR app IN SELECT id, priority_area_radio_astronomy, priority_area_geosciences,
        priority_area_directors, priority_area_partner, priority_area_national
        FROM allocation_application
    LOOP
        IF app.priority_area_radio_astronomy IS TRUE THEN
            UPDATE allocation_application SET
                priority_area_id=(SELECT id FROM allocation_priorityarea WHERE name='Astronomy')
                WHERE id=app.id;
        ELSIF app.priority_area_geosciences IS TRUE THEN
            UPDATE allocation_application SET
                priority_area_id=(SELECT id FROM allocation_priorityarea WHERE name='Geosciences')
                WHERE id=app.id;
        ELSIF app.priority_area_directors IS TRUE THEN
            UPDATE allocation_application SET
                priority_area_id=(SELECT id FROM allocation_priorityarea WHERE name='Directors')
                WHERE id=app.id;
        ELSIF app.priority_area_partner IS TRUE THEN
            UPDATE allocation_application SET
                priority_area_id=(SELECT id FROM allocation_priorityarea WHERE name='iVEC Partners')
                WHERE id=app.id;
        ELSIF app.priority_area_national IS TRUE THEN
            UPDATE allocation_application SET
                priority_area_id=(SELECT id FROM allocation_priorityarea WHERE name='National Merit')
                WHERE id=app.id;
        ELSE
            RAISE EXCEPTION 'Application %s has no priority area set, can''t migrate. Please fix manually and try again.', app.id;
        END IF;
    
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- New table, what was once columns of application is now a table
CREATE TABLE "allocation_priorityarea" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL,
    "code" varchar(32) NOT NULL,
    "description" varchar(1000) NOT NULL
);

-- Populate this new table with the previously hardcoded priority areas
INSERT INTO allocation_priorityarea (name, code, description) VALUES ('Astronomy', 'astronomy', 'Radio Astronomy Priority Area');
INSERT INTO allocation_priorityarea (name, code, description) VALUES ('Geosciences', 'geosciences', 'Geosciences Priority Area');
INSERT INTO allocation_priorityarea (name, code, description) VALUES ('Directors', 'director', 'Directors Priority Area');
INSERT INTO allocation_priorityarea (name, code, description) VALUES ('iVEC Partners', 'partner', 'iVEC Partners Priority Area');
INSERT INTO allocation_priorityarea (name, code, description) VALUES ('National Merit', 'national', 'National Merit Priority Area');

-- Find which priority area column is true and migrate that to the new
-- relational model before dropping the old columns
ALTER TABLE allocation_application ADD priority_area_id integer;
SELECT migrate_priorityarea();
ALTER TABLE allocation_application ALTER COLUMN priority_area_id SET NOT NULL; 
ALTER TABLE allocation_application DROP COLUMN priority_area_radio_astronomy;
ALTER TABLE allocation_application DROP COLUMN priority_area_geosciences;
ALTER TABLE allocation_application DROP COLUMN priority_area_directors;
ALTER TABLE allocation_application DROP COLUMN priority_area_partner;
ALTER TABLE allocation_application DROP COLUMN priority_area_national;

-- This table is a many to many mapping between allocationround and priorityarea
CREATE TABLE "allocation_allocationround_priority_area" (
    "id" serial NOT NULL PRIMARY KEY,
    "allocationround_id" integer NOT NULL,
    "priorityarea_id" integer NOT NULL REFERENCES "allocation_priorityarea" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("allocationround_id", "priorityarea_id")
);

-- Make sure the Epic Legacy allocation round supports all priority areas
INSERT INTO allocation_allocationround_priority_area (allocationround_id, priorityarea_id)
    VALUES ((SELECT id FROM allocation_allocationround WHERE name='Epic legacy'),
            (SELECT id FROM allocation_priorityarea WHERE name='Astronomy'));
INSERT INTO allocation_allocationround_priority_area (allocationround_id, priorityarea_id)
    VALUES ((SELECT id FROM allocation_allocationround WHERE name='Epic legacy'),
            (SELECT id FROM allocation_priorityarea WHERE name='Geosciences'));        
INSERT INTO allocation_allocationround_priority_area (allocationround_id, priorityarea_id)
    VALUES ((SELECT id FROM allocation_allocationround WHERE name='Epic legacy'),
            (SELECT id FROM allocation_priorityarea WHERE name='Directors'));                                     
INSERT INTO allocation_allocationround_priority_area (allocationround_id, priorityarea_id)
    VALUES ((SELECT id FROM allocation_allocationround WHERE name='Epic legacy'),
            (SELECT id FROM allocation_priorityarea WHERE name='iVEC Partners'));                                                               
INSERT INTO allocation_allocationround_priority_area (allocationround_id, priorityarea_id)
    VALUES ((SELECT id FROM allocation_allocationround WHERE name='Epic legacy'),
            (SELECT id FROM allocation_priorityarea WHERE name='National Merit'));
                                                        
-- Done with the procedure, so drop it before the commit            
DROP FUNCTION migrate_priorityarea();
